from oauth2client.service_account import ServiceAccountCredentials
import os
import gspread
import gspread_dataframe as gd


class ScrapperParent:
    def __init__(self):
        self.table_url = 'https://docs.google.com/spreadsheets/d/1QzayngI5uYi9BqfXS1fQFC_a3HXc7uio3Tuu-KT8b2U/'
        self.sheet_name = 'Market'
        self.google_creds = os.path.join(os.path.dirname(__file__), 'wsheet.json')

    def get_worksheet(self):
        """
        :param sheet_name: str
        :Return: Worksheet object with a given name
        """
        for try_count in range(10):
            try:
                scope = [
                    'https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive'
                ]
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    self.google_creds, scope)
                client = gspread.authorize(creds)
                worksheet = client.open_by_url(self.table_url).worksheet(self.sheet_name)
                return worksheet
            except Exception as e:
                    continue
        raise Exception("CANT CONNECT TO GSHEET")

    def write_to_sheet(self):
        wsh = self.get_worksheet()
        gd.set_with_dataframe(worksheet=wsh, dataframe=self.df, row=2,
                              resize=False, include_column_header=False)
