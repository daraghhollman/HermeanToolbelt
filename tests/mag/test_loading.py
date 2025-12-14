import math
import unittest
from pathlib import Path

from sunpy.time import TimeRange

from hermpy.mag import load_between_dates


class Test_Loading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data_dir = Path("./tests/data/")

    def test_single_file_loading(self):
        """
        Test if we can load a file of data
        """

        data = load_between_dates(
            self.test_data_dir,
            TimeRange("2011-04-23 00:00", "2011-04-23 00:01"),
            average=None,  # Testing full res data
            aberrate=False,  # We must implement testing of aberration. We would need the spice kernels which makes things tricky
        )

        # Check length is correct
        # This file was shortened to the first 10 rows manually
        assert len(data) == 10

        # Just check the first row
        r = data.iloc[0]

        # Check position is correct
        assert math.isclose(r["X MSM (radii)"], 0.986832, abs_tol=0.00001)

        # Check position was converted from MSO to MSM
        assert math.isclose(r["Z MSM (radii)"], -6.504103, abs_tol=0.00001)

        # Check MAG is correct
        assert math.isclose(r["Bx"], -7.179, abs_tol=0.001)

        # This data is missing, and should throw an error
        with self.assertRaises(FileNotFoundError):
            load_between_dates(
                self.test_data_dir,
                TimeRange("2011-06-23 12:00", "2011-06-23 13:00"),
                average=None,
                aberrate=False,
            )

    def test_loading_across_files(self):
        """Test if we can load data across multiple files"""

        data = load_between_dates(
            self.test_data_dir,
            TimeRange("2011-04-23 00:00", "2011-04-24 23:59"),
            average=None,
            aberrate=False,
        )

        # Again, these files were manually shortened
        assert len(data) == 20


if __name__ == "__main__":
    unittest.main()
