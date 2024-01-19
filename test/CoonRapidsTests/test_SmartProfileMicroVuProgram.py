import shutil

import pytest

from lib.MicroVuProgram import MicroVuProgram
from test.CommonFunctions import get_input_filepath, get_output_filepath, delete_all_files_in_output_directory, \
    get_output_directory


# Fixtures
@pytest.fixture(scope="module")
def micro_vu() -> MicroVuProgram:
    return MicroVuProgram(get_input_filepath("446007 ITEM 1 PROFILE.iwp"), "10", "A", "446007 ITEM 1 PROFILE.spp")


def test_has_auto_report(micro_vu):
    assert micro_vu.has_auto_report


def test_instruction_index(micro_vu):
    assert micro_vu.instructions_index == 3


def test_has_killfile(micro_vu):
    assert micro_vu.has_text_kill is True


def test_can_write_to_output_file(micro_vu):
    assert micro_vu.can_write_to_output_file is True
    shutil.copy(get_input_filepath("446007 ITEM 1 PROFILE.iwp"), get_output_filepath("446007 ITEM 1 PROFILE.iwp"))
    assert micro_vu.can_write_to_output_file is False
    delete_all_files_in_output_directory()


def test_comment(micro_vu):
    assert micro_vu.comment == "Edited By and Comments: UPDATED THE LIGHTING FOR THE SOFTWARE CHANGE SB 10/6/2021."


def test_set_comment(micro_vu):
    assert micro_vu.comment == "Edited By and Comments: UPDATED THE LIGHTING FOR THE SOFTWARE CHANGE SB 10/6/2021."
    micro_vu.comment = "bob"
    assert micro_vu.comment == "bob"
    micro_vu.comment = "Edited By and Comments: UPDATED THE LIGHTING FOR THE SOFTWARE CHANGE SB 10/6/2021."
    assert micro_vu.comment == "Edited By and Comments: UPDATED THE LIGHTING FOR THE SOFTWARE CHANGE SB 10/6/2021."


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
    assert micro_vu.filename == "446007 ITEM 1 PROFILE.iwp"


def test_filepath(micro_vu):
    assert micro_vu.filepath == get_input_filepath("446007 ITEM 1 PROFILE.iwp")


def test_has_calculators(micro_vu):
    assert micro_vu.has_calculators is False


def test_get_existing_smartprofile_call_index(micro_vu):
    assert micro_vu.get_existing_smartprofile_call_index == -1


def test_is_smartprofile(micro_vu):
    assert micro_vu.is_smartprofile is True


def test_last_microvu_system_id(micro_vu):
    assert micro_vu.last_microvu_system_id == "1F41F120"


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
    assert micro_vu.output_filepath == get_output_filepath("446007 ITEM 1 PROFILE.iwp")


def test_part_number(micro_vu):
    assert micro_vu.part_number == "446007"


def test_prompt_insertion_index(micro_vu):
    assert micro_vu.prompt_insertion_index == 11


def test_report_filepath(micro_vu):
    assert not micro_vu.report_filepath
    micro_vu.report_filepath = "dave"
    assert not micro_vu.report_filepath


def test_rev_number(micro_vu):
    assert micro_vu.rev_number == "A"


def test_smartprofile_call_insertion_index(micro_vu):
    assert micro_vu.smartprofile_call_insertion_index == 323


def test_smartprofile_projectname(micro_vu):
    assert micro_vu.smartprofile_projectname == "446007 ITEM 1 PROFILE.spp"


def test_view_name(micro_vu):
    assert micro_vu.view_name == "ITEM 1 PROFILE"


def test_delete_line_containing_text(micro_vu):
    number_of_lines = len(micro_vu.file_lines)
    micro_vu.insert_line(10, "Prmt 0 1EFD3AA8 (Name \"Farfignugen #\") (ExpProps Ans) (Txt \"Farfignugen\")")
    micro_vu.delete_line_containing_text("Farfignugen")
    assert len(micro_vu.file_lines) == number_of_lines


def test_get_index_containing_text(micro_vu):
    assert micro_vu.get_index_containing_text("(Name \"Employee #") == 13


def test_insert_line(micro_vu):
    micro_vu.insert_line(10, "Farfignugen")
    assert micro_vu.file_lines[10].find("Farfignugen") > -1
    del micro_vu.file_lines[10]


def test_update_feature_name(micro_vu):
    micro_vu.update_feature_name(20, "Farfignugen")
    assert micro_vu.file_lines[20].find("Farfignugen") > -1
    micro_vu.update_feature_name(20, "77")
    assert micro_vu.file_lines[20].find("77") > -1


def test_update_instruction_count(micro_vu):
    micro_vu.insert_line(10, "Prmt 0 1EFD3AA8 (Name \"Farfignugen #\") (ExpProps Ans) (Txt \"Farfignugen\")")
    micro_vu.update_instruction_count()
    assert micro_vu.file_lines[3].find("Instructions 59") > -1
    micro_vu.delete_line_containing_text("Farfignugen")
    micro_vu.update_instruction_count()
    assert micro_vu.file_lines[3].find("Instructions 58") > -1
