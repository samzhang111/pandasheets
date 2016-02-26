import xml

from gspread import Cell
from mock import MagicMock
from test.helpers.fixtures import gspread_worksheet


class FakeCellElement(dict):
    text = ''


class ComparableCell(Cell):
    def __eq__(self, other):
        return self.value == other.value and self.row == other.row and self.col == other.col


def get_empty_cells(rows, cols):
    empty_cells = []
    for i in range(rows):
        for j in range(cols):
            element = make_element(i + 1, j + 1, 0)
            empty_cells.append(ComparableCell(gspread_worksheet, element))

    return empty_cells


def get_test_cells_like_df(df):
    cells = get_empty_cells(*df.shape)
    for cell in cells:
        row = cell.row - 2
        col = cell.col - 1

        if row == -1:
            value = df.columns[col]
        else:
            value = df.iloc[row, col]

        cell.value = value

    return cells


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