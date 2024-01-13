import configparser
import os


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


def test_get_node_text(self):
    self.fail()


def test_set_node_text(self):
    self.fail()


def test__does_name_already_exist(self):
    self.fail()


def test__get_instructions_count(self):
    self.fail()


def test__global_replace(self):
    self.fail()


def test__postinit(self):
    self.fail()


def test__set_has_calculators(self):
    self.fail()


def test__set_smartprofile(self):
    self.fail()


def test_can_write_to_output_file(self):
    self.fail()


def test_comment(self):
    self.fail()


def test_set_comment(self):
    self.fail()


def test_dimension_names(self):
    self.fail()


def test_export_filepath(self):
    self.fail()


def test_set_export_filepath(self):
    self.fail()


def test_filename(self):
    self.fail()


def test_filepath(self):
    self.fail()


def test_has_calculators(self):
    self.fail()


def test_get_existing_smartprofile_call_index(self):
    self.fail()


def test_is_smartprofile(self):
    self.fail()


def test_last_microvu_system_id(self):
    self.fail()


def test_manual_dimension_names(self):
    self.fail()


def test_set_manual_dimension_names(self):
    self.fail()


def test_op_number(self):
    self.fail()


def test_output_directory(self):
    self.fail()


def test_output_filepath(self):
    self.fail()


def test_part_number(self):
    self.fail()


def test_prompt_insertion_index(self):
    self.fail()


def test_report_filepath(self):
    self.fail()


def test_set_report_filepath(self):
    self.fail()


def test_rev_number(self):
    self.fail()


def test_smartprofile_call_insertion_index(self):
    self.fail()


def test_smartprofile_projectname(self):
    self.fail()


def test_view_name(self):
    self.fail()


def test_delete_line_containing_text(self):
    self.fail()


def test_get_index_containing_text(self):
    self.fail()


def test_insert_line(self):
    self.fail()


def test_update_feature_name(self):
    self.fail()


def test_update_instruction_count():
    assert fail



