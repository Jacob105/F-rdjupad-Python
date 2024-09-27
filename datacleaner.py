import pandas as pd
import logging
import re
import math

class DataCleaner:
    def __init__(self, data) -> None:
        """
        Initializes the DataCleaner class with the input data.
        Args:
            data (pd.DataFrame): The DataFrame to clean.
        """
        self.data = data
        self.logger = logging.getLogger(__name__)

    def format_value(self, value):
        """
        Cleans and formats a string representing a numeric value.

        Args:
            value (str): The value to format.

        Returns:
            str: The formatted value, or the original if an error occurs.
        """
        try:
            # Ensure the value is a string
            if not isinstance(value, str):
                self.logger.warning(f'Value is not a string: {value}')
                return value

            # Remove any non-numeric characters except commas and dots
            cleaned_value = re.sub(r'[^\d,.]', '', value)
            self.logger.debug(f'Cleaned value (raw): {cleaned_value}')

            # Replace commas with dots for consistent decimal handling
            cleaned_value = cleaned_value.replace(',', '.')
            self.logger.debug(f'Value after replacing commas with dots: {cleaned_value}')

            # Convert cleaned value to float
            try:
                number = float(cleaned_value)
            except ValueError:
                self.logger.error(f'Failed to convert cleaned value to float: {cleaned_value}')
                return value

            # Use math.trunc() to remove decimal part
            truncated_number = math.trunc(number)
            self.logger.debug(f'Number after truncation: {truncated_number}')

            # Format the number with spaces as thousand separators
            formatted_value = f"{truncated_number:,}".replace(',', ' ')
            self.logger.debug(f'Formatted value: {formatted_value}')

            return formatted_value
        except Exception as e:
            # Log the error if necessary
            self.logger.error(f'Formatting error: {e} - Original value: {value}')
            return value

    def clean(self):
        """
        Cleans the DataFrame by formatting specific columns.

        Returns:
            pd.DataFrame: The cleaned DataFrame.
        """
        self.logger.info('Starting data cleaning process')
        # List of columns to clean
        columns_to_clean = ['Folkmängd', 'Födda', 'Döda', 'Befolkningsförändring']

        for col in columns_to_clean:
            if col in self.data.columns:
                self.logger.info(f'Cleaning column: {col}')
                # Convert column values to string to apply formatting
                self.data[col] = self.data[col].astype(str).apply(self.format_value)
                self.logger.info(f'Finished cleaning column: {col}')
            else:
                self.logger.warning(f'Column not found in DataFrame: {col}')

        self.logger.info('Data cleaning process completed')
        return self.data
