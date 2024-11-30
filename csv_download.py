import os
import pandas as pd
import requests
from tqdm import tqdm

def sanitize_filename(filename: str):
    """
    替换文件名中的非法字符（Windows系统）为下划线。
    """
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename

def parse_source(source: str):
    """
    解析Source字段，检查是否包含https://aclanthology.org/，并返回解析后的URL和类别（'ACL' 或 'others'）。
    """
    if "https://aclanthology.org/" in source:
        # 将URL末尾的斜杠替换为.pdf
        return source.rstrip('/') + '.pdf'
    if "openreview.net" in source:
        return source.replace('forum', 'pdf')
    if source.endswith('.pdf'):
        return source
    return 'has_not_supported'

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

    # 检查 CSV 文件是否有"download"这一列，如果没有则新增，并设为False
    if "download" not in data.columns:
        data["download"] = False

    # 检查 CSV 文件的列名是否符合要求
    required_columns = ['Rank', 'Author', 'Title', 'Citations', 'Year', 'Publisher', 'Venue', 'describe', 'Source', 'download']
    if list(data.columns) != required_columns:
        print("Error: The CSV file does not have the correct format.")
        print(f"Expected columns: {required_columns}")
        print(f"Found columns: {list(data.columns)}")
        return

    # 创建保存PDF的文件夹，文件夹名与CSV文件同名，并与CSV文件同目录
    folder_name = os.path.splitext(os.path.basename(csvPath))[0]
    folder_name = sanitize_filename(folder_name)  # 清理文件夹名中的非法字符
    parent_dir = os.path.dirname(csvPath)  # 获取CSV文件所在的目录
    folder_path = os.path.join(parent_dir, folder_name)  # 将文件夹路径设置为CSV文件所在目录下的同名文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 初始化计数器和失败的论文列表
    success_count = 0
    failure_count = 0
    not_supported_count = 0  # 用于统计“暂不支持”的记录
    failed_papers = []
    not_supported_papers = []  # 用于存储暂不支持的论文

    # 使用 tqdm 显示进度条
    for index, row in tqdm(data.iterrows(), total=len(data), desc="Downloading Papers", ncols=100):
        source_url = row['Source']
        parsed_url = parse_source(source_url)

        # 为每个类别（ACL / others）创建一个子文件夹
        category_folder = os.path.join(folder_path)  # 清理子文件夹名
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # 如果是有效的PDF链接，检查文件是否已存在
        if parsed_url != 'has_not_supported':
            # 文件名中替换冒号为下划线
            file_name = sanitize_filename(f"{row['Title']}.pdf")  # 清理文件名中的非法字符
            pdf_path = os.path.join(category_folder, file_name)

            # 检查文件是否已经存在
            if os.path.exists(pdf_path):
                data.at[index, 'download'] = True  # 标记为已下载
                success_count += 1
                continue

            try:
                # 下载文件
                response = requests.get(parsed_url)
                if response.status_code == 200:
                    with open(pdf_path, 'wb') as pdf_file:
                        pdf_file.write(response.content)
                    data.at[index, 'download'] = True  # 更新为已下载
                    success_count += 1  # 增加成功计数
                else:
                    data.at[index, 'download'] = False  # 下载失败
                    failure_count += 1  # 增加失败计数
                    failed_papers.append(row['Title'])  # 添加到失败列表
            except Exception as e:
                data.at[index, 'download'] = False  # 下载失败
                failure_count += 1  # 增加失败计数
                failed_papers.append(row['Title'])  # 添加到失败列表
                print(f"Error: An error occurred while downloading {row['Title']}. {e}")
        else:
            # 记录“暂不支持”的论文
            not_supported_count += 1
            not_supported_papers.append(row['Title'])

    # 保存更新后的CSV文件
    data.to_csv(csvPath, index=False)

    # 完成下载后，打印结果
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
