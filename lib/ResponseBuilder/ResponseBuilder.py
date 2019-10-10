import pandas as pd
import decimal as D
import simplejson as json
from datetime import date


class ResponseBuilder:

    __qnt = D.Decimal(10) ** -2

    @classmethod
    def build(cls, df: pd.DataFrame, datefilter: date):
        """
        Converts the dataframe build from the imported CSV to the desired JSON structure, filtering the results
        by the given date.
        :param df (pd.DataFrame): data source/
        :param datefilter (datetime.date): date filter.
        :return:
        """

        # Filter entries by date
        df = df.loc[df['INVESTMENT DATE'] <= pd.Timestamp(datefilter)]

        # Calculate sum of numeric columns
        sum = df.sum()

        # Build ownership dataframe
        ownership_stats = df.groupby(['INVESTOR']).sum()

        # Converts dataframe index to aditional column
        ownership_stats.reset_index(level=0, inplace=True)

        # Rename columns to required JSON standard
        ownership_stats.columns = ['investor', 'shares', 'cash_paid']

        # Calculate ownership column values
        ownership_stats['ownership'] = 100 * ownership_stats['shares'] / sum['SHARES PURCHASED']

        # Convert dataframe to list of dictionaries
        ownership_list = ownership_stats.to_dict('records')

        # Convert floating point values to Decimals as required (Dataframes don't support Decimals natively)
        for x in ownership_list:
            x['ownership'] = D.Decimal(x['ownership']).quantize(cls.__qnt)
            x['cash_paid'] = D.Decimal(x['cash_paid']).quantize(cls.__qnt)


        # Build response dictionary
        response = {
            "date": datefilter.strftime("%m/%d/%Y"),
            "cash_raised": D.Decimal(sum['CASH PAID']).quantize(cls.__qnt),
            "total_number_of_shares": int(sum['SHARES PURCHASED']),
            "ownership": ownership_list
        }

        # Convert to JSON and return
        return json.dumps(response, indent=4, sort_keys=True, use_decimal=True)