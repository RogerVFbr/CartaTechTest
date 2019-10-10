import sys
from datetime import date
import pandas as pd


class Validator:

    __data_source = None
    __date_filter = None

    @classmethod
    def get_data_source(cls):
        """
        Expose aqcuired data in a Pandas DataFrame form.
        :return: Pandas Dataframe
        """
        return cls.__data_source

    @classmethod
    def get_date_filter(cls):
        """
        Expose aqcuired date filter in a date form.
        :return: datetime.date
        """
        return cls.__date_filter

    @classmethod
    def validate(cls):
        """
        Initiate validation procedure and pre-validate parameter count.
        :return: boolean
        """
        if len(sys.argv) < 2 or len(sys.argv) > 3:
            print("Invalid parameter count. Please use: 'main.py <data_source_path>' or " +
                  "'main.py <data_source_path> <date_filter_YYYY-MM-DD>'")
            return False
        if cls.__validate_data_source() is False: return False
        if cls.__validate_date_filter() is False: return False
        return True


    @classmethod
    def __validate_data_source(cls):
        """
        Validate data source by attempting to use given path to build a dataframe.
        :return: boolean
        """
        try:
            cls.__data_source = pd.read_csv(sys.argv[1], parse_dates=[0])
        except FileNotFoundError:
            print(f"Data source not found at given path ('{sys.argv[1]}'). Please check for spelling mistakes.")
            return False
        except Exception as e:
            print(f"An error occurred while opening data source file: {e}")
            return False
        return True


    @classmethod
    def __validate_date_filter(cls):
        """
        Validate date filter by checking its existence and format.
        :return: boolean
        """
        if len(sys.argv) < 3:
            cls.__date_filter = date.today()
            return True

        invalid_syntax_msg = "Invalid date filter syntax. Please use 'YYYY-MM-DD'. Integers only. Example: 2019-02-02."

        try:
            year, month, day = tuple(sys.argv[2].split('-'))
        except:
            print(invalid_syntax_msg)
            return False

        if len(year) is not 4 or len(month) is not 2 or len(day) is not 2:
            print(invalid_syntax_msg)
            return False

        try:
            year = int(year)
            month = int(month)
            day = int(day)
        except:
            print(invalid_syntax_msg)
            return False

        cls.__date_filter = date(year, month, day)
        return True

