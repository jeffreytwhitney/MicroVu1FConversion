import configparser
import os
import pathlib

import lib
from lib import MicroVuFileProcessor
from lib.MicroVuProgram import MicroVuProgram


# Support Methods
def _delete_all_files_in_output_directory():
    for root, dirs, files in os.walk(_get_output_root_path()):
        for item in files:
            filespec = os.path.join(root, item)
            os.unlink(filespec)


def _get_dot_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk(_get_parent_directory()):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)
    return ""


def _get_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk(_get_parent_directory()):
        for file in files:
            if file == file_name:
                return str(os.path.join(root, file))
    return ""


def _get_input_filepath(file_name: str):
    return str(os.path.join(_get_input_root_path(), file_name))


def _get_input_root_path() -> str:
    return str(os.path.join(_get_parent_directory(), "Input"))


def _get_node_text(line_text: str, search_value: str, start_delimiter: str, end_delimiter: str = "") -> str:
    if not end_delimiter:
        end_delimiter = start_delimiter
    title_index: int = line_text.upper().find(search_value.upper())
    begin_index: int = line_text.find(start_delimiter, title_index + len(search_value))
    end_index: int = line_text.find(end_delimiter, begin_index + 1)
    if end_index == -1:
        end_index = len(line_text)
    return line_text[begin_index + 1:end_index].strip()


def _get_output_directory() -> str:
    return str(os.path.join(_get_output_root_path(), "Input"))


def _get_output_filepath(file_name: str):
    return str(os.path.join(_get_output_directory(), file_name))


def _get_output_root_path() -> str:
    return str(os.path.join(_get_parent_directory(), "Output"))


def _get_parent_directory():
    current_dir = os.path.dirname(__file__)
    return str(pathlib.Path(current_dir).resolve().parents[0])


def _get_stored_ini_value(ini_section, ini_key):
    ini_file_path = _get_filepath_by_name("TESTSettings.ini")
    config = configparser.ConfigParser()
    config.read(ini_file_path)
    try:
        config_value = config.get(ini_section, ini_key)
    except:
        try:
            config_value = config.get(ini_section, "*")
        except:
            config_value = ""
    return config_value


def _get_unencoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    with open(file_path, "r") as f:
        return f.readlines()


def _get_utf_encoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    with open(file_path, "r", encoding='utf-16-le') as f:
        return f.readlines()


def _set_node_text(line_text: str, search_value: str, set_value: str, start_delimiter: str,
                   end_delimiter: str = "") -> str:
    current_value: str = MicroVuProgram.get_node_text(line_text, search_value, start_delimiter, end_delimiter)
    current_node: str = search_value + start_delimiter + current_value + end_delimiter
    new_node: str = search_value + start_delimiter + set_value + end_delimiter
    return line_text.replace(current_node, new_node)


def _store_ini_value(ini_value, ini_section, ini_key):
    ini_file_path = _get_filepath_by_name("TESTSettings.ini")
    config = configparser.ConfigParser()
    if not os.path.exists(ini_file_path):
        config.add_section(ini_section)
    else:
        if not config.has_section(ini_section):
            config.add_section(ini_section)
        config.read(ini_file_path)
    config.set(ini_section, ini_key, ini_value)
    with open(ini_file_path, "w") as conf:
        config.write(conf)


def setup_module():
    _store_ini_value("CoonRapids", "Location", "site")
    _store_ini_value("False", "GlobalSettings", "hand_edit_dimension_names")


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
