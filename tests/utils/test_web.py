import unittest

import requests

from hermpy.utils import Urls


class Test_Web_Access(unittest.TestCase):
    def test_PDS_BASE(self):
        r = requests.head(Urls.PDS_BASE)
        self.assertEqual(r.status_code, 200)

    def test_mag_location(self):
        """
        Checks if MESSENGER MAG data is still following the correct format
        """
        url = (
            Urls.PDS_BASE
            + Urls.MAG_EXTENSION
            + "2011/091_120_APR/MAGMSOSCI11113_V08.TAB"
        )
        r = requests.head(url)

        self.assertEqual(r.status_code, 200)

        url = (
            Urls.PDS_BASE
            + Urls.MAG_EXTENSION_AVG
            + "2011/091_120_APR/MAGMSOSCI11113_01_V08.TAB"
        )
        r = requests.head(url)

        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()
