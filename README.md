# jove

A terminal-focused alternative to Jupyter notebooks.

Jove works with [Anaconda](https://docs.anaconda.com/anaconda/install/), and assumes that your system has it
installed. 

Jove targets a middle ground between Jupyter Notebooks and iPython, providing enough structure to keep a data
analysis organized, without a complex multimedia JSON document. Instead, it provides a loose file-oriented analysis
framework, which is intended as a starting point for an analysis to [evolve in complexity
naturally](https://knowyourmeme.com/memes/pepe-silvia).

This approach lends itself to productionizing code (all logic is in simple Python files), as well as sharing insights
(all exposition is in a Markdown file, with linked images and data.)  It also lets you stay in the terminal and do all
of your data work [in Neovim, btw](https://neovimbtw.com/en-usd/). 

Some other complimentary CLI tools include:

- [jq](https://jqlang.github.io/jq/) for JSON data
- [Miller](https://github.com/johnkerl/miller) for CSV data
- [VisiData](https://www.visidata.org/) for more complex spreadsheets

## Usage

Create a new analysis in the current directory

```
jove start myanalysis
```

The analysis directory initializes a few key files and directories, which are intended to be modified as needed for each analysis:

```
$ tree myproject/
myproject/
└── myanalysis
    ├── code.py
    ├── data
    ├── figures
    ├── lib.py
    ├── README.md
    └── shell.sh
```

- `README.md`: Markdown file with analysis notes
    - Named README.md so GitHub auto-renders when viewing the root directory
- `data`: Stores analysis datasets (CSVs, JSON, etc.)
- `figures`: Stores charts and figures
- `lib.py`: Helper functions for performing analysis
    - `save_csv`: Writes a Pandas DataFrame as CSV in `data`
    - `save_fig`: Writes a Matplotlib figure as PNG in `figures`
- `code.py`: Analysis-specific functions and code
- `shell.sh`: Starts an iPython shell, and runs lib.py then code.py

## Example

Navigate to the analysis created above

```
cd myanalysis
```

Download some random CSV file

```
wget https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv -O data/iris.csv
```

Run the following to start an iPython session

```
./shell.sh
```

Load the data

```python
df = pd.read_csv("data/iris.csv")
```

Compute descriptive statistics, save them as a CSV using the `save_csv` helper function (this will create
`./data/data-1.csv`), and output them as a markdown table (to copy into `README.md`)

```python
sepal_length = df.sepal_length.describe()
save_csv(sepal_length)
print(sepal_length.to_markdown())
```

View a histogram and save it as a figure (this will create `./figures/fig-1.csv`)

```python
ax = df.sepal_length.hist()
save_fig(ax.figure)
```

The idea is to iteratively build out code in addition to insights, so after a bit of exploration, it's a good idea to
copy these commands into `code.py` as a new utility function

```python
def get_sepal_length_stats(df):
    sepal_length = df.sepal_length.describe()
    ax = df.sepal_length.hist()
    return sepal_length, ax.figure  # Return the data and figure, for repeatability
```

Now, close the shell and re-open it, or execute `%run ./code.py` in your current shell, then use the utility method to
get the results again

```python
df = pd.read_csv("data/iris.csv")
sepal_length, fig = get_sepal_length_stats(df)
```

# TODOs

- [ ] Command to upgrade `lib.py`, `shell.sh` files in existing analysis repos
- [ ] Helper to generate a markdown table (df.to_markdown() and append to README
