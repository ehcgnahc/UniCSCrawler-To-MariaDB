from .database_controller import connect_to_maria_db, check_connection, close_connection, save_events_to_db
from .setup_logging import setup_logging
from .crawler import get_events
from .config import headers
from .target import sites
import logging
import requests
# import schedule

logs_dir = 'logs'
logger = logging.getLogger('main')

def run():
    connection = None
    try:
        roles = "admin" # admin, user
        connection = connect_to_maria_db(roles)
        if connection:
            if check_connection(connection):
                logger.info("資料庫連接正常")
                for site in sites:
                    try:
                        events = get_events(site, headers)
                        logger.info(f"從 {site['school']} 獲取到 {len(events)} 筆資料")
                        save_events_to_db(connection, events)
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