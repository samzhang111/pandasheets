import pandas as pd


class PandaSheet:
    def __init__(self, gspread_sheet):
        self.gspread_sheet = gspread_sheet

    def save_dataframe(self, df, worksheet_title):
        try:
            worksheet = self.gspread_sheet.add_worksheet(worksheet_title,
                                                         df.shape[0] + 1, df.shape[1])
        except AttributeError:
            worksheet = self.gspread_sheet.worksheet(worksheet_title)

        cells = self.get_all_cells(worksheet)

        for cell in cells:
            row = cell.row - 2
            col = cell.col - 1

            if row == -1:
                value = df.columns[col]
            else:
                value = df.iloc[row, col]

            cell.value = value

        worksheet.update_cells(cells)

    def get_all_cells(self, worksheet):
        return worksheet._fetch_cells()

    def load(self, worksheet_name, headers=False):
        worksheet = self.gspread_sheet.worksheet(worksheet_name)
        all_cells = self.get_all_cells(worksheet)

        shape = self._get_shape_of_sparse_cells(all_cells)
        df = pd.DataFrame(index=range(shape[0] - headers), columns=range(shape[1]))

        columns = {}
        for cell in all_cells:
            row = cell.row - 1 - headers
            col = cell.col - 1

            if row == -1:
                columns[col] = cell.value
            else:
                df.iloc[row, col] = self.convert_value(cell.value)

        if headers:
            df.rename(columns=columns, inplace=True)

        return df

    def convert_value(self, value):
        try:
            if int(float(value)) == float(value):
                return int(value)
            else:
                return float(value)
        except ValueError:
            return value

    def _get_shape_of_sparse_cells(self, cells):
        width = 0
        height = 0
        for cell in cells:
            if cell.col > height:
                height = cell.col
            if cell.row > width:
                width = cell.row

        return (width, height)

    def from_sparse_cell_list(self, cells):
        shape = self._get_shape_of_sparse_cells(cells)
        df = pd.DataFrame(index=range(shape[0]), columns=range(shape[1]))

        columns = {}
        for cell in cells:
            row = cell.row - 1
            col = cell.col - 1

            if row == -1:
                columns[col] = cell.value
            else:
                df.iloc[row, col] = self.convert_value(cell.value)

        return df

