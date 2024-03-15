import os

import pytest

import lib
from lib import MicroVuFileProcessor
from lib.MicroVuProgram import MicroVuProgram
from test.CommonFunctions import get_output_filepath, get_utf_encoded_file_lines, get_input_filepath, store_ini_value, \
    get_node_text


# Fixtures
@pytest.fixture(scope="module")
def micro_vu_lines() -> list[str]:
    output_path = get_output_filepath("110047396A0_OPFAI_REVA_SP.iwp")
    return get_utf_encoded_file_lines(output_path)


def setup_module():
    store_ini_value("Anoka", "Location", "site")
    store_ini_value("True", "GlobalSettings", "hand_edit_dimension_names")
    input_path = get_input_filepath("110047396A0_OPFAI_REVA_SP.iwp")
    micro_vu = MicroVuProgram(input_path, "10", "A", "110047396A0_OPFAI_REVA_SP")
    manual_dimensions = micro_vu.dimension_names
    for i, dimension in enumerate(manual_dimensions):
        new_dimension_name = f"INSP_{i + 1}"
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
    assert os.path.exists(get_output_filepath("110047396A0_OPFAI_REVA_SP.iwp"))


def test_export_filepath(micro_vu_lines):
    assert get_node_text(
            micro_vu_lines[2], "ExpFile", "\"") == "C:\\TEXT\\OUTPUT.txt"
    assert get_node_text(
            micro_vu_lines[2], "AutoExpFile", "\"") == "C:\\TEXT\\OUTPUT.txt"


def test_auto_report_filepath(micro_vu_lines):
    assert get_node_text(
            micro_vu_lines[2], "AutoRptFileName", "\"") == ""


def test_instruction_count(micro_vu_lines):
    assert "Instructions 141\n" in micro_vu_lines[3]


def test_text_kill_exists(micro_vu_lines):
    assert "C:\\killFile.bat" in micro_vu_lines[4]
    assert "TEXT KILL" in micro_vu_lines[4]


def test_bring_part_to_met_exists(micro_vu_lines):
    assert "Bring part to Metrology" in micro_vu_lines[7]


def test_created_by_exists(micro_vu_lines):
    assert get_node_text(
            micro_vu_lines[10], "Txt", "\"") == "Created by & date"


def test_comments(micro_vu_lines):
    assert get_node_text(
            micro_vu_lines[11], "Txt", "\"") == "Edited by & comments"
    assert "Converted program to work with 1Factory." in micro_vu_lines[11]


def test_part_number_is_correct(micro_vu_lines):
    assert "(Txt \"110047396A0\")" in micro_vu_lines[12]
    assert "(Name \"PT\")" in micro_vu_lines[12]


def test_rev_letter_is_correct(micro_vu_lines):
    assert "(Txt \"A\")" in micro_vu_lines[13]
    assert "(Name \"REV LETTER\")" in micro_vu_lines[13]


def test_op_number_is_correct(micro_vu_lines):
    assert "(Txt \"10\")" in micro_vu_lines[14]
    assert "(Name \"OPERATION\")" in micro_vu_lines[14]


def test_sp_filename(micro_vu_lines):
    assert "(Txt \"110047396A0_OPFAI_REVA_SP\")" in micro_vu_lines[15]
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


def test_smart_profile_call_exists(micro_vu_lines):
    assert "(Name \"CallSmartProfileScript\")" in micro_vu_lines[618]
    assert "SmartProfile.exe" in micro_vu_lines[618]

def test_features_disabled(micro_vu_lines):

    assert "(AutoRpt 0)" in micro_vu_lines[2]
    assert "(AutoConf 0)" in micro_vu_lines[2]
    assert "(DontMeasure)" in micro_vu_lines[15]
    assert "(DontMeasure)" in micro_vu_lines[16]
    assert "(DontMeasure)" in micro_vu_lines[17]
    assert "(DontMeasure)" in micro_vu_lines[18]
    assert "(DontMeasure)" in micro_vu_lines[19]
    assert "(DontMeasure)" in micro_vu_lines[20]
    assert "(DontMeasure)" in micro_vu_lines[21]
    assert "(DontMeasure)" in micro_vu_lines[22]
    assert "(DontMeasure)" in micro_vu_lines[75]
    assert "(DontMeasure)" in micro_vu_lines[80]
    assert "(DontMeasure)" in micro_vu_lines[93]
    assert "(DontMeasure)" in micro_vu_lines[98]
    assert "(DontMeasure)" in micro_vu_lines[129]
    assert "(DontMeasure)" in micro_vu_lines[135]
    assert "(DontMeasure)" in micro_vu_lines[140]
    assert "(DontMeasure)" in micro_vu_lines[145]