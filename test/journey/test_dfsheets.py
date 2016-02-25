import pytest
from signin import get_sheets_client
import os
import json
import pandas as pd
from expects import *
from dfsheets import PandaSheet


@pytest.fixture
def logged_in_sheet(request, scope='session'):
    config_file_name = os.environ['TEST_CONFIG_FILE']

    with open(config_file_name) as config_file:
        config = json.load(config_file)

    gc = get_sheets_client(config)

    return gc.open('Test Sheet')


class TestPandaSheets:
    def test_sheets_can_create_new_sheet_from_dataframe(self, logged_in_sheet):
        ps = PandaSheet(logged_in_sheet)

        df = pd.DataFrame({'a': range(5), 'b': range(5, 10)})
        ps.save_dataframe(df, 'test worksheet')

        new_worksheet = logged_in_sheet.worksheets()[-1]
        expect(new_worksheet.title).to(equal('test worksheet'))
        expect(new_worksheet.get_all_records()).to(equal(
            [{'0': 1, '5': 6},
             {'0': 2, '5': 7},
             {'0': 3, '5': 8},
             {'0': 4, '5': 9}]
        ))
        logged_in_sheet.client.del_worksheet(new_worksheet)

    def test_sheets_can_update_existing_sheet(self, logged_in_sheet):
        ps = PandaSheet(logged_in_sheet)

        df = pd.DataFrame({'a': range(5), 'b': range(5, 10)})
        ps.save_dataframe(df, 'test worksheet')

        df = pd.DataFrame({'a': range(5, 10), 'b': range(10, 15)})
        ps.save_dataframe(df, 'test worksheet')

        new_worksheet = logged_in_sheet.worksheets()[-1]

        expect(new_worksheet.title).to(equal('test worksheet'))
        expect(new_worksheet.get_all_records()).to(equal(
            [{'5': 6, '15': 11},
             {'5': 7, '15': 12},
             {'5': 8, '15': 13},
             {'5': 9, '15': 14}]
        ))

