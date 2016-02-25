import pytest
from signin import get_sheets_client
import os
import json
import pandas as pd
from expects import *
from dfsheets import PandaSheet


@pytest.fixture
def logged_in_google_client():
    config_file_name = os.environ['TEST_CONFIG_FILE']

    with open(config_file_name) as config_file:
        config = json.load(config_file)

    return get_sheets_client(config)


class TestPandaSheets:
    def test_sheets_can_create_new_sheet_from_dataframe(self, logged_in_google_client):
        ps.save_dataframe(df, 'test worksheet')

        new_worksheet = test_spreadsheet.worksheets()[-1]
        expect(new_worksheet.title).to(equal('test worksheet'))

