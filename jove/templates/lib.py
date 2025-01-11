import os

DIRNAME_FIGURES = "{dirname_figures}"
DIRNAME_DATA = "{dirname_data}"


def find_next_id(dirname, prefix, suffix):
    max_id = 0
    for filename in os.listdir(dirname):
        if filename.startswith(prefix) and filename.endswith(suffix):
            id_ = int(os.path.splitext(filename)[0].split("-")[1])
            if id_ > max_id:
                max_id = id_
    next_id = max_id + 1
    return "".join([prefix, str(next_id), suffix])


def save_csv(df, prefix=None, filename=None, *args, **kwargs):
    if prefix and filename:
        raise ValueError("Only provide one of prefix or filename")
    elif not filename:
        filename = find_next_id(DIRNAME_DATA, prefix or "table-", ".csv")
    df.to_csv(os.path.join(DIRNAME_DATA, filename), *args, **kwargs)


def save_fig(fig, prefix=None, filename=None, *args, **kwargs):
    if prefix and filename:
        raise ValueError("Only provide one of prefix or filename")
    elif not filename:
        filename = find_next_id(DIRNAME_FIGURES, prefix or "fig-", ".png")
    fig.savefig(os.path.join(DIRNAME_FIGURES, filename), *args, **kwargs)
