import requests
from bs4 import BeautifulSoup
from .normalize_text import normalize_text
import logging
from urllib import parse

logger = logging.getLogger('main')

def get_events(site, headers):
    events = []
    try:
        response = requests.get(site['url'], headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_list = soup.select(site["selector"])

        for event in title_list:
            title = event.get("title", "").strip() or event.text.strip()
            title_simplified = normalize_text(title)
            link = parse.urljoin(site["url"], event.get("href", ""))
            events.append((site["school"], title, title_simplified, link))
    except requests.exceptions.Timeout as e:
        logger.error(f"請求 {site['school']} 超時: {e}")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"請求 {site['school']} 時發生錯誤: {e}")
        return []
    except Exception as e:
        logger.exception(f"解析 {site['school']} 時發生未預期錯誤: {e}")
        return []

    return events
