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
        bottom_right = worksheet.get_addr_int(
            worksheet.row_count,
            worksheet.col_count)

        return worksheet.range('A1:%s' % bottom_right)

    def load(self, worksheet):
        records = self.gspread_sheet.worksheet(worksheet).get_all_records()
        return pd.DataFrame(records)