import pytest

from pandasheet.pandaworksheet import PandaWorksheet
from tests.helpers.cell_helpers import get_test_cells_like_df
from tests.helpers.fixtures import pandaworksheet
import pandas as pd


class TestPandaWorksheet:

    @pytest.mark.parametrize('shape', [(5, 2)])
    def test_save_dataframe_updates_new_worksheet_with_same_dimensions(self, pandaworksheet):
        df = pd.DataFrame({'a': range(5), 'b': range(5)})
        pandaworksheet.save_dataframe(df)

        pandaworksheet.worksheet.update_cells.assert_called_with(
            get_test_cells_like_df(df, pandaworksheet.worksheet)
        )
