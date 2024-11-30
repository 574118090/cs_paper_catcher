# CS Paper Catcher

[English](README.md) | [中文](README.zh-CN.md)

**CS Paper Catcher** is a web scraper based on Google Scholar, designed to fetch papers primarily in the field of **Computer Science** from specific sources. This tool helps researchers quickly gather paper information from selected sources in the CS domain and save the data in CSV format. Additionally, the tool now supports downloading the PDFs of the papers. Currently, it supports a limited number of sources, and future plans include expanding support for more sources.

The project forked from [**google_scholar_spider**](https://github.com/JessyTsui/google_scholar_spider).

## Features

- Search for papers based on keywords and sources(conferences, journals) names.
- Sort papers by citation count.
- Filter papers by specific years (start and end year).
- Automatically save the fetched data as a CSV file.
- Support two tasks:
  - `catch`: Fetch papers from Google Scholar and save them as a CSV.
  - `download`: Downloads the PDF files of the papers listed in an existing CSV file.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/574118090/cs_paper_catcher.git
   cd cs-paper-catcher
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Arguments

```
python paper_cathcer.py --task catch --kw "Machine Learning" --source "ICML 2024, ACL 2024" --nresults 50 --path "./papers"
```

### Argument Description

- `--task`: The task to perform. Choose either `catch` or `download`.
- `--kw`: The keyword to search for (required).
- `--source`: The name of the conference or journal to filter papers by (optional).
- `--sortby`: The column to sort by (optional, default is "Citations").
- `--nresults`: The number of search results to fetch (optional, default is 100).
- `--path`: The path to save or process the CSV file (optional, default is the current directory).

### Examples

#### Example 1: Catch data from Google Scholar

```
python paper_catcher.py --task catch --kw "Deep Learning" --source "CVPR 2023" --nresults 50 --path "./cvpr_papers"
```

This command will search for papers with the keyword "Deep Learning" in the "CVPR" conference and save the results to the `./cvpr_papers` folder.

#### Example 2: Download and process a CSV file

```
python paper_catcher.py --task download --path "./cvpr_papers/CVPR_2023_Deep_Learning.csv"
```

This will create a folder with the same name as the CSV file and store the PDFs of each paper in that folder.

#### Example 3: Catch data and download the PDFs

```
python paper_catcher.py --task catch&download --kw "Reinforcement Learning" --source "NeurIPS 2024" --nresults 50 --path "./neurips_papers"
```

This command will first fetch papers with the keyword "Reinforcement Learning" from the "NeurIPS 2024" conference and then download the corresponding PDFs to the `./neurips_papers` folder.

## Supported Source for Parsing and Download

Currently, the following source are supported for downloading papers:

- **ACL**
- **NeuralPS**(from Openreview)
- **ICML**(from Openreview)

## License

MIT License
