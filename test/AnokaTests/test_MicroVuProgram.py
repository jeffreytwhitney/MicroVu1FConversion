import configparser
import os
import pathlib
import shutil

import pytest

from lib.MicroVuProgram import MicroVuProgram


def _get_parent_directory():
    current_dir = os.path.dirname(__file__)
    return str(pathlib.Path(current_dir).resolve().parents[0])


def _delete_all_files_in_output_directory():
    for root, dirs, files in os.walk(_get_output_root_path()):
        for item in files:
            filespec = os.path.join(root, item)
            os.unlink(filespec)


def _get_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk(_get_parent_directory()):
        for file in files:
            if file == file_name:
                return str(os.path.join(root, file))
    return ""


def _get_dot_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk(_get_parent_directory()):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)
    return ""


def _get_input_root_path() -> str:
    return str(os.path.join(_get_parent_directory(), "Input"))


def _get_output_root_path() -> str:
    return str(os.path.join(_get_parent_directory(), "Output"))


def _get_output_directory() -> str:
    return str(os.path.join(_get_output_root_path(), "Input"))


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


def _get_input_filepath():
    return str(os.path.join(_get_input_root_path(), "NN00160A001-2_OPFAI_REVC_VMM_REV2.iwp"))


def _get_output_filepath():
    return str(os.path.join(_get_output_directory(), "NN00160A001-2_OPFAI_REVC_VMM_REV2.iwp"))


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
def micro_vu() -> MicroVuProgram:
    return MicroVuProgram(_get_input_filepath(), "10", "A", "")


def test_has_auto_report(micro_vu):
    assert not micro_vu.has_auto_report


def test_can_write_to_output_file(micro_vu):
    assert micro_vu.can_write_to_output_file is True
    shutil.copy(_get_input_filepath(), _get_output_filepath())
    assert micro_vu.can_write_to_output_file is False
    _delete_all_files_in_output_directory()


def test_instruction_index(micro_vu):
    assert micro_vu.instructions_index == 3


def test_has_killfile(micro_vu):
    assert micro_vu.has_text_kill is True


def test_comment(micro_vu):
    assert micro_vu.comment == "Edited By and Comments:"


def test_set_comment(micro_vu):
    micro_vu.comment = "bob"
    assert micro_vu.comment == "bob"
    micro_vu.comment = "Edited By and Comments: UPDATED THE LIGHTING BECAUSE OF THE SOFTWARE UPDATED SB 10/6/2021."
    assert micro_vu.comment == "Edited By and Comments: UPDATED THE LIGHTING BECAUSE OF THE SOFTWARE UPDATED SB 10/6/2021."


def test_dimension_names(micro_vu):
    assert len(micro_vu.dimension_names) == 31


def test_export_filepath(micro_vu):
    assert micro_vu.export_filepath == "C:\\SPCdata\\NN00160A001-2_OPFAI_REVC_MV.sta"


def test_set_export_filepath(micro_vu):
    micro_vu.export_filepath = "bob"
    assert micro_vu.export_filepath == "bob"
    micro_vu.export_filepath = "C:\\spcdata\\mvexport.txt"
    assert micro_vu.export_filepath == "C:\\spcdata\\mvexport.txt"


def test_filename(micro_vu):
    assert micro_vu.filename == "NN00160A001-2_OPFAI_REVC_VMM_REV2.iwp"


def test_filepath(micro_vu):
    assert micro_vu.filepath == _get_input_filepath()


def test_has_calculators(micro_vu):
    assert micro_vu.has_calculators is False


def test_get_existing_smartprofile_call_index(micro_vu):
    assert micro_vu.get_existing_smartprofile_call_index == -1


def test_is_smartprofile(micro_vu):
    assert micro_vu.is_smartprofile is False


def test_last_microvu_system_id(micro_vu):
    assert micro_vu.last_microvu_system_id == "249E630"


def test_manual_dimension_names(micro_vu):
    assert len(micro_vu.manual_dimension_names) == 0
    micro_vu.manual_dimension_names = micro_vu.dimension_names
    assert len(micro_vu.manual_dimension_names) == 31
    micro_vu.manual_dimension_names = []


def test_op_number(micro_vu):
    assert micro_vu.op_number == "10"


def test_output_directory(micro_vu):
    assert micro_vu.output_directory == _get_output_directory()


def test_output_filepath(micro_vu):
    assert micro_vu.output_filepath == _get_output_filepath()


def test_part_number(micro_vu):
    assert micro_vu.part_number == "NN00160A001-2"


def test_prompt_insertion_index(micro_vu):
    assert micro_vu.prompt_insertion_index == 14


def test_report_filepath(micro_vu):
    micro_vu.report_filepath = "dave"
    assert micro_vu.report_filepath == "dave"
    micro_vu.report_filepath = "S:\\Micro-Vu\\446007 END VIEW_REV G_.pdf"
    assert micro_vu.report_filepath == "S:\\Micro-Vu\\446007 END VIEW_REV G_.pdf"


def test_rev_number(micro_vu):
    assert micro_vu.rev_number == "A"


def test_smartprofile_call_insertion_index(micro_vu):
    assert micro_vu.smartprofile_call_insertion_index == -1


def test_blank_smartprofile_projectname(micro_vu):
    assert micro_vu.smartprofile_projectname == ""


def test_view_name(micro_vu):
    assert micro_vu.view_name == "OPFAI REVC VMM"


def test_delete_line_containing_text(micro_vu):
    number_of_lines = len(micro_vu.file_lines)
    micro_vu.insert_line(10, "Prmt 0 1EFD3AA8 (Name \"Farfignugen #\") (ExpProps Ans) (Txt \"Farfignugen\")")
    micro_vu.delete_line_containing_text("Farfignugen")
    assert len(micro_vu.file_lines) == number_of_lines


def test_get_index_containing_text(micro_vu):
    assert micro_vu.get_index_containing_text("(Name \"Employee #") == 16


def test_insert_line(micro_vu):
    micro_vu.insert_line(10, "Farfignugen")
    assert micro_vu.file_lines[10].find("Farfignugen") > -1
    del micro_vu.file_lines[10]


def test_update_feature_name(micro_vu):
    micro_vu.update_feature_name(51, "Farfignugen")
    assert micro_vu.file_lines[51].find("Farfignugen") > -1
    micro_vu.update_feature_name(51, "18")
    assert micro_vu.file_lines[51].find("18") > -1


def test_update_instruction_count(micro_vu):
    micro_vu.insert_line(10, "Prmt 0 1EFD3AA8 (Name \"Farfignugen #\") (ExpProps Ans) (Txt \"Farfignugen\")")
    micro_vu.update_instruction_count()
    assert micro_vu.file_lines[3].find("Instructions 157") > -1
    micro_vu.delete_line_containing_text("Farfignugen")
    micro_vu.update_instruction_count()
    assert micro_vu.file_lines[3].find("Instructions 156") > -1
