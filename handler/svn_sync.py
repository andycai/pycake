from core.web import post, Response
from service.svn_sync import sync_paths
from utils.logger import SyncLogger
from config.svn import LOG_FILE

@post('/sync')
def handle_sync(request):
    paths = request.body.get("paths", "")
    paths = [p.strip() for p in paths.split(",") if p.strip()]
    
    if not paths:
        return Response("Error: No valid paths provided", status_code=400)
    
    logger = SyncLogger(LOG_FILE, to_stdout=False)
    try:
        sync_paths(paths, logger)
        return Response(logger.get_logs())
    except Exception as e:
        return Response(
            f"Error: {str(e)}\n\nLogs:\n{logger.get_logs()}",
            status_code=500
        ) 