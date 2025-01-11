import os

DIRNAME_FIGURES = "{dirname_figures}"
DIRNAME_DATA = "{dirname_data}"


def find_next_id(dirname, prefix, suffix):
    """
    Finds the next sequential ID among files that share the same prefix/suffix.
    """
    max_id = 0
    for filename in os.listdir(dirname):
        if filename.startswith(prefix) and filename.endswith(suffix):
            id_ = int(os.path.splitext(filename)[0].split("-")[1])
            if id_ > max_id:
                max_id = id_
    next_id = max_id + 1
    return "".join([prefix, str(next_id), suffix])


def save_csv(df, prefix=None, filename=None, *args, **kwargs):
    """
    Saves a Pandas DataFrame as CSV.

    :param df: Pandas DataFrame to save as CSV
    :param prefix: Prefix of the CSV file (default: table-)
    :param filename: If provided, use this instead of prefix naming scheme.
    """
    if prefix and filename:
        raise ValueError("Only provide one of prefix or filename")
    elif not filename:
        filename = find_next_id(DIRNAME_DATA, prefix or "table-", ".csv")
    df.to_csv(os.path.join(DIRNAME_DATA, filename), *args, **kwargs)


def save_fig(fig, prefix=None, filename=None, *args, **kwargs):
    """
    Saves a Matplotlib figure as PNG.

    :param fig: Matplotlib figure object
    :param prefix: Prefix of the PNG file (default: fig-)
    :param filename: If provided, use this instead of prefix naming scheme.
    """
    if prefix and filename:
        raise ValueError("Only provide one of prefix or filename")
    elif not filename:
        filename = find_next_id(DIRNAME_FIGURES, prefix or "fig-", ".png")
    fig.savefig(os.path.join(DIRNAME_FIGURES, filename), *args, **kwargs)


def save_wip(filename="wip.py", session=0, start=1, stop=None, raw=True):
    """
    Appends IPython commands to a work-in-progress file for further refinement.

    Note that the ``wip.py`` file is sourced when ``shell.sh`` starts.

    :param filename: Append work-in-progress code to this file.
    :seealso: :func:``IPython.core.history.HistoryManager.get_range``
    """
    from IPython import get_ipython

    history_manager = get_ipython().history_manager
    history = [
        dict(session_id=session_id, line_number=line_number, input_line=input_line)
        for session_id, line_number, input_line in history_manager.get_range(
            session=session, start=start, stop=stop, raw=raw
        )
    ]
    with open(filename, "a") as f:
        for elt in history:
            input_line = elt["input_line"]
            if "save_wip" not in input_line:
                f.write(input_line + "\n")
