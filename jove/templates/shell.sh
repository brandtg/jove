#!/bin/bash

# Activate anaconda3
CONDA_SH="$HOME/anaconda3/etc/profile.d/conda.sh"
if [ -f "$CONDA_SH" ]; then
    source "$CONDA_SH"
else
    echo "Error: conda.sh not found at $CONDA_SH"
    exit 1
fi
conda activate

# Run ipython shell initialized by lib.py and code.py
cat libjove.py code.py wip.py > .session.py
ipython -i .session.py
