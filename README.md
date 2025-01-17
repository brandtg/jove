# jove

A terminal-focused alternative to Jupyter notebooks.

Jove works with [Anaconda](https://docs.anaconda.com/anaconda/install/), and assumes that your system has it
installed. 

Jove targets a middle ground between Jupyter Notebooks and IPython, providing enough structure to keep a data
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

Install

```
python -m pip install jove
```

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
    ├── libjove.py
    ├── README.md
    └── shell.sh
```

- `README.md`: Markdown file with analysis notes
    - Named README.md so GitHub auto-renders when viewing the root directory
- `data`: Stores analysis datasets (CSVs, JSON, etc.)
- `figures`: Stores charts and figures
- `libjove.py`: Helper functions for performing analysis
    - `save_csv`: Writes a Pandas DataFrame as CSV in `data`
    - `save_fig`: Writes a Matplotlib figure as PNG in `figures`
- `code.py`: Refined analysis-specific functions and code
- `shell.sh`: Starts an IPython shell, and runs code files

## Example

Start a new analysis

```
jove start example-analysis
cd example-analysis
```

Download some random CSV file

```
wget https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv -O data/iris.csv
```

Run the following to start an IPython session

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
copy these commands into `code.py` as a new utility function. 

We can use the `save_wip()` helper function to first dump the session history into the `code.py` file, to avoid copy/paste.

```python
save_wip()
```

The `code.py` file should now look something like this

```python
# Add code that is a work in progress here, before promoting to code.py
df = pd.read_csv("data/iris.csv")
sepal_length = df.sepal_length.describe()
save_csv(sepal_length)
print(sepal_length.to_markdown())
ax = df.sepal_length.hist()
save_fig(ax.figure)
```

This is super messy, but we can quickly refactor it into something more usable. Open `code.py` in your favorite editor,
and refactor that into a nice function:

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

This process is a little more upfront work than the typical append-and-forget Jupyter notebook flow, but stopping to
refine thoughts, code, visualizations, etc. dramatically improves the quality and repeatability of analyses.
