from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from services.file_manager import FileManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def cleanup_old_files_job():
    logger.info("Starting cleanup of old CSV files")
    try:
        file_manager = FileManager()
        file_manager.cleanup_old_files(days=30)
        logger.info("Cleanup completed successfully")
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")

def start_scheduler():
    scheduler.add_job(
        cleanup_old_files_job,
        CronTrigger(hour=2, minute=0),
        id="cleanup_old_files",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down")
