# CS Paper Catcher

**CS Paper Catcher** is a web scraper based on Google Scholar, designed to fetch papers primarily in the field of **Computer Science** from specific conferences. This tool helps researchers quickly gather paper information from selected conferences in the CS domain and save the data in CSV format. Future plans include adding PDF download functionality.

The project forked from [**google_scholar_spider**](https://github.com/JessyTsui/google_scholar_spider).

## Features

- Search for papers based on keywords and conference names.
- Sort papers by citation count.
- Filter papers by specific years (start and end year).
- Automatically save the fetched data as a CSV file.
- Support two tasks:
  - `catch`: Fetch papers from Google Scholar and save them as a CSV.
  - `download`: Downloads the PDF files of the papers listed in an existing CSV file. It creates a folder named after the CSV file and saves the PDFs of each paper in that folder. The CSV must contain valid links to the papers.

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
python main.py --task catch --kw "Deep Learning" --source "CVPR 2023" --nresults 50 --path "./cvpr_papers"
```

This command will search for papers with the keyword "Deep Learning" in the "CVPR" conference and save the results to the `./cvpr_papers` folder.

#### Example 2: Download and process a CSV file

```
python main.py --task download --path "./cvpr_papers/CVPR_2023_Deep_Learning.csv"
```

This will create a folder with the same name as the CSV file and store the PDFs of each paper in that folder.

## Development Plan

- PDF download functionality will be added in the future, allowing automatic downloading of the papers in PDF format.

## License

MIT License
