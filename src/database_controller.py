from dotenv import load_dotenv, find_dotenv
from mysql.connector import Error
import mysql.connector
import logging
import os

logger = logging.getLogger('main')

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    logger.error("找不到 .env 檔案，請確保它存在於專案根目錄")

def connect_to_maria_db(roles):
    connection = None
    try:
        role_prefix = roles.upper()
        db_host = os.getenv(f"{role_prefix}_DB_HOST")
        db_port = os.getenv(f"{role_prefix}_DB_PORT")
        db_name = os.getenv(f"{role_prefix}_DB_NAME")
        db_user = os.getenv(f"{role_prefix}_DB_USER")
        db_password = os.getenv(f"{role_prefix}_DB_PASSWORD")
        
        logger.info(f"嘗試連接到資料庫: {db_host}:{db_port}/{db_name} 作為用戶: {db_user}")
        
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password,
        )
        logger.info("成功連接到資料庫")
        return connection
    except Error as e:
        logger.error(f"資料庫連接錯誤 (Error): {e}")
        return None
    except Exception as e:
        logger.exception(f"建立連接時發生未預期錯誤: {e}")
        return None

def check_connection(connection):
    if not connection or not connection.is_connected():
        logger.warning("檢查連接失敗：連接不存在或已斷開")
        return False
    try:
        db_Info = connection.server_info
        logger.debug(f"資料庫版本: {db_Info}") # Use f-string
        cursor = connection.cursor()
        cursor.execute("SELECT database();")
        record = cursor.fetchone()
        cursor.close()
        logger.info(f"你連接到的資料庫: {record}") # Use f-string
        return True
    except Error as e:
        logger.error(f"檢查連接時發生資料庫錯誤: {e}")
        return False
    except Exception as e:
        # print(f"檢查連接時發生未預期錯誤: {e}") # Remove this print
        logger.exception(f"檢查連接時發生未預期錯誤: {e}")
        return False

def save_events_to_db(connection, events):
    successful_inserts = 0
    cursor = None
    if not events:
        logger.info("沒有要儲存的資料")
        return
    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO events (school, title, title_simplified, link)
            VALUES (%s, %s, %s, %s)
        """
        
        for event in events:
            try:
                cursor.execute(insert_query, event)
                successful_inserts += 1
            except Error as e:
                if e.errno == 1062:
                    continue
                else:
                    logger.error(f"儲存資料時發生資料庫錯誤: {e}")
                    continue
        
        connection.commit()
        logger.info(f"成功儲存 {successful_inserts} 筆資料")
    except Error as e:
        logger.error(f"儲存資料時發生資料庫錯誤: {e}")
    except Exception as e:
        logger.exception(f"儲存資料時發生未預期的錯誤: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        logger.info("資料庫連接已關閉")