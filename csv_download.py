import os
import pandas as pd

def download(csvPath: str):
    # 检查文件是否存在
    if not os.path.exists(csvPath):
        print(f"Error: The file '{csvPath}' does not exist.")
        return

    # 尝试读取 CSV 文件
    try:
        data = pd.read_csv(csvPath)
    except Exception as e:
        print(f"Error: Failed to read the CSV file. {e}")
        return

    # 检查 CSV 文件的列名是否符合要求
    required_columns = ['Rank', 'Author', 'Title', 'Citations', 'Year', 'Publisher', 'Venue', 'describe', 'Source']
    
    if list(data.columns) != required_columns:
        print("Error: The CSV file does not have the correct format.")
        print(f"Expected columns: {required_columns}")
        print(f"Found columns: {list(data.columns)}")
        return

    print(f"CSV file '{csvPath}' is valid.")
    print("Download success.")