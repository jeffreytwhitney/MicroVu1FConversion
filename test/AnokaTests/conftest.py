import configparser
import os
import pathlib


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


def pytest_configure(config):
    config_filepath = _get_filepath_by_name("TESTSettings.ini")
    os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = config_filepath
    input_path = _get_input_root_path()
    output_path = _get_output_root_path()
    _store_ini_value(input_path, "Paths", "input_rootpath")
    _store_ini_value(output_path, "Paths", "output_rootpath")
    _delete_all_files_in_output_directory()
    if not os.path.exists(output_path):
        os.mkdir(output_path)


def pytest_unconfigure(config):
    os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = ""
    _delete_all_files_in_output_directory()