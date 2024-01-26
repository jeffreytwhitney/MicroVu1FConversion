import os

import pytest

import lib
from lib import MicroVuFileProcessor
from lib.MicroVuProgram import MicroVuProgram
from test.CommonFunctions import store_ini_value, get_input_filepath, get_output_filepath, get_utf_encoded_file_lines, \
    get_node_text


# Fixtures
@pytest.fixture(scope="module")
def micro_vu_lines() -> list[str]:
    output_path = get_output_filepath("446007 DATUM F UP.iwp")
    return get_utf_encoded_file_lines(output_path)


def setup_module():
    store_ini_value("CoonRapids", "Location", "site")
    store_ini_value("False", "GlobalSettings", "hand_edit_dimension_names")
    input_path = get_input_filepath("446007 DATUM F UP.iwp")
    micro_vu = MicroVuProgram(input_path, "10", "A", "")
    _processor = lib.MicroVuFileProcessor.get_processor("JTW")
    _processor.add_micro_vu_program(micro_vu)
    _processor.process_files()


# Tests
def test_add_get_microvu():
    microvu = MicroVuProgram(get_input_filepath("446007 DATUM F UP.iwp"), "10", "A", "")
    p = lib.MicroVuFileProcessor.get_processor("JTW")
    p.add_micro_vu_program(microvu)
    assert len(p.micro_vu_programs) == 1
    second_micro_vu = p.micro_vu_programs[0]
    assert microvu == second_micro_vu


def test_add_get_microvus():
    micro_vu_list: list[MicroVuProgram] = []
    mv1 = MicroVuProgram(get_input_filepath("446007 DATUM F UP.iwp"), "10", "A", "")
    micro_vu_list.append(mv1)
    mv2 = MicroVuProgram(get_input_filepath("446007 ITEM 1 PROFILE.iwp"), "10", "A", "")
    micro_vu_list.append(mv2)
    p = lib.MicroVuFileProcessor.get_processor("JTW")
    p.add_micro_vu_programs(micro_vu_list)
    assert len(p.micro_vu_programs) == 2
    assert micro_vu_list == p.micro_vu_programs


def test_correct_processor():
    p = lib.MicroVuFileProcessor.get_processor("JTW")
    assert isinstance(p, MicroVuFileProcessor.CoonRapidsProcessor)


def test_output_file_exists(micro_vu_lines):
    assert os.path.exists(get_output_filepath("446007 DATUM F UP.iwp"))


def test_export_filepath(micro_vu_lines):
    assert get_node_text(
            micro_vu_lines[2], "ExpFile", "\"") == "C:\\Users\\Public\\CURL\\in\\446007_OP10_DATUM F UP_REVA_.csv"
    assert get_node_text(
            micro_vu_lines[2], "AutoExpFile", "\"") == "C:\\Users\\Public\\CURL\\in\\446007_OP10_DATUM F UP_REVA_.csv"


def test_auto_report_filepath(micro_vu_lines):
    assert get_node_text(
            micro_vu_lines[2], "AutoRptFileName", "\"") == "S:\\Micro-Vu\\446007_OP10_DATUM F UP_REVA_.pdf"


def test_instruction_count(micro_vu_lines):
    assert "Instructions 58" in micro_vu_lines[3]


def test_text_kill_exists(micro_vu_lines):
    assert "TEXT KILL" in micro_vu_lines[4]


def test_created_by_exists(micro_vu_lines):
    assert get_node_text(
            micro_vu_lines[13], "Txt", "\"") == "Created By:"


def test_comments(micro_vu_lines):
    assert get_node_text(
            micro_vu_lines[14], "Txt", "\"") == "Edited By and Comments:"
    assert "Converted program to work with 1Factory." in micro_vu_lines[14]


def test_part_number_is_correct(micro_vu_lines):
    assert "(Txt \"446007\")" in micro_vu_lines[15]
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
    assert "(Name \"INSP_19\")" in micro_vu_lines[299]
    assert "(DistX \"INSP_19\")" in micro_vu_lines[299]
    assert "(Name \"INSP_20\")" in micro_vu_lines[305]
    assert "(DistX \"INSP_20\")" in micro_vu_lines[305]
    assert "(Name \"INSP_21\")" in micro_vu_lines[311]
    assert "(DistX \"INSP_21\")" in micro_vu_lines[311]


def test_features_disabled(micro_vu_lines):
    assert "(AutoRpt 0)" in micro_vu_lines[2]
    assert "(AutoConf 0)" in micro_vu_lines[2]
    assert "(DontMeasure)" in micro_vu_lines[34]
    assert "(DontMeasure)" in micro_vu_lines[39]
    assert "(DontMeasure)" in micro_vu_lines[47]
    assert "(DontMeasure)" in micro_vu_lines[239]
    assert "(DontMeasure)" in micro_vu_lines[258]
    assert "(DontMeasure)" in micro_vu_lines[277]
    assert "(DontMeasure)" in micro_vu_lines[281]
    assert "(DontMeasure)" in micro_vu_lines[285]
    assert "(DontMeasure)" in micro_vu_lines[294]
    assert "(DontMeasure)" in micro_vu_lines[299]
    assert "(DontMeasure)" in micro_vu_lines[305]
    assert "(DontMeasure)" in micro_vu_lines[311]
