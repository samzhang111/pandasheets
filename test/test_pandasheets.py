import pytest
from dfsheets import PandaSheet
from expects import *
import pandas as pd
from mock import MagicMock
from gspread.models import Worksheet, Spreadsheet, Cell
import xml


@pytest.fixture
def gspread_sheet():
    return MagicMock(spec=Spreadsheet)


@pytest.fixture
def gspread_worksheet():
    return MagicMock(spec=Worksheet)


class FakeCellElement(dict):
    text = ''


def get_empty_cells(rows, cols):
    empty_cells = []
    for i in range(rows):
        for j in range(cols):
            element = make_element(i+1, j+1, 0)
            empty_cells.append(Cell(gspread_worksheet, element))

    return empty_cells


def make_element(row, col, value, input_value=None, numeric_value=None):
    mock_element = MagicMock(spec=xml.etree.ElementTree.Element)
    found_element = FakeCellElement(
            row=row,
            col=col,
            input_value=input_value,
            numeric_value=numeric_value
            )
    found_element.text = value

    mock_element.find.return_value = found_element

    return mock_element


class TestPandaSheets:
    def test_save_dataframe_creates_new_worksheet_with_same_dimensions(self,
            gspread_sheet):

        panda_sheet = PandaSheet(gspread_sheet)
        df = pd.DataFrame({'a': range(5), 'b': range(5)})
        panda_sheet.save_dataframe(df, 'name')

        gspread_sheet.add_worksheet.assert_called_with('name', 6, 2)

    def test_save_dataframe_updates_new_worksheet_with_data_from_dataframe(self,
            gspread_sheet, gspread_worksheet):

        df = pd.DataFrame({'a': range(5), 'b': range(5)})
        empty_cells = get_empty_cells(*df.shape)

        gspread_worksheet.range.return_value = empty_cells

        gspread_sheet.add_worksheet.return_value = gspread_worksheet

        panda_sheet = PandaSheet(gspread_sheet)
        panda_sheet.save_dataframe(df, 'name')

        for cell in empty_cells:
            cell.value = df.iloc[cell.row-1, cell.col-1]

        gspread_worksheet.update_cells.assert_called_with(empty_cells)

    def test_save_dataframe_updates_existing_worksheet_with_data(self,
            gspread_sheet, gspread_worksheet):
        df = pd.DataFrame({'a': range(5), 'b': range(5)})
        gspread_sheet.add_worksheet.side_effect = AttributeError()

        panda_sheet = PandaSheet(gspread_sheet)
        panda_sheet.save_dataframe(df, 'name')


