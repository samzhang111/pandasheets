import json

import pandas as pd
import pytest
from expects import *
from pandasheet.pandasheet import PandaSheet
from tests.helpers.fixtures import logged_in_sheet, test_worksheet


@pytest.mark.integration
class TestPandaSheetEndToEnd:
    def test_can_create_new_sheet_from_dataframe(self, logged_in_sheet, test_worksheet):
        ps = PandaSheet(logged_in_sheet)

        df = pd.DataFrame({'a': range(5), 'b': range(5, 10)})
        ps.save_dataframe(df, 'test worksheet')

        new_worksheet = logged_in_sheet.worksheet('test worksheet')
        expect(new_worksheet.get_all_records()).to(equal(
            [{'a': 0, 'b': 5},
             {'a': 1, 'b': 6},
             {'a': 2, 'b': 7},
             {'a': 3, 'b': 8},
             {'a': 4, 'b': 9}]
        ))

    def test_can_update_existing_sheet(self, logged_in_sheet, test_worksheet):
        ps = PandaSheet(logged_in_sheet)

        df = pd.DataFrame({'a': range(5), 'b': range(5, 10)})
        ps.save_dataframe(df, 'test worksheet')

        df = pd.DataFrame({'a': range(5, 10), 'b': range(10, 15)})
        ps.save_dataframe(df, 'test worksheet')

        new_worksheet = logged_in_sheet.worksheet('test worksheet')
        expect(new_worksheet.get_all_records()).to(equal(
            [{'a': 5, 'b': 10},
             {'a': 6, 'b': 11},
             {'a': 7, 'b': 12},
             {'a': 8, 'b': 13},
             {'a': 9, 'b': 14}]
        ))

    def test_loads_correct_shape_of_sparse_sheets(self, logged_in_sheet, test_worksheet):
        logged_in_sheet.add_worksheet('test worksheet', 3, 3)
        ps = PandaSheet(logged_in_sheet)
        df = ps.load('test worksheet')
        expect(df.shape).to(equal((3, 3)))

    def test_loads_optional_header_from_first_row(self, logged_in_sheet, test_worksheet):
        logged_in_sheet.add_worksheet('test worksheet', 3, 3)
        worksheet = logged_in_sheet.worksheet('test worksheet')

        worksheet.update_cell(1, 1, 'z')
        worksheet.update_cell(1, 2, 'y')
        worksheet.update_cell(1, 3, 'x')

        ps = PandaSheet(logged_in_sheet)
        df = ps.load('test worksheet', headers=True)

        expect(df.shape).to(equal((2, 3)))
        expect(list(df.columns)).to(equal(['z', 'y', 'x']))

    def test_can_load_existing_sheet_into_dataframe(self, logged_in_sheet, test_worksheet):
        ps = PandaSheet(logged_in_sheet)
        df = pd.DataFrame({'a': range(5), 'b': ['a', 'b', 'c', 'd', 'e']})

        ps.save_dataframe(df, 'test worksheet')

        received = ps.load('test worksheet', headers=True)

        expect(df.to_dict()).to(equal(received.to_dict()))
