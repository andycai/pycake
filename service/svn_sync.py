import os
import subprocess
import shutil
from config.svn import A_REPO_PATH, B_REPO_PATH
from utils.logger import SyncLogger

def run_cmd(cmd, cwd, logger):
    """Execute a command and log its output."""
    logger.log(f"Executing command: {cmd} (in {cwd})")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            logger.log(result.stdout.strip())
        if result.stderr:
            logger.log(result.stderr.strip())
        return result.returncode
    except subprocess.CalledProcessError as e:
        logger.log(f"Command failed: {e}")
        logger.log(f"Error output: {e.stderr}")
        raise

def svn_revert_and_update(repo_path, logger):
    """Revert and update SVN repository."""
    logger.log(f"Processing repository: {repo_path}")
    run_cmd("svn revert -R .", repo_path, logger)
    run_cmd("svn update", repo_path, logger)

def sync_paths(paths, logger):
    """Main synchronization function."""
    try:
        # 1. SVN revert & update
        logger.log("Starting synchronization process")
        svn_revert_and_update(A_REPO_PATH, logger)
        svn_revert_and_update(B_REPO_PATH, logger)

        # 2. Sync each path
        for rel_path in paths:
            src = os.path.join(A_REPO_PATH, rel_path)
            dst = os.path.join(B_REPO_PATH, rel_path)
            
            if not os.path.exists(src):
                logger.log(f"Warning: Source path does not exist: {src}")
                continue
                
            logger.log(f"Syncing {src} -> {dst}")

            # Remove existing destination if it exists
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)

            # Copy from source to destination
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

        # 3. Process SVN changes
        logger.log("Processing SVN changes")
        run_cmd("svn status", B_REPO_PATH, logger)
        
        # Get SVN status and process changes
        result = subprocess.run(
            "svn status",
            cwd=B_REPO_PATH,
            shell=True,
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.splitlines():
            if line.startswith("?"):
                file_path = line[1:].strip()
                run_cmd(f"svn add \"{file_path}\"", B_REPO_PATH, logger)
            elif line.startswith("!"):
                file_path = line[1:].strip()
                run_cmd(f"svn delete \"{file_path}\"", B_REPO_PATH, logger)

        # 4. Commit changes
        logger.log("Committing changes")
        run_cmd("svn commit -m 'sync update'", B_REPO_PATH, logger)
        logger.log("Synchronization completed successfully")

    except Exception as e:
        logger.log(f"Error during synchronization: {str(e)}")
        raise 