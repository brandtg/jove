# spyndle

A terminal-focused alternative to Jupyter notebooks

## Usage

Create a new project

```
python -m spyndle.workspace newproject myproject
```

Create a new analysis

```
cd myproject
python -m spyndle.workspace newanalysis myanalysis
```

TODOs

- [ ] Command to upgrade `lib.py`, `shell.sh` files in existing analysis repos
- [ ] Helper to generate a markdown table (df.to_markdown() and append to README
