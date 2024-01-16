import configparser
import os

import pytest

import lib.MicroVuFileProcessor
from lib.MicroVuProgram import MicroVuProgram


# Support Methods
def _delete_all_files_in_output_directory():
    for root, dirs, files in os.walk(_get_output_root_path()):
        for item in files:
            filespec = os.path.join(root, item)
            os.unlink(filespec)


def _get_dot_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)
    return ""


def _get_filepath_by_name(file_name: str) -> str:
    current_dir = os.path.dirname(__file__)
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file == file_name:
                return str(os.path.join(root, file))
    return ""


def _get_input_filepath(file_name: str) -> str:
    return str(os.path.join(_get_input_root_path(), file_name))


def _get_input_root_path() -> str:
    current_dir = os.path.dirname(__file__)
    return str(os.path.join(current_dir, "Input"))


def _get_output_directory() -> str:
    return str(os.path.join(_get_output_root_path(), "Input"))


def _get_output_filepath(file_name: str):
    return str(os.path.join(_get_output_directory(), file_name))


def _get_output_root_path() -> str:
    current_dir = os.path.dirname(__file__)
    return str(os.path.join(current_dir, "Output"))


def get_node_text(line_text: str, search_value: str, start_delimiter: str, end_delimiter: str = "") -> str:
    if not end_delimiter:
        end_delimiter = start_delimiter
    title_index: int = line_text.upper().find(search_value.upper())
    begin_index: int = line_text.find(start_delimiter, title_index + len(search_value))
    end_index: int = line_text.find(end_delimiter, begin_index + 1)
    if end_index == -1:
        end_index = len(line_text)
    return line_text[begin_index + 1:end_index].strip()


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


def get_utf_encoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    with open(file_path, "r", encoding='utf-16-le') as f:
        return f.readlines()


def set_node_text(line_text: str, search_value: str, set_value: str, start_delimiter: str,
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


# Setup/Teardown
def setup_module(micro_vu):
    config_filepath = _get_filepath_by_name("TESTSettings.ini")
    os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = config_filepath
    input_path = _get_input_root_path()
    output_path = _get_output_root_path()
    _store_ini_value(input_path, "Paths", "input_rootpath")
    _store_ini_value(output_path, "Paths", "output_rootpath")
    _delete_all_files_in_output_directory()
    if not os.path.exists(_get_output_directory()):
        os.mkdir(_get_output_directory())
    _processor = lib.MicroVuFileProcessor.get_processor("JTW")
    _processor.add_micro_vu_program(micro_vu)


def teardown_module():
    os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = ""
    _delete_all_files_in_output_directory()


# Fixtures
@pytest.fixture(scope="module")
def micro_vu() -> MicroVuProgram:
    return MicroVuProgram(_get_input_filepath("446007 END VIEW.iwp"), "10", "A", "")


@pytest.fixture(scope="module")
def micro_vu_lines() -> list[str]:
    return get_utf_encoded_file_lines(_get_output_filepath("446007 END VIEW.iwp"))


# Tests
def test_output_file_exists():
    assert False


def test_export_filepath(micro_vu_lines):
    assert False


def test_auto_export_filepath(micro_vu_lines):
    assert False


def test_auto_report_filepath(micro_vu_lines):
    assert False


def test_instruction_count(micro_vu_lines):
    assert False


def test_created_by_exists(micro_vu_lines):
    assert False


def test_comments_exist(micro_vu_lines):
    assert False


def test_comments_has_new_comment(micro_vu_lines):
    assert False


def test_part_number_text_exists(micro_vu_lines):
    assert False
