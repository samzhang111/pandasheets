import pytest
from gspread import Spreadsheet, Worksheet
from mock import MagicMock


@pytest.fixture
def gspread_sheet():
    return MagicMock(spec=Spreadsheet)


@pytest.fixture
def gspread_worksheet():
    return MagicMock(spec=Worksheet)