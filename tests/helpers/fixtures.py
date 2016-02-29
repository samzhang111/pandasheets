import json

import os

import gspread
import pytest
from gspread import Spreadsheet, Worksheet, WorksheetNotFound
from mock import MagicMock
from pandasheet.pandasheet import PandaSheet
from pandasheet.pandaworksheet import PandaWorksheet
from pandasheet.signin import get_sheets_client
from tests.helpers.cell_helpers import get_empty_cells, make_cell, make_element, ComparableCell, get_empty_elements
import pandas as pd


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
def fake_cells(gspread_worksheet):
    return get_empty_cells(5, 5, gspread_worksheet)

@pytest.fixture
def gspread_worksheet(shape):
    mock_worksheet = MagicMock(spec=Worksheet)
    empty_elements = get_empty_cells(shape[0], shape[1], mock_worksheet)

    mock_worksheet.client = MagicMock(spec=gspread.Client)
    mock_worksheet.client.get_cells_feed.return_value = empty_elements
    return mock_worksheet


@pytest.fixture
def pandasheet(gspread_sheet):
    return PandaSheet(gspread_sheet)

@pytest.fixture
def pandaworksheet(shape):
    mock_worksheet = MagicMock(spec=Worksheet)
    empty_elements = get_empty_elements(shape[0], shape[1])

    pw = PandaWorksheet(mock_worksheet, CellClass=ComparableCell)

    pw.get_cell_feed = lambda: empty_elements

    return pw
