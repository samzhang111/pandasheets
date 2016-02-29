import xml

from gspread import Cell
from mock import MagicMock


class FakeCellElement(dict):
    text = ''


class ComparableCell(Cell):
    def __eq__(self, other):
        return self.value == other.value and self.row == other.row and self.col == other.col


def get_empty_cells(rows, cols, worksheet):
    empty_cells = []
    for i in range(rows):
        for j in range(cols):
            print(i, j)
            cell = make_cell(i + 1, j + 1, 0, worksheet)
            empty_cells.append(cell)

    return empty_cells

def get_empty_elements(rows, cols):
    empty_elements = []
    for i in range(rows):
        for j in range(cols):
            cell = make_element(i + 1, j + 1, 0)
            empty_elements.append(cell)

    return empty_elements

def get_test_cells_like_df(df, worksheet):
    cells = get_empty_cells(*df.shape, worksheet=worksheet)
    for cell in cells:
        row = cell.row - 2
        col = cell.col - 1

        if row == -1:
            value = df.columns[col]
        else:
            value = df.iloc[row, col]

        cell.value = value

    return cells

def make_cell(workbook, *args, **kwargs):
    return ComparableCell(workbook, make_element(*args, **kwargs))

def make_element(row, col, value, input_value=None, numeric_value=None):
    mock_element = MagicMock(spec=xml.etree.ElementTree.Element)
    found_element = FakeCellElement(
        row=row,
        col=col,
        input_value=input_value,
        numeric_value=numeric_value
    )
    found_element.text = value
    mock_element.col = col
    mock_element.row = row
    mock_element.value = value
    mock_element.find.return_value = found_element

    return mock_element