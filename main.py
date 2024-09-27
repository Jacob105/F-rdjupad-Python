import logging
import sqlite3
from api import fetch_data
from datacleaner import DataCleaner

# Configure logging for the entire pipeline
logging.basicConfig(
    filename='data_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main() -> None:
    """
    Main function to execute the data pipeline: fetch, clean, and save data.
    """
    conn = None
    try:
        # Fetch data using the API
        df = fetch_data()
        logging.info('Data fetched successfully')

        # Create a DataCleaner instance
        cleaner = DataCleaner(df)

        # Clean the data
        cleaned_data = cleaner.clean()

        # Save cleaned data to CSV 
        cleaned_data.to_csv('cleaned_data.csv', index=False)
        logging.info('Cleaned data saved to CSV')

        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('cleaned_data.db')
        logging.info('Connected to SQLite database')

        # Save cleaned data to the database
        cleaned_data.to_sql('demographic_data', conn, if_exists='replace', index=False)
        logging.info('Cleaned data saved to SQLite database table "demographic_data"')

    except sqlite3.Error as e:
        logging.error(f'SQL error: {e}')

    except Exception as e:
        logging.error(f'An error occurred: {e}')

    finally:
        if conn:
            conn.close()
            logging.info('SQLite database connection closed')

if __name__ == "__main__":
    main()
