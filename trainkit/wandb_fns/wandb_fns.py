import os

import polars as pl
import wandb


def get_min_df(df):
    df = df.filter(pl.col("state") == "finished")
    df = df.filter(pl.col("d_model") == 16)
    df = df.cast({"parameter_count": pl.Int64})
    select = [
        "WQE P50 LTSP(All,All) [valid]",
        "WQE P50 LTSP(All,All) [train]",
        "parameter_count",
        "lr",
        "train_loss",
        "d_model",
        "mlp_width",
        "d_state",
        "num_blocks",
    ]
    df = df.select(select)
    group_cols = ["parameter_count", "d_model", "d_state", "mlp_width", "num_blocks"]
    min_df = (
        df.group_by(group_cols)
        .agg(
            pl.col("WQE P50 LTSP(All,All) [valid]").min(),
        )
        .join(df, on=group_cols + ["WQE P50 LTSP(All,All) [valid]"])
    )
    return min_df


def get_project_data(project, dynamic_vars, config_vars, rerun_pull=False):
    filepath = f"./logs/{project.replace('/', '_')}.csv"
    if os.path.exists(filepath) and not rerun_pull:
        print("Using existing table")
        df = pl.read_csv(filepath)
    else:
        print("Fetching")
        df = get_wandb_df(project=project, config_vars=config_vars, dynamic_vars=dynamic_vars)
        df.write_csv(filepath)
        print(f"Saved in {filepath}")
    return df


def get_wandb_df(project, config_vars, dynamic_vars):
    api = wandb.Api()
    runs = api.runs(project)

    data = []
    for run in runs:
        all = {"name": run.name, "state": run.state}
        all.update({key: val for key, val in run.config.items() if key in config_vars})
        aux = {key: val for key, val in all.items()}
        aux.update({key: val for key, val in run.summary._json_dict.items() if key in dynamic_vars})
        data.append(aux)

    runs_df = pl.DataFrame(data, schema=["name", "state"] + dynamic_vars + config_vars)
    return runs_df


def get_wandb_dynamic_df(project, configs, filters):
    api = wandb.Api(timeout=59)
    runs = api.runs(project, filters=filters)

    data, col_order = [], None
    for run in runs:
        all = {"name": run.name, "state": run.state}
        all.update({key: val for key, val in run.config.items() if key in configs})
        print("Going over:")
        print(all)
        df = run.history()
        df = pl.DataFrame(df)
        for key, val in all.items():
            df = df.with_columns(pl.lit(val).alias(key))
        if col_order is None:
            col_order = df.columns
        data.append(df.select(col_order))
    data = pl.concat(data)

    return data


def run_selector_fn(run_config, config_vals):
    checks = []
    for case in config_vals:
        checks.append(all([run_config[k] == val for k, val in case.items()]))
    return any(checks)
