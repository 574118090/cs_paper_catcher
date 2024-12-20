# CS Paper Catcher

[English](README.md) | [中文](README.zh-CN.md)

**CS Paper Catcher** 是一个基于 Google Scholar 的网页爬虫，旨在帮助用户快速抓取计算机科学领域特定会议或期刊的论文信息，并将数据保存为 CSV 格式。此外，工具还支持直接下载论文的 PDF 文件，进一步方便用户获取相关资源。**目前该工具仅支持下载部分来源的论文，我正在逐步完善对更多来源的支持。**

该项目是从 [**google_scholar_spider**](https://github.com/JessyTsui/google_scholar_spider) 项目派生的。

## 功能

- 根据关键词和会议、期刊名称搜索论文。
- 按引用次数对论文进行排序。
- 根据特定年份筛选论文。
- 自动将抓取的数据保存为 CSV 文件。
- 支持两种任务：
  - `catch`: 从 Google Scholar 抓取论文并保存为 CSV 文件。
  - `download`: 下载已存在 CSV 文件中列出的论文 PDF 文件。
  - `catch&download`: 同时执行两个任务。

## 安装

1. 克隆仓库：

   ```bash
   git clone https://github.com/574118090/cs_paper_catcher.git
   cd cs-paper-catcher
   ```

2. 安装依赖：

   ```
   pip install -r requirements.txt
   ```

## 使用

### 命令行参数

```
python paper_cathcer.py --task "catch" --kw "Machine Learning" --source "ICML,ACL" --year 2024 --nresults 50 --path "./papers"
```

### 参数说明

- `--task`: 要执行的任务。可以选择 `catch` 或 `download`或`catch&download`。
- `--kw`: 搜索的关键词（必选）。
- `--source`: 要筛选的会议或期刊名称（可选）。
- `--sortby`: 排序的列（可选，默认为“Citations”）。
- `--nresults`: 获取的搜索结果数量（可选，默认为 100）。
- `--path`: 保存或处理 CSV 文件的路径（可选，默认为当前目录）。
- `--year`:论文的发表年份。

### 示例

#### 示例 1：从 Google Scholar 抓取数据

```
python paper_catcher.py --task "catch" --kw "Deep Learning" --source "CVPR" --year 2023 --nresults 50 --path "./cvpr_papers" 
```

此命令将搜索关键词为“Deep Learning”的“CVPR 2023”会议论文，并将结果保存到 `./cvpr_papers` 文件夹中。

#### 示例 2：下载并处理 CSV 文件

```
python paper_catcher.py --task "download" --path "./cvpr_papers/CVPR_2023_Deep_Learning.csv"
```

此命令将根据现有的 CSV 文件，创建一个同名的文件夹，并将每篇论文的 PDF 文件下载到该文件夹中。

#### 示例 3：抓取数据并下载 PDF 文件

```
python paper_catcher.py --task "catch&download" --kw "Large Language Model" --source "NeurIPS" --year 2024 --nresults 50 --path "./neurips_papers"
```

此命令将首先抓取关键词为“Large Language Model”的“NeurIPS 2024”会议论文，然后下载对应的 PDF 文件到 `./neurips_papers` 文件夹中。

## 可下载的论文来源

目前支持下载以下来源的论文：

- **ACL**
- **NeuralPS**（来自 Openreview）
- **ICML**（来自 Openreview）
- **ICLR**（来自 Openreview）
- **AAAI**

## 许可证

MIT License