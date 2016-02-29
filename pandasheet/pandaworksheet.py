import gspread
from gspread import Cell


class PandaWorksheet:

    def __init__(self, worksheet, CellClass=Cell):
        self.worksheet = worksheet
        self.CellClass = CellClass

    def save_dataframe(self, df):

        cells = self.get_all_cells()

        for cell in cells:
            row = cell.row - 2
            col = cell.col - 1

            try:
                if row == -1:
                    value = df.columns[col]
                else:
                    value = df.iloc[row, col]
            except IndexError:
                continue

            cell.value = value

        self.worksheet.update_cells(cells)

    def get_all_cells(self):
        cell_feed = self.get_cell_feed()
        return [self.CellClass(self.worksheet, elem) for elem in cell_feed]

    def get_cell_feed(self):
        return self.worksheet.client.get_cells_feed(
            self.worksheet,
            params={'return-empty': 'true'}
        ).findall(gspread.ns._ns('entry'))
