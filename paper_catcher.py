import argparse
import time, os
from google_scholar_spider import ArgsConfig, google_scholar_spider
from csv_download import download


def get_command_line_args() -> ArgsConfig:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('--task', type=str, required=True,
                        choices=['catch', 'download', 'c', 'd', 'catch&download', 'c&d'], help="Task to perform: 'catch' or 'download'")
    parser.add_argument('--kw', type=str,
                        help="""Keyword to be searched. Use double quote followed by simple quote to search for an exact keyword. Example: "'exact keyword'" """)
    parser.add_argument('--source', type=str, help='Source for search')
    parser.add_argument('--sortby', type=str, help='Column to be sorted by. Default is "Citations".')
    parser.add_argument('--nresults', type=int, help='Number of articles to search on Google Scholar. Default is 100.')
    parser.add_argument('--path', type=str, help='Path to save the exported CSV file. Default is the current folder')

    args, _ = parser.parse_known_args()

    return ArgsConfig(
        task=args.task,
        keyword=args.kw if args.kw else ArgsConfig.keyword,
        nresults=args.nresults if args.nresults else ArgsConfig.nresults,
        csvpath=args.path if args.path else ArgsConfig.csvpath,
        sortby=args.sortby if args.sortby else ArgsConfig.sortby,
        source=args.source if args.source else ArgsConfig.source
    )

def main():
    print("Getting command line arguments...")
    start = time.time()
    
    # Get command line arguments
    args = get_command_line_args()

    # Perform the task based on the argument
    if args.task.lower() == 'catch' or args.task.lower() == 'c':
        google_scholar_spider(GoogleScholarConfig=args)
    elif args.task.lower() == 'download' or args.task.lower() == 'd':
        download(args.csvpath)
    elif args.task.lower() == 'catch&download' or args.task.lower() == 'c&d':
        google_scholar_spider(GoogleScholarConfig=args)
        keyword = f'{args.source}_{args.keyword}'
        download(os.path.join(args.csvpath, keyword.replace(' ', '_').replace(':','-') + '.csv'))

    end = time.time()
    print("Task completed!")
    print(f"Time taken: {end - start:.2f} seconds")

if __name__ == '__main__':
    main()
