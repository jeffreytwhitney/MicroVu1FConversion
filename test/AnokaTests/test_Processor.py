import configparser
import os
import pathlib

import pytest

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


# Fixtures
@pytest.fixture(scope="module")
def micro_vu_lines() -> list[str]:
    output_path = _get_output_filepath("NN00160A001-2_OPFAI_REVC_VMM_REV2.iwp")
    return _get_utf_encoded_file_lines(output_path)


def setup_module():
    _store_ini_value("Anoka", "Location", "site")
    _store_ini_value("True", "GlobalSettings", "hand_edit_dimension_names")
    input_path = _get_input_filepath("NN00160A001-2_OPFAI_REVC_VMM_REV2.iwp")
    micro_vu = MicroVuProgram(input_path, "10", "A", "")
    manual_dimensions = micro_vu.dimension_names
    for i, dimension in enumerate(manual_dimensions):
        new_dimension_name = f"INSP_{i+1}"
        manual_dimensions[i].name = new_dimension_name
    micro_vu.manual_dimension_names = manual_dimensions
    _processor = lib.MicroVuFileProcessor.get_processor("JTW")
    _processor.add_micro_vu_program(micro_vu)
    _processor.process_files()


# Tests
def test_correct_processor():
    p = lib.MicroVuFileProcessor.get_processor("JTW")
    assert isinstance(p, MicroVuFileProcessor.AnokaProcessor)


def test_output_file_exists(micro_vu_lines):
    assert os.path.exists(_get_output_filepath("NN00160A001-2_OPFAI_REVC_VMM_REV2.iwp"))


def test_export_filepath(micro_vu_lines):
    assert _get_node_text(
            micro_vu_lines[2], "ExpFile", "\"") == "C:\\Users\\Public\\CURL\\in\\NN00160A001-2_OP10_OPFAI REVC VMM_REVA_.csv"
    assert _get_node_text(
            micro_vu_lines[2], "AutoExpFile", "\"") == "C:\\Users\\Public\\CURL\\in\\NN00160A001-2_OP10_OPFAI REVC VMM_REVA_.csv"


def test_auto_report_filepath(micro_vu_lines):
    assert _get_node_text(
            micro_vu_lines[2], "AutoRptFileName", "\"") == "S:\\Micro-Vu\\NN00160A001-2_OP10_OPFAI REVC VMM_REVA_.pdf"


def test_instruction_count(micro_vu_lines):
    assert "Instructions 161" in micro_vu_lines[3]


def test_text_kill_exists(micro_vu_lines):
    assert "TEXT KILL" in micro_vu_lines[4]


def test_created_by_exists(micro_vu_lines):
    assert _get_node_text(
            micro_vu_lines[13], "Txt", "\"") == "Created By and Date:"


def test_comments(micro_vu_lines):
    assert _get_node_text(
            micro_vu_lines[14], "Txt", "\"") == "Edited By and Comments:"
    assert "Converted program to work with 1Factory." in micro_vu_lines[14]


def test_part_number_is_correct(micro_vu_lines):
    assert "(Txt \"NN00160A001-2\")" in micro_vu_lines[15]
    assert "(Name \"PT\")" in micro_vu_lines[15]


def test_rev_letter_is_correct(micro_vu_lines):
    assert "(Txt \"A\")" in micro_vu_lines[16]
    assert "(Name \"REV LETTER\")" in micro_vu_lines[16]


def test_op_number_is_correct(micro_vu_lines):
    assert "(Txt \"10\")" in micro_vu_lines[17]
    assert "(Name \"OPERATION\")" in micro_vu_lines[17]


def test_employee_id_prompt_exists(micro_vu_lines):
    assert "(Txt \"Enter Employee #\")" in micro_vu_lines[18]
    assert "(Name \"EMPLOYEE\")" in micro_vu_lines[18]


def test_job_number_prompt_exists(micro_vu_lines):
    assert "(Txt \"Enter Job #\")" in micro_vu_lines[19]
    assert "(Name \"JOB\")" in micro_vu_lines[19]


def test_machine_number_prompt_exists(micro_vu_lines):
    assert "(Txt \"Enter Machine #\")" in micro_vu_lines[20]
    assert "(Name \"MACHINE\")" in micro_vu_lines[20]


def test_inprocess_text_exists(micro_vu_lines):
    assert "(Txt \"IN PROCESS\")" in micro_vu_lines[21]
    assert "(Name \"IN PROCESS\")" in micro_vu_lines[21]


def test_sequence_number_prompt_exists(micro_vu_lines):
    assert "(Txt \"SEQUENCE # IF SETUP PART USE 0 (ZERO).\")" in micro_vu_lines[22]
    assert "(Name \"SEQUENCE\")" in micro_vu_lines[22]


def test_inspection_names(micro_vu_lines):
    assert "(Name \"INSP_1\")" in micro_vu_lines[526]
    assert "(Name \"INSP_2\")" in micro_vu_lines[536]
    assert "(Name \"INSP_3\")" in micro_vu_lines[544]
    assert "(Name \"INSP_4\")" in micro_vu_lines[552]
    assert "(Name \"INSP_5\")" in micro_vu_lines[557]
    assert "(Name \"INSP_6\")" in micro_vu_lines[572]
    assert "(Name \"INSP_7\")" in micro_vu_lines[577]
    assert "(Name \"INSP_8\")" in micro_vu_lines[583]