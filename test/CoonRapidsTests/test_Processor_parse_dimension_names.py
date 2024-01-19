import lib
from lib import MicroVuFileProcessor
from test.CommonFunctions import store_ini_value


def setup_module():
    store_ini_value("CoonRapids", "Location", "site")
    store_ini_value("False", "GlobalSettings", "hand_edit_dimension_names")


def test_parse_dimension_names():
    processor = lib.MicroVuFileProcessor.get_processor("JTW")
    assert processor.parse_dimension_name("12", "INSP_") == "INSP_12"
    assert processor.parse_dimension_name("ITEM 12A 1X", "INSP_") == "ITEM 12A 1X"
    assert processor.parse_dimension_name("ITEM_12A 1X", "INSP_") == "ITEM_12A 1X"
    assert processor.parse_dimension_name("ITEM_12A_1X", "INSP_") == "ITEM_12A_1X"
    assert processor.parse_dimension_name("ITEM 12A_1X", "INSP_") == "ITEM 12A_1X"
    assert processor.parse_dimension_name("ITEM 12.1A 1X", "INSP_") == "ITEM 12.1A 1X"
    assert processor.parse_dimension_name("ITEM_12.1A 1X", "INSP_") == "ITEM_12.1A 1X"
    assert processor.parse_dimension_name("ITEM_12.1A_1X", "INSP_") == "ITEM_12.1A_1X"
    assert processor.parse_dimension_name("ITEM 12.1A_1X", "INSP_") == "ITEM 12.1A_1X"
    assert processor.parse_dimension_name("12", "INSP_") == "INSP_12"
    assert processor.parse_dimension_name("ITEM 12", "INSP_") == "INSP_12"
    assert processor.parse_dimension_name("ITEM_12", "INSP_") == "INSP_12"
    assert processor.parse_dimension_name("INSP 12", "INSP_") == "INSP_12"
    assert processor.parse_dimension_name("INSP_12", "INSP_") == "INSP_12"
    assert processor.parse_dimension_name("ITEM 12 1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("ITEM_12 1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("ITEM_12_1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("ITEM 12_1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("INSP 12 1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("INSP_12 1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("INSP_12_1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("INSP 12_1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("12_1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("ITEM-12", "INSP_") == "INSP_12"
    assert processor.parse_dimension_name("INSP-12", "INSP_") == "INSP_12"
    assert processor.parse_dimension_name("ITEM 12.16", "INSP_") == "INSP_12.16"
    assert processor.parse_dimension_name("ITEM_12.16", "INSP_") == "INSP_12.16"
    assert processor.parse_dimension_name("INSP 12.16", "INSP_") == "INSP_12.16"
    assert processor.parse_dimension_name("INSP_12.16", "INSP_") == "INSP_12.16"
    assert processor.parse_dimension_name("ITEM-12.1", "INSP_") == "INSP_12.1"
    assert processor.parse_dimension_name("INSP-12.1", "INSP_") == "INSP_12.1"
    assert processor.parse_dimension_name("INSP-12.1_1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("INSP_12.1-1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("INSP-12.1-1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("ITEM-12.1_1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("ITEM_12.1-1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("ITEM-12.1-1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12.1-1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12.1-1", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12.1", "INSP_") == "INSP_12.1"
    assert processor.parse_dimension_name("ITEM 12.1", "INSP_") == "INSP_12.1"
    assert processor.parse_dimension_name("ITEM_12.1", "INSP_") == "INSP_12.1"
    assert processor.parse_dimension_name("INSP 12.1", "INSP_") == "INSP_12.1"
    assert processor.parse_dimension_name("INSP_12.1", "INSP_") == "INSP_12.1"
    assert processor.parse_dimension_name("ITEM 12.1 1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("ITEM_12.1 1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("ITEM_12.1_1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("ITEM 12.1_1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("INSP 12.1 1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("INSP_12.1 1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("INSP_12.1_1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("INSP 12.1_1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12.1 1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12.1_1X", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12.1 A", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12.1_A", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12 1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("12 A", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("12_A", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("12A", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("INSP-12_1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("INSP_12-1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("INSP-12-1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("ITEM-12_1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("ITEM_12-1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("ITEM-12-1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("12-1X", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("12-1", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("12_1", "INSP_") == "INSP_12A"
    assert processor.parse_dimension_name("12.1A", "INSP_") == "INSP_12.1A"
    assert processor.parse_dimension_name("12.1_1", "INSP_") == "INSP_12.1A"
