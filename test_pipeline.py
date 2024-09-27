import pytest
import sqlite3
import os
import pandas as pd
from api import fetch_data
from datacleaner import DataCleaner

@pytest.fixture
def raw_data():
    """Fixture to fetch raw data once for reuse in tests."""
    return fetch_data()

def test_fetch_data(raw_data):
    """Test to check if data is fetched correctly from the API."""
    assert isinstance(raw_data, pd.DataFrame), "The data should be a DataFrame."
    assert len(raw_data) > 0, "The DataFrame should not be empty."

def test_clean_data(raw_data):
    """Test to check if data is cleaned properly."""
    cleaner = DataCleaner(raw_data)
    cleaned_df = cleaner.clean()

    assert isinstance(cleaned_df, pd.DataFrame), "The cleaned data should be a DataFrame."
    assert 'Folkmängd' in cleaned_df.columns, "The column 'Folkmängd' should exist after cleaning."
    assert not cleaned_df['Folkmängd'].str.contains(r'[^\d\s]').any(), "The 'Folkmängd' column should only contain numeric values and spaces."

@pytest.fixture
def cleaned_data(raw_data):
    """Fixture to clean the data for use in the SQL test."""
    cleaner = DataCleaner(raw_data)
    return cleaner.clean()

def test_sql_insertion(cleaned_data):
    """Test to check if cleaned data is inserted into the SQLite database correctly."""
    # Create a test database connection
    conn = sqlite3.connect('test_cleaned_data.db')

    # Insert the cleaned data into the database
    cleaned_data.to_sql('demographic_data', conn, if_exists='replace', index=False)

    # Check if the table was created and contains data
    result = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='demographic_data'")
    assert result.fetchone() is not None, "The table 'demographic_data' should exist in the database."

    # Check if the data was inserted correctly
    result = conn.execute("SELECT COUNT(*) FROM demographic_data")
    count = result.fetchone()[0]
    assert count > 0, "The 'demographic_data' table should contain rows."

    # Close the connection and clean up the test database
    conn.close()
    os.remove('test_cleaned_data.db')
