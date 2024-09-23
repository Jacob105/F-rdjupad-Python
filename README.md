Demographic Data Processing Pipeline

Overview:

This project fetches demographic data from Wikipedia, cleans the data, and stores it in a SQLite database. It includes a robust logging mechanism and a series of tests to ensure data integrity.

Table of Contents:
- Features
- Technologies Used
- Installation
- Usage
- Testing

Features:

- Fetch demographic data from the Swedish Wikipedia page.
- Clean the data to ensure consistency and accuracy.
- Save the cleaned data to a CSV file and an SQLite database.
- Logging throughout the pipeline for better traceability.
- Automated tests to verify functionality and data integrity.

Technologies Used:
- Python
- Pandas
- SQLite
- Requests
- BeautifulSoup
- Logging
- Pytest

Installation:
- Clone the repository in cmd: git clone https://github.com/Jacob105/F-rdjupad-Python.git
cd F-rdjupad-Python
- Install the required packages: pip install -r requirements.txt

Usage:
To run the data processing pipeline, execute: python main.py in the command prompt.

(This command fetches the data, cleans it, and saves it to both a CSV file (cleaned_data.csv) and an SQLite database (cleaned_data.db).)

Testing
To run the tests, use: pytest in the command prompt.

(This will execute all the tests defined in the test files and report any issues.)
