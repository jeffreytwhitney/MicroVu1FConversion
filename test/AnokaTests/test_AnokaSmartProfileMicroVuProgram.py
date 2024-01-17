import configparser
import os
import pathlib
import shutil

import pytest

from lib.MicroVuProgram import MicroVuProgram


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
def micro_vu() -> MicroVuProgram:
    return MicroVuProgram(_get_input_filepath("110047396A0_OPFAI_REVA_SP.iwp"), "10", "A", "110047396A0_OPFAI_REVA_SP.iwp")


def test_can_write_to_output_file(micro_vu):
    assert micro_vu.can_write_to_output_file is True
    shutil.copy(_get_input_filepath("110047396A0_OPFAI_REVA_SP.iwp"), _get_output_filepath("110047396A0_OPFAI_REVA_SP.iwp"))
    assert micro_vu.can_write_to_output_file is False
    _delete_all_files_in_output_directory()


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
    assert micro_vu.filepath == _get_input_filepath("110047396A0_OPFAI_REVA_SP.iwp")


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
    assert micro_vu.output_directory == _get_output_directory()


def test_output_filepath(micro_vu):
    assert micro_vu.output_filepath == _get_output_filepath("110047396A0_OPFAI_REVA_SP.iwp")


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
