import os
from datetime import datetime

from lib import Utilities
import configparser

import random
import string


def _delete_all_files_in_output_directory():
    for root, dirs, files in os.walk(_get_output_root_path()):
        for item in files:
            filespec = os.path.join(root, item)
            os.unlink(filespec)


def _get_filepath_by_name(file_name: str) -> str:
    current_dir = os.path.dirname(__file__)
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file == file_name:
                return str(os.path.join(root, file))
    return ""


def _get_dot_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)
    return ""


def _get_input_root_path() -> str:
    current_dir = os.path.dirname(__file__)
    return str(os.path.join(current_dir, "Input"))


def _get_output_root_path() -> str:
    current_dir = os.path.dirname(__file__)
    return str(os.path.join(current_dir, "Output"))


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
    config_filepath = _get_filepath_by_name("TESTSettings.ini")
    os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = config_filepath
    input_path = _get_input_root_path()
    output_path = _get_output_root_path()
    _store_ini_value(input_path, "Paths", "input_rootpath")
    _store_ini_value(output_path, "Paths", "output_rootpath")


def teardown_module():
    os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = ""
    _delete_all_files_in_output_directory()


def test_get_ini_file_path():
    config_filepath = _get_filepath_by_name("TESTSettings.ini")
    ini_filepath = Utilities.GetIniFilePath("TESTSettings.ini")
    assert ini_filepath == config_filepath


def test_get_stored_ini_value():
    assert Utilities.GetStoredIniValue("Paths", "output_rootpath", "Settings") == _get_output_root_path()


def test_store_ini_value():
    initials = "".join(random.choices(string.ascii_uppercase, k=3))
    Utilities.StoreIniValue(initials, "UserSettings", "initials", "Settings")
    assert _get_stored_ini_value("UserSettings", "initials") == initials


def test_get_unencoded_file_lines():
    current_dir = os.path.dirname(__file__)
    input_filepath = str(os.path.join(current_dir, "UnencodedFile.txt"))
    lines = Utilities.get_unencoded_file_lines(input_filepath)
    assert len(lines) == 4


def test_get_utf_encoded_file_lines():
    input_filepath = str(os.path.join(_get_input_root_path(), "446007 END VIEW.iwp"))
    lines = Utilities.get_utf_encoded_file_lines(input_filepath)
    assert len(lines) == 245
    assert lines[1].startswith("Programs")


def test_get_filepath_by_name():
    config_filepath = _get_dot_filepath_by_name("TESTSettings.ini")
    ini_filepath = Utilities.get_filepath_by_name("TESTSettings.ini")
    assert ini_filepath == config_filepath


def test_get_file_as_string():
    current_dir = os.path.dirname(__file__)
    input_filepath = str(os.path.join(current_dir, "UnencodedFile.txt"))
    file_string = Utilities.get_file_as_string(input_filepath)
    assert file_string


def test_write_lines_to_file():
    date_text = datetime.now().strftime("%m_%d_%Y")
    file_name = f"test_{date_text}.txt"
    output_filepath = str(os.path.join(_get_output_root_path(), file_name))
    current_dir = os.path.dirname(__file__)
    input_filepath = str(os.path.join(current_dir, "UnencodedFile.txt"))
    lines = _get_unencoded_file_lines(input_filepath)
    Utilities.write_lines_to_file(output_filepath, lines)
    assert os.path.exists(output_filepath)
    output_lines = _get_unencoded_file_lines(output_filepath)
    assert lines == output_lines
