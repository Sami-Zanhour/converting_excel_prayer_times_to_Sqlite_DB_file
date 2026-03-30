# converting_excel_prayer_times_to_Sqlite_DB_file
Converting Prayer Times Excel Sheet to SQLite file DB
# 🕌 Prayer Times Excel-to-SQLite Converter

Converting Prayer Times Excel Sheet to SQLite file DB.

A professional Python desktop application that automates the migration of prayer time schedules from Microsoft Excel (.xlsx) files into optimized SQLite databases.

## 📝 What This Project Does
This tool is designed for developers and mosque administrators who need to convert manual Excel schedules into a structured database format for mobile apps, websites, or digital displays.

### Key Features:
* **Graphical User Interface (GUI):** A simple window built with Tkinter for easy file selection and database naming.
* **Smart Time Normalization:** Automatically fixes inconsistent time formats (e.g., converts 6:35 to 06:35). Strips unnecessary seconds or date information from Excel time objects.
* **Data Integrity:**
    * **Auto-ID:** Automatically generates a unique Primary Key (id) for every row.
    * **Duplicate Prevention:** Creates a Unique Composite Index on (month, day) to ensure no date is entered twice.
    * **Data Cleaning:** Automatically handles accidental spaces or inconsistent capitalization in Excel headers (e.g., " Fajr " -> "fajr").
* **High Performance:** Includes database indexing for near-instant query speeds.

## 🚀 How to Run

### 1. Prerequisites
You need Python 3.11+ installed. You will also need the `pandas` and `openpyxl` libraries to handle the Excel data.

Install the requirements via terminal:
```bash
pip install pandas openpyxl
