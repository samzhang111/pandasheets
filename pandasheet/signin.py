from oauth2client.client import SignedJwtAssertionCredentials
import json
import gspread
import os
import sys

from pandasheet.pandasheet import PandaSheet


def get_sheets_client(config):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(config['client_email'], config['private_key'].encode(), scope)
    return gspread.authorize(credentials)

def fire_up_pandasheets(config, spreadsheet):
    gc = get_sheets_client(config)
    sheet = gc.open(spreadsheet)
    ps = PandaSheet(sheet)
    return ps

if __name__ == '__main__':
    config = json.load(open(os.environ['TEST_CONFIG_FILE']))
    ps = fire_up_pandasheets(config, sys.argv[1])

