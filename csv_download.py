import os
import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

def sanitize_filename(filename: str):
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename

def parse_source(source: str):
    if "https://aclanthology.org/" in source:
        return source.rstrip('/') + '.pdf'
    if "openreview.net" in source:
        return source.replace('forum', 'pdf')
    if "ieeexplore.ieee.org/abstract" in source:
        return source.replace('abstract/document/', 'stamp/stamp.jsp?tp=&arnumber=').strip('/')
    if source.startswith('https://ojs.aaai.org/index.php'):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            response = requests.get(source, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                pdf_link = soup.find('a', class_='obj_galley_link pdf')
                if pdf_link and pdf_link.get('href'):
                    return pdf_link['href']
                else:
                    return 'has_not_supported'
            else:
                return 'has_not_supported'
        except Exception as e:
            return 'has_not_supported'
    if source.endswith('.pdf'):
        return source
    return 'has_not_supported'

def download(csvPath: str):
    if not os.path.exists(csvPath):
        return

    try:
        data = pd.read_csv(csvPath)
    except Exception as e:
        return

    if "download" not in data.columns:
        data["download"] = False

    required_columns = ['Rank', 'Author', 'Title', 'Citations', 'Year', 'Publisher', 'Venue', 'describe', 'Source', 'download']
    if list(data.columns) != required_columns:
        return

    folder_name = os.path.splitext(os.path.basename(csvPath))[0]
    folder_name = sanitize_filename(folder_name) 
    parent_dir = os.path.dirname(csvPath)
    folder_path = os.path.join(parent_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    success_count = 0
    failure_count = 0
    not_supported_count = 0
    failed_papers = []
    not_supported_papers = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for index, row in tqdm(data.iterrows(), total=len(data), desc="Downloading Papers", ncols=100):
        source_url = row['Source']
        parsed_url = parse_source(source_url)

        category_folder = os.path.join(folder_path)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        if parsed_url != 'has_not_supported':
            file_name = sanitize_filename(f"{row['Title']}.pdf")
            pdf_path = os.path.join(category_folder, file_name)

            if os.path.exists(pdf_path):
                data.at[index, 'download'] = True
                success_count += 1
                continue

            try:
                response = requests.get(parsed_url, headers=headers)
                if response.status_code == 200:
                    with open(pdf_path, 'wb') as pdf_file:
                        pdf_file.write(response.content)
                    data.at[index, 'download'] = True
                    success_count += 1
                else:
                    data.at[index, 'download'] = False
                    failure_count += 1
                    failed_papers.append(row['Title'])
            except Exception as e:
                data.at[index, 'download'] = False
                failure_count += 1
                failed_papers.append(row['Title'])
        else:
            not_supported_count += 1
            not_supported_papers.append(row['Title'])

    data.to_csv(csvPath, index=False)

    print("\nDownload process finished.")
    print(f"Total Success: {success_count}, Total Failure: {failure_count}, Not Supported: {not_supported_count}")

    if failure_count > 0:
        print("\nFailed Papers:")
        for paper in failed_papers:
            print(f"- {paper}")
    
    if not_supported_count > 0:
        print("\nNot Supported Papers:")
        for paper in not_supported_papers:
            print(f"- {paper}")
