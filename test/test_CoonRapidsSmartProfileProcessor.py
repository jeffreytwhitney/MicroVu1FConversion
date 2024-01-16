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


def _get_node_text(line_text: str, search_value: str, start_delimiter: str, end_delimiter: str = "") -> str:
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


# Setup/Teardown
def setup_module():
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
    micro_vu = MicroVuProgram(_get_input_filepath("446007 ITEM 1 PROFILE.iwp"), "10", "A", "446007 ITEM 1 PROFILE")
    _processor.add_micro_vu_program(micro_vu)
    _processor.process_files()


def teardown_module():
    os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = ""


# Fixtures
@pytest.fixture(scope="module")
def micro_vu() -> MicroVuProgram:
    return MicroVuProgram(_get_input_filepath("446007 ITEM 1 PROFILE.iwp"), "10", "A", "")


@pytest.fixture(scope="module")
def micro_vu_lines() -> list[str]:
    output_path = _get_output_filepath("446007 ITEM 1 PROFILE.iwp")
    return _get_utf_encoded_file_lines(output_path)


# Tests
def test_output_file_exists(micro_vu_lines):
    assert os.path.exists(_get_output_filepath("446007 ITEM 1 PROFILE.iwp"))


def test_export_filepath(micro_vu_lines):
    assert _get_node_text(
            micro_vu_lines[2], "ExpFile", "\"") == "C:\\TEXT\\OUTPUT.txt"
    assert _get_node_text(
            micro_vu_lines[2], "AutoExpFile", "\"") == "C:\\TEXT\\OUTPUT.txt"


def test_auto_report_filepath(micro_vu_lines):
    assert _get_node_text(
            micro_vu_lines[2], "AutoRptFileName", "\"") == ""


def test_instruction_count(micro_vu_lines):
    assert "Instructions 63" in micro_vu_lines[3]


def test_text_kill_exists(micro_vu_lines):
    assert "TEXT KILL" in micro_vu_lines[4]


def test_created_by_exists(micro_vu_lines):
    assert _get_node_text(
            micro_vu_lines[10], "Txt", "\"") == "Created By:"


def test_comments(micro_vu_lines):
    assert _get_node_text(
            micro_vu_lines[11], "Txt", "\"") == "Edited By and Comments:"
    assert "Converted program to work with 1Factory." in micro_vu_lines[11]


def test_part_number_is_correct(micro_vu_lines):
    assert "(Txt \"446007\")" in micro_vu_lines[12]
    assert "(Name \"PT\")" in micro_vu_lines[12]


def test_rev_letter_is_correct(micro_vu_lines):
    assert "(Txt \"A\")" in micro_vu_lines[13]
    assert "(Name \"REV LETTER\")" in micro_vu_lines[13]


def test_op_number_is_correct(micro_vu_lines):
    assert "(Txt \"10\")" in micro_vu_lines[14]
    assert "(Name \"OPERATION\")" in micro_vu_lines[14]


def test_smartprofile_filename(micro_vu_lines):
    assert "(Txt \"446007 ITEM 1 PROFILE\")" in micro_vu_lines[15]
    assert "(Name \"SPFILENAME\")" in micro_vu_lines[15]


def test_employee_id_prompt_exists(micro_vu_lines):
    assert "(Txt \"Enter Employee #\")" in micro_vu_lines[16]
    assert "(Name \"EMPLOYEE\")" in micro_vu_lines[16]


def test_job_number_prompt_exists(micro_vu_lines):
    assert "(Txt \"Enter Job #\")" in micro_vu_lines[17]
    assert "(Name \"JOB\")" in micro_vu_lines[17]


def test_machine_number_prompt_exists(micro_vu_lines):
    assert "(Txt \"Enter Machine #\")" in micro_vu_lines[18]
    assert "(Name \"MACHINE\")" in micro_vu_lines[18]


def test_inprocess_text_exists(micro_vu_lines):
    assert "(Txt \"IN PROCESS\")" in micro_vu_lines[19]
    assert "(Name \"IN PROCESS\")" in micro_vu_lines[19]


def test_sequence_number_prompt_exists(micro_vu_lines):
    assert "(Txt \"SEQUENCE # IF SETUP PART USE 0 (ZERO).\")" in micro_vu_lines[20]
    assert "(Name \"SEQUENCE\")" in micro_vu_lines[20]


def test_smart_profile_call(micro_vu_lines):
    assert "(Name \"CallSmartProfileScript\")" in micro_vu_lines[327]

