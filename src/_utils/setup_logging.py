import logging.config
import datetime
import os

def setup_logging(logs_dir):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_date_dir_path = os.path.join(logs_dir, current_date)
    
    current_time = datetime.datetime.now().strftime("%H-%M-%S")
    
    log_filename = f"{current_date}_{current_time}.log"
    
    log_config_path = os.path.join(os.path.dirname(__file__), '..\..', 'logging.ini')
    
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(current_date_dir_path, exist_ok=True)
    
    logging.config.fileConfig(
        log_config_path,
        defaults={
            'logsdir': logs_dir,
            'dirname': current_date,
            'filename': log_filename,
        },
        disable_existing_loggers=False
    )