import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database_controller import connect_to_maria_db, check_connection, close_connection, save_events_to_db
from src._utils.setup_logging import setup_logging
from src.crawler import get_events
from src.config import headers, N8N_WEBHOOK_URL
from src.target import sites
from src.n8n import title_filter
import logging
import requests

logs_dir = 'logs'
logger = logging.getLogger('main')

def run():
    connection = None
    try:
        roles = "admin"
        connection = connect_to_maria_db(roles)
        if connection:
            if check_connection(connection):
                logger.info("資料庫連接正常")
                logger.info(f"使用 n8n webhook URL: {N8N_WEBHOOK_URL}")
                
                for site in sites:
                    try:
                        events = get_events(site, headers)
                        logger.info(f"從 {site['school']} 獲取到 {len(events)} 筆資料")
                        filtered_events = title_filter(N8N_WEBHOOK_URL, events)
                        save_events_to_db(connection, filtered_events)
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
                        logger.warning(f"請求 {site['school']} 時發生網路錯誤 ({type(e).__name__})，跳過此網站")
                        continue
                    except requests.exceptions.RequestException as e:
                        logger.error(f"請求 {site['school']} 發生錯誤: {e}")
                        continue
            else:
                logger.error("資料庫連接失敗，無法執行爬蟲")
        else:
            logger.error("無法建立資料庫連接，無法執行爬蟲")
    except Exception as e:
        logger.exception(f"執行 run() 時發生未預期錯誤: {e}")
    finally:
        if connection:
            close_connection(connection)

if __name__ == "__main__":
    setup_logging(logs_dir)
    run()