import os
import pytest


def _get_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)
    return ""



def setup_module():
    config_filepath = _get_filepath_by_name("TESTSettings.ini")
    os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = config_filepath

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


def test_update_instruction_count(self):
    self.fail()


def main():
    tester = TestMicroVuProgram()


if __name__ == "__main__":
    main()
