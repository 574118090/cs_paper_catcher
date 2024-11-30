# CS Paper Catcher

**CS Paper Catcher** is a web scraper based on Google Scholar, designed to fetch papers from specific conferences. This tool helps researchers quickly gather paper information from selected conferences and save the data in CSV format. Future plans include adding PDF download functionality.

The project forked from [**google_scholar_spider**](https://github.com/JessyTsui/google_scholar_spider).

## Features

- Search for papers based on keywords and conference names.
- Sort papers by citation count.
- Filter papers by specific years (start and end year).
- Automatically save the fetched data as a CSV file.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/cs-paper-catcher.git
   cd cs-paper-catcher
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Arguments

```
python google_scholar_spider.py --kw "Machine Learning" --source "ICML 2024, ACL 2024" --nresults 50 --path "./papers"
```

### Argument Description

- `--kw`: The keyword to search for (required).
- `--source`: The name of the conference or journal to filter papers by (required).
- `--sortby`: The column to sort by (optional, default is "Citations").
- `--nresults`: The number of search results to fetch (optional, default is 100).
- `--path`: The path to save the CSV file (optional, default is the current directory).

### Examples

#### Example 1: Search for papers from a specific conference

```
python google_scholar_spider.py --kw "Deep Learning" --source "CVPR 2023" --nresults 50 --path "./cvpr_papers"
```

This command will search for papers with the keyword "Deep Learning" in the "CVPR" conference and save the results to the `./cvpr_papers` folder.

#### Example 2: Search for papers within a specific year range and sort by citation count

```
python google_scholar_spider.py --kw "Reinforcement Learning" --source "NeurIPS 2024" --nresults 100 --sortby "Citations" --path "./neurips_papers"
```

This command will search for papers with the keyword "Reinforcement Learning" in the "NeurIPS" conference, sort the results by citation count, and save the data to the `./neurips_papers` folder.

## Development Plan

- PDF download functionality will be added in the future, allowing automatic downloading of the papers in PDF format.

## License

MIT License
