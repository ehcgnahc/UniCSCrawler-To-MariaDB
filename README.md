# UniCSCrawler To MariaDB

Web Crawling and Data Storage for Computer Science Department Information

## Project Description

UniCSCrawler To MariaDB is an automated web scraping application that collects announcements and event information from various university Computer Science/CSIE department websites in Taiwan. The collected data is normalized and stored in a MariaDB database for easy access and analysis.

## Project Structure

```
UniCSCrawler To MariaDB/
├── LICENSE                     # MIT License file
├── README.md                   # Project documentation
├── logging.ini                 # Logging configuration
├── requirements.txt            # Project dependencies
├── logs/                       # Log files directory
│   └── YYYY-MM-DD/             # Date-organized log folders
│       └── YYYY-MM-DD_HH-MM-SS.log # Timestamped log files
└── src/                        # Source code
    ├── __init__.py            
    ├── config.py               # Configuration settings
    ├── crawler.py              # Web scraping functionality
    ├── database_controller.py  # Database operations
    ├── main.py                 # Application entry point
    ├── normalize_text.py       # Text normalization utilities
    ├── setup_logging.py        # Logging setup
    └── target.py               # Target websites configuration
```

## Requirements

- Python 3.6+
- MariaDB/MySQL server
- Internet connection
- Environment variables configuration

Check the [installation notes](#installation) for more details on how to install the project.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/ehcgnahc/UniCSCrawler-To-MariaDB.git
   cd UniCSCrawler-To-MariaDB
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your database credentials:
   ```
   ADMIN_DB_HOST=your_host
   ADMIN_DB_PORT=your_database_port
   ADMIN_DB_NAME=your_database_name
   ADMIN_DB_USER=your_username
   ADMIN_DB_PASSWORD=your_password
   
   USER_DB_HOST=your_host
   USER_DB_PORT=your_database_port
   USER_DB_NAME=your_database_name
   USER_DB_USER=your_readonly_username
   USER_DB_PASSWORD=your_readonly_password
   ```
   **Note:** Currently, the application only uses the `ADMIN` credentials for writing data to the database. The `USER` credentials (intended for read-only access) are defined but not yet utilized in the current version.

4. Create a database table:
   ```sql
   CREATE TABLE `events` (
     `ID` int(11) NOT NULL AUTO_INCREMENT,
     `School` varchar(255) NOT NULL,
     `Title` varchar(255) NOT NULL,
     `Title_Simplified` varchar(255) NOT NULL,
     `Link` text NOT NULL,
     `Post_Date` datetime NOT NULL DEFAULT current_timestamp(),
     PRIMARY KEY (`ID`),
     UNIQUE KEY `Title` (`Title`),
     UNIQUE KEY `Title_Simplified` (`Title_Simplified`),
     UNIQUE KEY `uq_school_link` (`School`,`Link`) USING HASH
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
   ```

## Usage

Run the crawler with:

```
python -m src.main
```

The program will:
1. Connect to the MariaDB database
2. Crawl announcements from specified university CS/CSIE websites
3. Normalize and store the data in the database
4. Log all operations to files in the `logs` directory

To schedule regular crawls, you can use the `schedule` library (already imported) or set up a cron job.

## Logging Configuration

The project uses Python's logging module configured through `logging.ini`. Logs are organized by date in the `logs/` directory. Each log file is timestamped with the format `YYYY-MM-DD_HH-MM-SS.log`.

To customize logging behavior, edit the `logging.ini` file. The current configuration saves logs with different severity levels (INFO, WARNING, ERROR, etc.) to date-organized directories.

## Customization

You can customize the target websites by editing the `src/target.py` file:

```python
sites = [
    {"school": "SCHOOL_NAME", "url": "https://example.com", "selector": "css_selector_for_announcements"}
]
```

## Dependencies

The project relies on the following Python packages:
- `requests` - For making HTTP requests to university websites
- `beautifulsoup4` - For parsing HTML and extracting information
- `emoji` - For handling emoji characters in announcement texts
- `python-dotenv` - For loading environment variables from .env file
- `mysql-connector-python` - For connecting to MariaDB/MySQL database

## Useful Resources

- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library Documentation](https://docs.python-requests.org/)
- [MariaDB Documentation](https://mariadb.org/documentation/)
- [Python Logging Guide](https://docs.python.org/3/howto/logging.html)

## License

[MIT License](LICENSE)

## Contributors

- ehcgnahc - Initial work

## Acknowledgements

This project uses the following open-source libraries:
- [Requests](https://requests.readthedocs.io/) - HTTP library for Python
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Web scraping library
- [Emoji](https://github.com/carpedm20/emoji/) - Emoji support for Python
- [Python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) - MySQL/MariaDB database connector

Special thanks to:
- The developers of all libraries listed in `requirements.txt`
- The Computer Science departments of various universities for providing public information

Note: This project only collects publicly available information from university websites for educational purposes.