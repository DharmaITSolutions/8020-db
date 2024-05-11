# CSV Total Extractor and Visualizer

## Overview

This project provides a Python script that processes a collection of CSV files to extract financial totals and corresponding dates, then visualizes this data over time. This is particularly useful for analyzing spending patterns from multiple receipt files stored in CSV format.

## Features

- Extract totals from specified lines near the end of each CSV file.
- Extract date information from a specific line in each CSV file.
- Accumulate totals by date.
- Generate a plot to visualize total spending over time.

## Requirements

- Python 3.6 or higher
- Matplotlib (for plotting graphs)

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository


pip install matplotlib
```
## Usage:

Place all your CSV files in a directory (e.g., receipts/).
Modify the script to point to your directory of CSV files by setting the directory_path variable.
Run the script:

```bash

python calculate_totals.py
```