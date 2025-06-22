# UniCSCrawler To MariaDB

**自動化網頁爬蟲系統** - 收集台灣各大學資訊工程系公告並整合到 MariaDB 資料庫

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Database](https://img.shields.io/badge/Database-MariaDB%2FMySQL-orange.svg)](https://mariadb.org/)

## 🚀 專案概述

UniCSCrawler To MariaDB 是一個智慧型網頁爬蟲應用程式，專門收集台灣各大學資訊工程系的公告和活動資訊。透過整合 N8N 工作流程，系統能夠自動過濾、分類和標準化資料，並將結果儲存到 MariaDB 資料庫中。

### 🎯 主要功能

- **多大學支援**: 同時爬取多所知名大學的資訊工程系網站
- **智慧過濾**: 整合 N8N 進行內容分類（競賽、實習、活動等）
- **資料標準化**: 自動清理和正規化文字內容
- **重複檢測**: 防止重複資料進入資料庫
- **錯誤處理**: 完整的網路和資料庫錯誤處理機制
- **日誌記錄**: 詳細的操作日誌，按日期分類儲存

### 🏫 支援的大學

| 學校代碼 | 學校名稱 | 系所 |
|---------|---------|------|
| NYUST | 雲林科技大學 | 資訊工程系 |
| NTU | 國立台灣大學 | 資訊工程學系 |
| NCKU | 國立成功大學 | 資訊工程學系 |
| NTHU | 國立清華大學 | 資訊工程學系 |
| NTUT | 國立台北科技大學 | 資訊工程系 |
| NCU | 國立中央大學 | 資訊工程學系 |

## 📁 專案結構

```
UniCSCrawler To MariaDB/
├── 📄 LICENSE                     # MIT 開源授權
├── 📄 README.md                   # 專案說明文件
├── ⚙️ logging.ini                 # 日誌配置檔案
├── 📄 requirements.txt            # Python 依賴套件
├── 🗄️ init.sql                   # 資料庫初始化腳本
├── 📁 logs/                       # 日誌檔案目錄
│   └── 📁 YYYY-MM-DD/             # 按日期分類的日誌資料夾
│       └── 📄 YYYY-MM-DD_HH-MM-SS.log # 時間戳記日誌檔案
├── 📁 src/                        # 主要程式碼
│   ├── 🐍 __init__.py            
│   ├── ⚙️ config.py               # 配置設定
│   ├── 🕷️ crawler.py              # 網頁爬蟲功能
│   ├── 🗄️ database_controller.py  # 資料庫操作
│   ├── 🚀 main.py                 # 應用程式入口
│   ├── 🔗 n8n.py                  # N8N 整合模組
│   ├── 🎯 target.py               # 目標網站配置
│   └── 📁 _utils/                 # 工具模組
│       ├── 🔧 normalize_text.py   # 文字標準化
│       └── 📋 setup_logging.py    # 日誌設定
└── 📁 tests/                      # 測試相關檔案
    ├── 🧪 show_db.py              # 資料庫查看工具
    └── 🧪 test_show.py            # 測試輔助函數
```

## 🛠️ 系統需求

- **Python**: 3.8+ (建議使用 3.9 或更新版本)
- **資料庫**: MariaDB 10.5+ 或 MySQL 8.0+
- **網路**: 穩定的網際網路連線
- **作業系統**: Windows, macOS, Linux
- **記憶體**: 至少 512MB 可用記憶體

## 📦 安裝說明

### 1. 複製專案

```bash
git clone https://github.com/ehcgnahc/UniCSCrawler-To-MariaDB.git
cd UniCSCrawler-To-MariaDB
```

### 2. 建立虛擬環境 (建議)

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 4. 環境變數配置

在專案根目錄建立 `.env` 檔案：

```env
# 資料庫配置 (Admin 權限 - 用於寫入資料)
ADMIN_DB_HOST=localhost
ADMIN_DB_PORT=3306
ADMIN_DB_NAME=your_database_name
ADMIN_DB_USER=your_admin_username
ADMIN_DB_PASSWORD=your_admin_password

# 資料庫配置 (User 權限 - 預留給未來唯讀功能)
USER_DB_HOST=localhost
USER_DB_PORT=3306
USER_DB_NAME=your_database_name
USER_DB_USER=your_readonly_username
USER_DB_PASSWORD=your_readonly_password

# N8N Webhook 配置
N8N_WEBHOOK_URL=http://localhost:5678/webhook/TitleFilter
N8N_HEADER_NAME=your_header_name
N8N_HEADER_VALUE=your_header_value
```

> **注意**: 目前版本主要使用 `ADMIN` 權限進行資料寫入，`USER` 權限為未來功能預留。

### 5. 資料庫初始化

```sql
-- 建立資料庫
CREATE DATABASE IF NOT EXISTS your_database_name;
USE your_database_name;

-- 建立事件資料表
CREATE TABLE `events` (
   `ID` int(11) NOT NULL AUTO_INCREMENT,
   `School` varchar(255) NOT NULL COMMENT '學校代碼',
   `Title` varchar(255) NOT NULL COMMENT '原始標題',
   `Title_Simplified` varchar(255) NOT NULL COMMENT '標準化標題',
   `Link` text NOT NULL COMMENT '公告連結',
   `Post_Date` datetime NOT NULL DEFAULT current_timestamp() COMMENT '發布時間',
   `Location` varchar(255) DEFAULT NULL COMMENT '活動地點',
   `Info` varchar(255) DEFAULT NULL COMMENT '活動資訊',
   `Type` varchar(255) DEFAULT NULL COMMENT '活動類型',
   PRIMARY KEY (`ID`),
   UNIQUE KEY `Title` (`Title`),
   UNIQUE KEY `Title_Simplified` (`Title_Simplified`),
   UNIQUE KEY `uq_school_link` (`School`,`Link`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='大學資訊工程系公告事件資料表';
```

或者直接使用提供的初始化腳本：

```bash
mysql -u your_username -p < init.sql
```

## 🚀 使用方法

### 基本執行

```bash
# 在專案根目錄執行
python -m src.main
```

### 執行流程

系統執行時會按照以下順序進行：

1. **🔗 資料庫連線** - 連接到 MariaDB/MySQL 資料庫
2. **🕷️ 網站爬取** - 依序爬取各大學的公告頁面
3. **🤖 智慧過濾** - 透過 N8N webhook 進行內容分析和分類
4. **💾 資料儲存** - 將通過過濾的資料存入資料庫
5. **📋 日誌記錄** - 所有操作記錄保存到 `logs/` 目錄

### 查看資料庫內容

使用提供的測試工具查看已收集的資料：

```bash
python tests/show_db.py
```

## 📊 日誌系統

### 日誌配置

專案使用 Python 的 `logging` 模組，配置檔案為 `logging.ini`：

- **控制台輸出**: INFO 等級以上的訊息
- **檔案記錄**: 詳細的操作日誌
- **分類儲存**: 按日期組織，格式為 `logs/YYYY-MM-DD/YYYY-MM-DD_HH-MM-SS.log`

### 日誌等級

- **INFO**: 一般操作資訊（如連線成功、資料數量等）
- **WARNING**: 警告訊息（如網路逾時、跳過某網站等）
- **ERROR**: 錯誤訊息（如資料庫錯誤、請求失敗等）
- **EXCEPTION**: 詳細的例外資訊

### 自訂日誌配置

編輯 `logging.ini` 檔案以客製化日誌行為：

```ini
[logger_main]
level=DEBUG  # 改為 DEBUG 可獲得更詳細的資訊
handlers=consoleHandler,fileHandler
```

## ⚙️ 自訂配置

### 新增目標網站

編輯 `src/target.py` 檔案以新增或修改要爬取的網站：

```python
sites = [
    {
        "school": "學校代碼",  # 例如: "NTUST"
        "url": "公告頁面網址",  # 例如: "https://example.edu.tw/announcements"
        "selector": "CSS選擇器"  # 例如: ".announcement-title a"
    },
    # 新增更多網站...
]
```

### CSS 選擇器說明

CSS 選擇器用於指定要提取的公告連結元素：

- `.class-name a` - 選擇具有特定 class 的元素內的連結
- `#id-name a` - 選擇具有特定 ID 的元素內的連結
- `a[title]` - 選擇具有 title 屬性的連結
- `.list-item .title a` - 選擇嵌套結構中的連結

### N8N 整合配置

N8N webhook 用於智慧過濾和分類爬取的內容：

1. **設定 N8N workflow**
   - 建立接收 webhook 的節點
   - 實作標題分析邏輯
   - 回傳分類結果

2. **回應格式**
   ```json
   {
     "event_type": "competition|internship|activities|black_list|same",
     "event_title": "處理後的標題",
     "event_location": "活動地點",
     "event_info": "活動資訊"
   }
   ```

3. **事件類型說明**
   - `competition`: 競賽活動
   - `internship`: 實習機會  
   - `activities`: 一般活動
   - `black_list`: 黑名單（不儲存）
   - `same`: 重複內容（不儲存）

## 📋 技術規格

### 依賴套件詳情

| 套件名稱 | 版本 | 用途 |
|---------|------|------|
| requests | 2.32.3 | HTTP 請求處理 |
| beautifulsoup4 | 4.12.3 | HTML 解析和資料提取 |
| emoji | 2.12.1 | emoji 字元處理和移除 |
| python-dotenv | 1.0.1 | 環境變數載入 |
| mysql-connector-python | 9.0.0 | MySQL/MariaDB 資料庫連接 |
| schedule | 1.2.2 | 定時任務排程 (可選) |

### 資料庫結構

#### events 資料表

| 欄位名稱 | 資料型態 | 說明 | 約束 |
|---------|---------|------|------|
| ID | int(11) | 主鍵，自動遞增 | PRIMARY KEY |
| School | varchar(255) | 學校代碼 | NOT NULL |
| Title | varchar(255) | 原始標題 | NOT NULL, UNIQUE |
| Title_Simplified | varchar(255) | 標準化標題 | NOT NULL, UNIQUE |
| Link | text | 公告連結 | NOT NULL |
| Post_Date | datetime | 發布時間 | DEFAULT current_timestamp() |
| Location | varchar(255) | 活動地點 | NULL |
| Info | varchar(255) | 活動資訊 | NULL |
| Type | varchar(255) | 活動類型 | NULL |

#### 唯一鍵約束

- `uq_school_link`: 防止同一學校的重複連結
- `Title`: 防止重複標題
- `Title_Simplified`: 防止標準化後的重複標題

### 文字標準化處理

`normalize_text()` 函數執行以下操作：

1. **移除空白字元**: 空格、換行、Tab 等
2. **轉換大小寫**: 統一轉為大寫
3. **移除特殊字元**: 底線、控制字元等
4. **處理 Markdown**: 移除粗體、斜體標記
5. **移除 emoji**: 清除所有 emoji 字元
6. **Unicode 正規化**: 統一字元編碼格式

## 🔧 故障排除

### 常見問題

#### 1. 資料庫連線失敗

**錯誤訊息**: `資料庫連接錯誤 (Error)`

**解決方法**:
- 檢查 `.env` 檔案中的資料庫配置
- 確認 MariaDB/MySQL 服務正在運行
- 驗證使用者權限和密碼正確性
- 檢查防火牆設定

#### 2. 網站爬取失敗

**錯誤訊息**: `請求 XXX 時發生網路錯誤`

**解決方法**:
- 檢查網路連線狀態
- 確認目標網站可正常訪問
- 調整 `crawler.py` 中的 timeout 設定
- 檢查 User-Agent 是否被封鎖

#### 3. N8N Webhook 失敗

**錯誤訊息**: `呼叫 n8n webhook 失敗`

**解決方法**:
- 確認 N8N 服務正在運行
- 檢查 `N8N_WEBHOOK_URL` 配置
- 驗證 header 認證資訊
- 確認 N8N workflow 正確設定

#### 4. 日誌檔案權限問題

**錯誤訊息**: `Permission denied`

**解決方法**:
- 確保對 `logs/` 目錄有寫入權限
- 在 Windows 上以管理員身分執行
- 在 Linux/macOS 上使用 `chmod` 調整權限

### 偵錯模式

啟用詳細日誌以獲得更多除錯資訊：

```python
# 在 logging.ini 中設定
[logger_main]
level=DEBUG
```

### 測試連線

使用以下指令測試各個組件：

```bash
# 測試資料庫連線
python -c "from src.database_controller import connect_to_maria_db; print('連線成功' if connect_to_maria_db('admin') else '連線失敗')"

# 測試單一網站爬取
python -c "from src.crawler import get_events; from src.target import sites; from src.config import headers; print(len(get_events(sites[0], headers)))"

# 查看資料庫內容
python tests/show_db.py
```

## 📚 參考資源

### 官方文檔

- [Beautiful Soup 4 文檔](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML 解析
- [Requests 文檔](https://docs.python-requests.org/) - HTTP 請求庫
- [MariaDB 文檔](https://mariadb.org/documentation/) - 資料庫操作
- [Python Logging 指南](https://docs.python.org/3/howto/logging.html) - 日誌系統
- [N8N 文檔](https://docs.n8n.io/) - 工作流程自動化

### 相關工具

- [VS Code](https://code.visualstudio.com/) - 推薦的開發環境
- [HeidiSQL](https://www.heidisql.com/) - MariaDB/MySQL 管理工具
- [Postman](https://www.postman.com/) - API 測試工具
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/) - 網頁除錯和 CSS 選擇器測試

### 學習資源

- [Python 網頁爬蟲教學](https://realpython.com/beautiful-soup-web-scraper-python/)
- [MySQL/MariaDB 教學](https://www.mysqltutorial.org/)
- [正規表達式學習](https://regex101.com/)
- [CSS 選擇器參考](https://www.w3schools.com/cssref/css_selectors.asp)

## 📄 授權條款

本專案採用 [MIT License](LICENSE) 開源授權。

```
MIT License

Copyright (c) 2025 ehcgnahc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👥 貢獻者

- **ehcgnahc** - 初始開發和維護

### 如何貢獻

我們歡迎社群的貢獻！以下是參與方式：

1. **Fork** 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 **Pull Request**

### 貢獻指南

- 遵循現有的程式碼風格
- 為新功能添加適當的測試
- 更新相關文檔
- 確保所有測試通過

## 🙏 致謝

### 開源套件

本專案使用了以下優秀的開源套件：

- [**Requests**](https://requests.readthedocs.io/) - Kenneth Reitz 開發的 HTTP 庫
- [**Beautiful Soup**](https://www.crummy.com/software/BeautifulSoup/) - Leonard Richardson 開發的網頁解析庫
- [**Emoji**](https://github.com/carpedm20/emoji/) - carpedm20 開發的 emoji 處理庫
- [**Python-dotenv**](https://github.com/theskumar/python-dotenv) - theskumar 開發的環境變數管理工具
- [**mysql-connector-python**](https://dev.mysql.com/doc/connector-python/en/) - Oracle 開發的 MySQL 連接器

### 特別感謝

- **各大學資訊工程系** - 提供公開的公告資訊
- **開源社群** - 提供強大的開發工具和資源
- **Python 社群** - 持續改善 Python 生態系統

### 免責聲明

- 本專案僅收集各大學網站上的**公開資訊**
- 使用目的限於**教育和研究用途**
- 請遵守各網站的使用條款和 robots.txt 規範
- 不建議過於頻繁的請求以免對目標網站造成負擔

---

<div align="center">

**⭐ 如果這個專案對您有幫助，請考慮給個星星支持！ ⭐**

[![GitHub stars](https://img.shields.io/github/stars/ehcgnahc/UniCSCrawler-To-MariaDB.svg?style=social&label=Star)](https://github.com/ehcgnahc/UniCSCrawler-To-MariaDB)

</div>