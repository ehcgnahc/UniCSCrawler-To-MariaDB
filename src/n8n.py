from dotenv import load_dotenv, find_dotenv
import requests
import logging
import time
import os

logger = logging.getLogger('main')

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    logger.info("找不到 .env 檔案，請確保它存在專案根目錄")

def title_filter(n8n_webhook_url, events):
    if not events:
        logger.info("No events to send to n8n")
        return []
    
    filtered_events = []
    
    header_name = os.getenv("N8N_HEADER_NAME")
    header_value = os.getenv("N8N_HEADER_VALUE")
    
    if not header_name or not header_value:
        # 未來可改為先暫時擱置直到問題修正並重新執行
        logger.error("N8N_HEADER_NAME 或 N8N_HEADER_VALUE 未在.env 檔案中設定")
        return []
    
    header = {
        'Content-Type': 'application/json',
        header_name: header_value,
    }
    
    for event in events:
        payload = {
            'title': event[2],
            'url': event[3],
            'school': event[0]
        }

        try:
            response = requests.post(n8n_webhook_url, headers=header, json=payload)
            response.raise_for_status()
            n8n_response = response.json()
            if n8n_response.get('event_type') == 'competition' or n8n_response.get('event_type') == 'internship' or n8n_response.get('event_type') == 'activities':
                event[2] = n8n_response.get('event_title')
                event.append(n8n_response.get('event_location'))
                event.append(n8n_response.get('event_info'))
                event.append(n8n_response.get('event_type'))
                filtered_events.append(event)
                logger.info(f"Event '{event[2]}' kept by n8n")
            elif n8n_response.get('event_type') == 'black_list':
                logger.info(f"Event '{event[2]}' black listed by n8n")
            elif n8n_response.get('event_type') == 'same':
                logger.info(f"Event '{event[2]}' is dupelicate")
            else:
                logger.info(f"Event '{event[2]}' filtered out by n8n")
            
            time.sleep(5)
        except requests.exceptions.Timeout:
            logger.warning(f"呼叫 n8n webhook 超時 (標題: {event[2]})")
        except requests.exceptions.RequestException as e:
            logger.error(f"呼叫 n8n webhook 失敗 (標題: {event[2]}): {e}")
        except ValueError:
            logger.error(f"解析 n8n webhook 的 JSON 回應失敗 (標題: {event[2]})")
        except Exception as e:
            logger.exception(f"處理 n8n 回應時發生未預期錯誤 (標題: {event[2]}): {e}")
        
    logger.info(f"共 {len(events)} 筆事件，經過 n8n 過濾後剩餘 {len(filtered_events)} 筆")
    return filtered_events