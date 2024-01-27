def compare_dicts(A, B, show=None):
    for key in A.keys():
        if key in B.keys():
            match = A[key] == B[key]
            if show is None:
                print(f"{key}: {A[key]} -> match?: {match}")
            elif show and match:
                print(f"{key}: {A[key]} -> match?: {match}")
            elif (not show) and (not match):
                print(f"{key}: {A[key]} -> match?: {match}")
