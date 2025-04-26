import argparse
from service.svn_sync import sync_paths
from utils.logger import SyncLogger
from config.svn import LOG_FILE

def main():
    parser = argparse.ArgumentParser(
        description="Synchronize directories between two SVN repositories"
    )
    parser.add_argument(
        "--paths",
        required=True,
        help="Comma-separated list of subdirectory paths to sync"
    )
    
    args = parser.parse_args()
    paths = [p.strip() for p in args.paths.split(",") if p.strip()]
    
    if not paths:
        print("Error: No valid paths provided")
        return 1
        
    logger = SyncLogger(LOG_FILE, to_stdout=True)
    try:
        sync_paths(paths, logger)
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 