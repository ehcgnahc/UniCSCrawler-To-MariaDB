def create_google_calendar_link(event_name, start_time, end_time, location, description):
    # 日期時間可能有問題 待處理
    google_calendar_url = "https://www.google.com/calendar/render?action=TEMPLATE"
    start_time_str = start_time.strftime("%Y%m%dT%H%M%S")
    end_time_str = end_time.strftime("%Y%m%dT%H%M%S")
    location_str = location.replace(" ", "+")
    description_str = description.replace(" ", "+")
    event_name_str = event_name.replace(" ", "+")
    google_calendar_link = (
        f"{google_calendar_url}"
        f"text={event_name_str}"
        f"&dates={start_time_str}/{end_time_str}"
        f"&location={location_str}"
        f"&details={description_str}"
        f"&sf=true&output=xml"
    )
    print(google_calendar_link)
    return google_calendar_link

def create_ios_calendar_link(event_name, start_time, end_time, location, description):
    # 要先建立.ics檔案 將其放在伺服器並提供下載連結 讓使用者點擊後可就會自動匯入行事曆
    return None