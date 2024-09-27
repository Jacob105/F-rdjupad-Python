import requests
import logging
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


# Use the logger without basicConfig
logger = logging.getLogger(__name__)

# Define constants for the API request
URL = 'https://sv.wikipedia.org/w/api.php'
PAGE = 'Sveriges_demografi'
HEADERS = {'user-agent': 'JBOT (jacob.anderssonds@hotmail.com)'}

def fetch_data():
    """
    Fetches population data from the Wikipedia API and returns a pandas DataFrame.

    Raises:
        ValueError: If the section or table is not found in the fetched data.
    Returns:
        pd.DataFrame: DataFrame containing demographic data.
    """
    try:
        # Fetch the page data and find the "Befolkningsstatistik sedan 1900" section
        params = {
            'action': 'parse',
            'page': PAGE,
            'format': 'json',
            'prop': 'sections'
        }

        response = requests.get(URL, headers=HEADERS, params=params)
        data = response.json()

        # Find the section ID for "Befolkningsstatistik sedan 1900"
        section_id = None
        for section in data['parse']['sections']:
            if section['line'] == 'Befolkningsstatistik sedan 1900':
                section_id = section['index']
                break

        if section_id:
            # Fetch the content of the section
            params = {
                'action': 'parse',
                'page': PAGE,
                'format': 'json',
                'section': section_id,
                'prop': 'text'
            }

            section_response = requests.get(URL, headers=HEADERS, params=params)
            section_data = section_response.json()

            # Parse the HTML content
            section_html = section_data['parse']['text']['*']
            soup = BeautifulSoup(section_html, 'html.parser')

            # Extract the first table from the section
            table = soup.find('table')

            if table:
                # Convert the table to a pandas DataFrame using StringIO
                df = pd.read_html(StringIO(str(table)))[0]

                # Select only the first five columns
                df = df.iloc[:, :5]
                df.columns = ['År', 'Folkmängd', 'Födda', 'Döda', 'Befolkningsförändring']

                logger.info('Data fetched and parsed successfully.')
                return df
            else:
                raise ValueError("No table found in the section.")
        else:
            raise ValueError("Section 'Befolkningsstatistik sedan 1900' not found.")
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        raise
