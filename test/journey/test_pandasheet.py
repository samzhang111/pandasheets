import json

import os
import pandas as pd
import pytest
from expects import *
from pandasheet.pandasheet import PandaSheet
from pandasheet.signin import get_sheets_client


@pytest.fixture
def logged_in_sheet(scope='session'):
    config_file_name = os.environ['TEST_CONFIG_FILE']

    with open(config_file_name) as config_file:
        config = json.load(config_file)

    gc = get_sheets_client(config)

    return gc.open('Test Sheet')


@pytest.mark.integration
class TestPandaSheetEndToEnd:
    def test_can_create_new_sheet_from_dataframe(self, logged_in_sheet):
        ps = PandaSheet(logged_in_sheet)

        df = pd.DataFrame({'a': range(5), 'b': range(5, 10)})
        ps.save_dataframe(df, 'test worksheet')

        new_worksheet = logged_in_sheet.worksheet('test worksheet')
        expect(new_worksheet.get_all_records()).to(equal(
            [{'a': 0, 'b': 5},
             {'a': 1, 'b': 6},
             {'a': 2, 'b': 7},
             {'a': 3, 'b': 8},
             {'a': 4, 'b': 9}]
        ))
        logged_in_sheet.client.del_worksheet(new_worksheet)

    def test_can_update_existing_sheet(self, logged_in_sheet):
        ps = PandaSheet(logged_in_sheet)

        df = pd.DataFrame({'a': range(5), 'b': range(5, 10)})
        ps.save_dataframe(df, 'test worksheet')

        df = pd.DataFrame({'a': range(5, 10), 'b': range(10, 15)})
        ps.save_dataframe(df, 'test worksheet')

        new_worksheet = logged_in_sheet.worksheet('test worksheet')
        expect(new_worksheet.get_all_records()).to(equal(
            [{'a': 5, 'b': 10},
             {'a': 6, 'b': 11},
             {'a': 7, 'b': 12},
             {'a': 8, 'b': 13},
             {'a': 9, 'b': 14}]
        ))

        logged_in_sheet.del_worksheet(new_worksheet)

    def test_can_load_existing_sheet_into_dataframe(self, logged_in_sheet):
        ps = PandaSheet(logged_in_sheet)
        df = pd.DataFrame({'a': range(5), 'b': range(5, 10)})

        ps.save_dataframe(df, 'test worksheet')

        received = ps.load('test worksheet')

        expect(df.to_dict()).to(equal(received.to_dict()))

        logged_in_sheet.del_worksheet(logged_in_sheet.worksheet('test worksheet'))