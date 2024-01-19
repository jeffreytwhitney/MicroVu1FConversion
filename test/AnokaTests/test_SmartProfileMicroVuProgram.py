import shutil

import pytest

from lib.MicroVuProgram import MicroVuProgram
from test.CommonFunctions import get_input_filepath, delete_all_files_in_output_directory, get_output_filepath, \
    get_output_directory


# Fixtures
@pytest.fixture(scope="module")
def micro_vu() -> MicroVuProgram:
    return MicroVuProgram(get_input_filepath("110047396A0_OPFAI_REVA_SP.iwp"), "10", "A", "110047396A0_OPFAI_REVA_SP.iwp")


def test_instruction_index(micro_vu):
    assert micro_vu.instructions_index == 3


def test_has_killfile(micro_vu):
    assert micro_vu.has_text_kill is False


def test_can_write_to_output_file(micro_vu):
    assert micro_vu.can_write_to_output_file is True
    shutil.copy(get_input_filepath("110047396A0_OPFAI_REVA_SP.iwp"), get_output_filepath("110047396A0_OPFAI_REVA_SP.iwp"))
    assert micro_vu.can_write_to_output_file is False
    delete_all_files_in_output_directory()


def test_comment(micro_vu):
    assert micro_vu.comment == ""


def test_set_comment(micro_vu):
    assert micro_vu.comment == ""
    micro_vu.comment = "bob"
    assert micro_vu.file_lines[5] == "Txt 0 22119100 (Name \"Edited by & comments\" (Txt \"bob\")\n"
    assert micro_vu.comment == "bob"
    micro_vu.comment = ""
    assert not micro_vu.comment


def test_dimension_names(micro_vu):
    assert len(micro_vu.dimension_names) == 0


def test_export_filepath(micro_vu):
    assert micro_vu.export_filepath == "C:\\TEXT\\OUTPUT.txt"


def test_set_export_filepath(micro_vu):
    micro_vu.export_filepath = "bob"
    assert micro_vu.export_filepath == "C:\\TEXT\\OUTPUT.txt"
    micro_vu.export_filepath = "C:\\TEXT\\OUTPUT.txt"
    assert micro_vu.export_filepath == "C:\\TEXT\\OUTPUT.txt"


def test_filename(micro_vu):
    assert micro_vu.filename == "110047396A0_OPFAI_REVA_SP.iwp"


def test_filepath(micro_vu):
    assert micro_vu.filepath == get_input_filepath("110047396A0_OPFAI_REVA_SP.iwp")


def test_has_calculators(micro_vu):
    assert micro_vu.has_calculators is False


def test_get_existing_smartprofile_call_index(micro_vu):
    assert micro_vu.get_existing_smartprofile_call_index == -1


def test_is_smartprofile(micro_vu):
    assert micro_vu.is_smartprofile is True


def test_last_microvu_system_id(micro_vu):
    assert micro_vu.last_microvu_system_id == "220E9D70"


def test_manual_dimension_names(micro_vu):
    assert len(micro_vu.manual_dimension_names) == 0
    micro_vu.manual_dimension_names = micro_vu.dimension_names
    assert len(micro_vu.manual_dimension_names) == 0
    micro_vu.manual_dimension_names = []


def test_op_number(micro_vu):
    assert micro_vu.op_number == "10"


def test_output_directory(micro_vu):
    assert micro_vu.output_directory == get_output_directory()


def test_output_filepath(micro_vu):
    assert micro_vu.output_filepath == get_output_filepath("110047396A0_OPFAI_REVA_SP.iwp")


def test_part_number(micro_vu):
    assert micro_vu.part_number == "110047396A0"


def test_prompt_insertion_index(micro_vu):
    assert micro_vu.prompt_insertion_index == 5


def test_report_filepath(micro_vu):
    assert not micro_vu.report_filepath
    micro_vu.report_filepath = "dave"
    assert not micro_vu.report_filepath


def test_rev_number(micro_vu):
    assert micro_vu.rev_number == "A"


def test_smartprofile_call_insertion_index(micro_vu):
    assert micro_vu.smartprofile_call_insertion_index == 605


def test_smartprofile_projectname(micro_vu):
    assert micro_vu.smartprofile_projectname == "110047396A0_OPFAI_REVA_SP.iwp"


def test_view_name(micro_vu):
    assert micro_vu.view_name == "OPFAI"


def test_delete_line_containing_text(micro_vu):
    number_of_lines = len(micro_vu.file_lines)
    micro_vu.insert_line(10, "Prmt 0 1EFD3AA8 (Name \"Farfignugen #\") (ExpProps Ans) (Txt \"Farfignugen\")")
    micro_vu.delete_line_containing_text("Farfignugen")
    assert len(micro_vu.file_lines) == number_of_lines


def test_get_index_containing_text(micro_vu):
    assert micro_vu.get_index_containing_text("(Name \"Employee") == 6


def test_insert_line(micro_vu):
    micro_vu.insert_line(10, "Farfignugen")
    assert micro_vu.file_lines[10].find("Farfignugen") > -1
    del micro_vu.file_lines[10]


def test_update_feature_name(micro_vu):
    micro_vu.update_feature_name(53, "Farfignugen")
    assert micro_vu.file_lines[53].find("Farfignugen") > -1
    micro_vu.update_feature_name(53, "289")
    assert micro_vu.file_lines[53].find("289") > -1


def test_update_instruction_count(micro_vu):
    micro_vu.insert_line(10, "Prmt 0 1EFD3AA8 (Name \"Farfignugen #\") (ExpProps Ans) (Txt \"Farfignugen\")")
    micro_vu.update_instruction_count()
    assert micro_vu.file_lines[3].find("Instructions 133") > -1
    micro_vu.delete_line_containing_text("Farfignugen")
    micro_vu.update_instruction_count()
    assert micro_vu.file_lines[3].find("Instructions 132") > -1
