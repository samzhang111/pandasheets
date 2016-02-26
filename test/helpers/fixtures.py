import json

import os

import pytest
from gspread import Spreadsheet, Worksheet, WorksheetNotFound
from mock import MagicMock
from pandasheet.pandasheet import PandaSheet
from pandasheet.signin import get_sheets_client


@pytest.fixture
def logged_in_sheet(scope='session'):
    config_file_name = os.environ['TEST_CONFIG_FILE']

    with open(config_file_name) as config_file:
        config = json.load(config_file)

    gc = get_sheets_client(config)

    return gc.open('Test Sheet')


@pytest.fixture
def test_worksheet(logged_in_sheet, request):
    try:
        logged_in_sheet.del_worksheet(logged_in_sheet.worksheet('test worksheet'))
    except WorksheetNotFound:
        pass

    def fin():
        logged_in_sheet.del_worksheet(logged_in_sheet.worksheet('test worksheet'))

    request.addfinalizer(fin)
    return test_worksheet


@pytest.fixture
def gspread_sheet():
    return MagicMock(spec=Spreadsheet)


@pytest.fixture
def gspread_worksheet():
    return MagicMock(spec=Worksheet)

@pytest.fixture
def pandasheet(gspread_sheet):
    return PandaSheet(gspread_sheet)