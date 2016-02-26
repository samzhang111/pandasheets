from oauth2client.client import SignedJwtAssertionCredentials
import json
import gspread
import os


def get_sheets_client(config):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(config['client_email'], config['private_key'].encode(), scope)
    return gspread.authorize(credentials)

if __name__ == '__main__':
    config = json.load(open(os.environ['TEST_CONFIG_FILE']))
    gc = get_sheets_client(config)
