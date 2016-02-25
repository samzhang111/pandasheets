class PandaSheet:
    def __init__(self, gspread_sheet):
        self.gspread_sheet = gspread_sheet

    def save_dataframe(self, df, worksheet_title):
        new_worksheet = self.gspread_sheet.add_worksheet(worksheet_title,
                df.shape[0], df.shape[1])

        cells = self.get_all_cells(new_worksheet)

        for cell in cells:
            value = df.iloc[cell.row-1, cell.col-1]
            cell.value = value

        new_worksheet.update_cells(cells)

    def get_all_cells(self, worksheet):
        bottom_right = worksheet.get_addr_int(
                worksheet.row_count,
                worksheet.col_count)

        return worksheet.range('A1:%s' % bottom_right)
