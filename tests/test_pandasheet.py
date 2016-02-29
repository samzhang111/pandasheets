import pandas as pd
import pytest
from expects import equal
from expects import expect
from numpy import nan
from pandasheet.pandasheet import PandaSheet
from tests.helpers.cell_helpers import get_test_cells_like_df, make_element
from tests.helpers.fixtures import gspread_sheet, gspread_worksheet, pandasheet
from tests.helpers.matchers import numpy_array_equal


class TestPandaSheet:
    def test_save_dataframe_creates_new_worksheet_with_same_dimensions(self, gspread_sheet):
        panda_sheet = PandaSheet(gspread_sheet)
        df = pd.DataFrame({'a': range(5), 'b': range(5)})
        panda_sheet.save_dataframe(df, 'name')

        gspread_sheet.add_worksheet.assert_called_with('name', 6, 2)

    def test_save_dataframe_updates_existing_worksheet_with_data(self, gspread_sheet, gspread_worksheet):
        df = pd.DataFrame({'a': range(5), 'b': range(5)})
        gspread_sheet.add_worksheet.side_effect = AttributeError()
        gspread_sheet.worksheet.return_value = gspread_worksheet
        gspread_worksheet._fetch_cells.return_value = make_element(2, 1, 'hello')

        panda_sheet = PandaSheet(gspread_sheet)
        panda_sheet.save_dataframe(df, 'name')

        gspread_worksheet.update_cells.assert_called_with(make_element(3, 3, 1))

    @pytest.mark.xfail
    def test_load_worksheet_pulls_into_dataframe(self, gspread_sheet, gspread_worksheet):
        gspread_worksheet.get_all_records.return_value = [{'b': 5, 'a': 0},
                                                          {'b': 6, 'a': 1},
                                                          {'b': 7, 'a': 2},
                                                          {'b': 8, 'a': 3},
                                                          {'b': 9, 'a': 4}]
        gspread_sheet.worksheet.return_value = gspread_worksheet

        panda_sheet = PandaSheet(gspread_sheet)
        df = panda_sheet.load('sheet name', headers=True)

        expect(df.to_dict()).to(equal({
            'b': {0: 5, 1: 6, 2: 7, 3: 8, 4: 9},
            'a': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
        }))

    def test_attempts_to_convert_numerical_values(self, pandasheet):
        expect(pandasheet.convert_value('1')).to(equal(1))
        expect(pandasheet.convert_value('1.2')).to(equal(1.2))
        expect(pandasheet.convert_value('a')).to(equal('a'))

    def test_converts_sparse_cell_list_to_dataframe(self, pandasheet):
        cell = make_element(3, 3, 'hello')
        df = pandasheet.from_sparse_cell_list([cell])

        expect(df.to_records().tolist()).to(numpy_array_equal(
            [(0, nan, nan, nan),
             (1, nan, nan, nan),
             (2, nan, nan, 'hello')]
        ))

        expect(df.shape).to(equal((3, 3)))
        expect(df.ix[2, 2]).to(equal('hello'))

