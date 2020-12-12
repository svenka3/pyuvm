import pyuvm_unittest
from pyuvm import *
import pyuvm.utility_classes as utility_classes
import inspect

class config_db_TestCase(pyuvm_unittest.pyuvm_TestCase):

    def tearDown(self) -> None:
        utility_classes.ConfigDB.clear_singletons()

    def test_GlobPathDict_set_get(self):
        gpd = utility_classes.GlobPathDict()
        gpd["aa"] = 1
        self.assertEqual(1, gpd["aa"])

    def test_Glob_set_get(self):
        gpd = utility_classes.GlobPathDict()
        gpd["aa"] = 1
        gpd["bb"] = 2
        gpd["*"] = 3
        datum = gpd["aa"]
        self.assertEqual(1, datum)
        datum = gpd["bb"]
        self.assertEqual(2,datum)
        datum = gpd["cc"]
        self.assertEqual(3, datum)

    def test_index_match(self):
        gpd = utility_classes.GlobPathDict()
        gpd["aa"] = 1
        gpd["b?"] = 2

        self.assertEqual(1, gpd["aa"])
        self.assertEqual(2, gpd["bb"])
        gpd["*"] = 5
        self.assertEqual(5, gpd["zz"])

    def test_long_path_match(self):
        gpd = utility_classes.GlobPathDict()
        gpd["*"] = 5
        gpd["top.*"] = 8
        gpd["top.A.B"] = 3
        datum = gpd["X"]
        self.assertEqual(5, datum)
        datum = gpd['top.X']
        self.assertEqual(8, datum)
        datum = gpd["top.A"]
        self.assertEqual(8, datum)
        datum = gpd["top.A.B"]
        self.assertEqual(3, datum)

    def test_longest_path_match(self):
        gpd = utility_classes.GlobPathDict()
        gpd["*"] = 5
        gpd["A.*"] = 6
        gpd["A.B.*"] = 7
        gpd["A.B.D"] = 8

        datum = gpd["B"]
        self.assertEqual(5, datum)

        datum = gpd["A"]
        self.assertEqual(5, datum)

        datum = gpd["A.B"]
        self.assertEqual(6, datum)

        datum = gpd["A.B.C"]
        self.assertEqual(7, datum)

        datum = gpd["A.B.D"]
        self.assertEqual(8, datum)

        datum = gpd["A.C"]
        self.assertEqual(6, datum)

    def test_config_db(self):
        cdb = ConfigDB()
        # simple set/get
        cdb.set(5, "LABEL", "*")
        datum = cdb.get("LABEL", "A")
        self.assertEqual(5, datum)
        with self.assertRaises(error_classes.UVMConfigItemNotFound):
            cdb.get("NOT THERE", "A")

        cdb.set(88, "OTHER_LABEL", "*")
        datum = cdb.get("OTHER_LABEL", "top.B.C")
        self.assertEqual(88, datum)
        datum = cdb.get("OTHER_LABEL", "A")
        self.assertEqual(88, datum)

    def test_empty_db(self):
        cdb = ConfigDB()
        with self.assertRaises(error_classes.UVMConfigItemNotFound):
            cdb.get("LABEL", "A")

        cdb.set(5, "LABEL", "A")
        datum = cdb.get("LABEL", "A")
        self.assertEqual(5, datum)

        with self.assertRaises(error_classes.UVMConfigItemNotFound):
            cdb.get("LABEL", "B")

        cdb.set(88, "OTHER_LABEL", "B")
        datum = cdb.get("OTHER_LABEL", "B")
        self.assertEqual(88, datum)

        with self.assertRaises(error_classes.UVMConfigItemNotFound):
            cdb.get("LABEL", "B")

