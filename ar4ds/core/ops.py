
def filter(df, mask):
    output = df[mask]
    output.reset_index()
    return output

def agg(df, cols, target, fns):
    outcols = {}
    for f in fns:
        outcols[f+"("+target+")"] = f
    output = df.groupby(cols, as_index = False)[target].agg(outcols)
    return output
