import lib
from lib import MicroVuFileProcessor
from test.CommonFunctions import store_ini_value


def setup_module():
    store_ini_value("Anoka", "Location", "site")
    store_ini_value("False", "GlobalSettings", "hand_edit_dimension_names")


def test_parse_dimension_names():
    processor = lib.MicroVuFileProcessor.get_processor("JTW")
    assert processor.parse_dimension_name("38.2 .125 DIST", "INSP_") == "INSP_38B"
    assert processor.parse_dimension_name("4 .500 DIST", "INSP_") == "INSP_4"
    assert processor.parse_dimension_name("1 .841 DIST", "INSP_") == "INSP_1"
    assert processor.parse_dimension_name("45.2_.058/.062", "INSP_") == "INSP_45B"

    assert processor.parse_dimension_name("(REF) TOP SLOT LENGTH", "INSP_") == "(REF) TOP SLOT LENGTH"
