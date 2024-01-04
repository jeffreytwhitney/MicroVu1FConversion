import os
import re
from pathlib import Path

import lib.Utilities
from lib.Utilities import get_utf_encoded_file_lines, get_filepath_by_name


class DimensionName:

    def __init__(self, index: int, name: str):
        self.index = index
        self.name = name


class MicroVuProgram:
    # Static Methods
    @staticmethod
    def get_node_text(line_text: str, search_value: str, start_delimiter: str, end_delimiter: str = "") -> str:
        if not end_delimiter:
            end_delimiter = start_delimiter
        title_index: int = line_text.upper().find(search_value.upper())
        begin_index: int = line_text.find(start_delimiter, title_index + len(search_value))
        end_index: int = line_text.find(end_delimiter, begin_index + 1)
        if end_index == -1:
            end_index = len(line_text)
        return line_text[begin_index + 1:end_index].strip()

    @staticmethod
    def set_node_text(line_text: str, search_value: str, set_value: str, start_delimiter: str,
                      end_delimiter: str = "") -> str:
        current_value: str = MicroVuProgram.get_node_text(line_text, search_value, start_delimiter, end_delimiter)
        current_node: str = search_value + start_delimiter + current_value + end_delimiter
        new_node: str = search_value + start_delimiter + set_value + end_delimiter
        return line_text.replace(current_node, new_node)

    @staticmethod
    def get_increment_filename(file_name: str, increment: int) -> str:
        file_stem = Path(file_name).stem
        file_extension = Path(file_name).suffix
        return f"{file_stem}-{increment}{file_extension}"

    @staticmethod
    def get_microvu_version_from_filepath(program_filepath):
        if program_filepath.find("\\311\\") != -1:
            return "311"
        if program_filepath.find("\\341\\") != -1:
            return "341"
        if program_filepath.find("\\420\\") != -1:
            return "420"

    # Dunder Methods
    def __init__(self, input_filepath: str, op_number: str, rev_number: str):
        self.filepath = input_filepath
        self.file_lines = get_utf_encoded_file_lines(self.filepath)
        self.op_num = op_number
        self.rev_num = rev_number

    # Internal Methods
    def _get_index_containing_text(self, text_to_find: str) -> int:
        return next(
                (i for i, l in enumerate(self.file_lines)
                 if l.upper().find(text_to_find.upper()) > 1), 0
        )

    def _get_instructions_count(self) -> str:
        return str(len([line for line in self.file_lines if line.find("(Name ") > 1]))

    def _global_replace(self, old_value: str, new_value: str) -> None:
        quoted_old_value = f"\"{old_value}\""
        quoted_new_value = f"\"{new_value}\""
        for i, l in enumerate(self.file_lines):
            if l.find(quoted_old_value) > 0:
                new_line = l.replace(quoted_old_value, quoted_new_value)
                self.file_lines[i] = new_line

    def _does_name_already_exist(self, name_to_find: str) -> bool:
        search_text = f"(Name \"{name_to_find}\")"
        return any(line.find(search_text) > 1 for line in self.file_lines)

    # Properties
    @property
    def last_microvu_system_id(self) -> str:
        last_system_reference_line = [line for line in self.file_lines if line.upper().find("(SYS ") > 1][-1]
        if last_system_reference_line.startswith("Sys 1"):
            return MicroVuProgram.get_node_text(last_system_reference_line, "Sys 1", " ")
        else:
            return MicroVuProgram.get_node_text(last_system_reference_line, "(Sys", " ", ")")

    @property
    def prompt_filename(self) -> str:
        return 'prompt_text.txt'

    @property
    def prompt_insertion_index(self) -> int:
        insert_index: int = self._get_index_containing_text("(Name \"Created")
        if not insert_index or not self.file_lines[insert_index].startswith("Txt"):
            return -1

        temp_idx: int = self._get_index_containing_text("(Name \"Edited")
        if not temp_idx or not self.file_lines[temp_idx].startswith("Txt"):
            return -1
        return max(temp_idx, insert_index)

    @property
    def smartprofile_call_insertion_index(self) -> int:
        return -1

    @property
    def smartprofile_filepath(self) -> str:
        return ""

    @property
    def rev_number(self) -> str:
        return self.rev_num

    @property
    def op_number(self) -> str:
        return self.op_num

    @property
    def part_number(self) -> str:
        filename = Path(self.filepath).stem
        parts = re.split("[ _]", filename)
        return parts[0]

    @property
    def view_name(self) -> str:
        rev_begin_idx = 0
        rev_end_idx = 0
        view_name = ""

        filename = Path(self.filepath).stem
        filename_parts = re.split("[ _]", filename)
        count_of_parts = len(filename_parts)
        if count_of_parts == 1:
            return ""
        for x in range(len(filename_parts)):
            if filename_parts[x].upper().startswith("REV"):
                rev_begin_idx = x
                if filename_parts[rev_begin_idx].upper() == "REV":
                    rev_end_idx = rev_begin_idx + 1
                else:
                    rev_end_idx = rev_begin_idx

        if rev_begin_idx == 0:
            for part in range(1, len(filename_parts)):
                view_name += f"{filename_parts[part]} "
        elif rev_begin_idx == 1 and rev_end_idx < count_of_parts - 1:
            for part in range(rev_end_idx, len(filename_parts)):
                view_name += f"{filename_parts[part]} "
        else:
            for part in range(1, rev_end_idx):
                view_name += f"{filename_parts[part]} "
        return view_name.strip()

    @property
    def comment(self) -> str:
        if comment_idx := self._get_index_containing_text("(Name \"Edited"):
            return MicroVuProgram.get_node_text(self.file_lines[comment_idx], "(Txt ", "\"")
        else:
            return ""

    @comment.setter
    def comment(self, value: str) -> None:
        if line_idx := self._get_index_containing_text("(Name \"Edited"):
            updated_comment_line = MicroVuProgram.set_node_text(self.file_lines[line_idx], "(Txt ", value, "\"")
            self.file_lines[line_idx] = updated_comment_line

    @property
    def export_filepath(self) -> str:
        if line_idx := self._get_index_containing_text("AutoExpFile"):
            return MicroVuProgram.get_node_text(self.file_lines[line_idx], "AutoExpFile", "\"")
        else:
            return ""

    @export_filepath.setter
    def export_filepath(self, value: str) -> None:
        line_idx = self._get_index_containing_text("AutoExpFile")
        if not line_idx:
            return
        line_text = self.file_lines[line_idx]
        updated_line_text = MicroVuProgram.set_node_text(line_text, "(ExpFile ", value, "\"")
        updated_line_text = MicroVuProgram.set_node_text(updated_line_text, "(AutoExpFile ", value, "\"")
        updated_line_text = updated_line_text.replace("(AutoExpFSApSt None)", "(AutoExpFSApSt DT)")
        updated_line_text = updated_line_text.replace("(FldDlm Tab)", "(FldDlm CrLf)")
        self.file_lines[line_idx] = updated_line_text

    @property
    def report_filepath(self) -> str:
        if line_idx := self._get_index_containing_text("AutoRptFileName"):
            return MicroVuProgram.get_node_text(self.file_lines[line_idx], "AutoRptFileName", "\"")
        else:
            return ""

    @report_filepath.setter
    def report_filepath(self, value: str) -> None:
        line_idx = self._get_index_containing_text("AutoRptFileName")
        if not line_idx:
            return
        line_text = self.file_lines[line_idx]
        updated_line_text = MicroVuProgram.set_node_text(line_text, "(AutoRptFileName ", value, "\"")
        self.file_lines[line_idx] = updated_line_text

    @property
    def output_directory(self) -> str:
        output_rootpath = lib.Utilities.GetStoredIniValue("Paths", "output_rootpath", "Settings")
        microvu_version = MicroVuProgram.get_microvu_version_from_filepath(self.filepath)
        parts = Path(self.filepath).parts
        machine_type_idx = parts.index(microvu_version)
        program_idx = parts.index(microvu_version) + 2
        program_directory = parts[program_idx]
        for i in range(program_idx + 1, len(parts) - 1):
            program_directory = os.path.join(program_directory, parts[i])
        machine_type_directory = parts[machine_type_idx]
        parent_directory = Path(machine_type_directory, program_directory)
        return str(Path(output_rootpath, parent_directory))

    @property
    def output_filepath(self) -> str:
        output_directory = self.output_directory
        file_name = Path(self.filepath).name
        return str(Path(output_directory, file_name))

    @property
    def can_write_to_output_file(self) -> bool:
        return True

    @property
    def archive_filepath(self) -> str:
        archive_directory = self.archive_directory
        archive_filename = Path(self.filepath).name
        archive_filepath = os.path.join(archive_directory, archive_filename)
        if os.path.exists(archive_filepath):
            increment = 0
            while True:
                increment += 1
                increment_filename = MicroVuProgram.get_increment_filename(archive_filename, increment)
                archive_filepath = os.path.join(archive_directory, increment_filename)
                if not os.path.exists(archive_filepath):
                    break
        return archive_filepath

    @property
    def archive_directory(self) -> str:
        archive_root_directory = lib.Utilities.GetStoredIniValue("Paths", "archive_root_directory", "Settings")
        microvu_version = MicroVuProgram.get_microvu_version_from_filepath(self.filepath)
        parts = Path(self.filepath).parts
        machine_type_idx = parts.index(microvu_version)
        program_idx = parts.index(microvu_version) + 2
        program_directory = parts[program_idx]
        for i in range(program_idx + 1, len(parts) - 1):
            program_directory = os.path.join(program_directory, parts[i])
        machine_type_directory = parts[machine_type_idx]
        parent_directory = Path(program_directory, machine_type_directory)
        return str(Path(archive_root_directory, parent_directory))

    @property
    def dimension_names(self) -> list[DimensionName]:
        dimensions: list[DimensionName] = []
        matches = ["(Name \"ITEM", "(Name \"INSP"]
        for i, line in enumerate(self.file_lines):
            if any(x in line for x in matches):
                if line.startswith("Calc"):
                    continue
                old_dimension_name = MicroVuProgram.get_node_text(line, "(Name ", "\"")
                dimension = DimensionName(i, old_dimension_name)
                dimensions.append(dimension)
        return dimensions

    # Public Methods
    def delete_line_containing_text(self, text_to_find: str) -> None:
        idx_to_delete = self._get_index_containing_text(text_to_find)
        if idx_to_delete > 0:
            del self.file_lines[idx_to_delete]
        return

    def update_instruction_count(self) -> None:
        instruction_count = self._get_instructions_count()
        idx: int = self._get_index_containing_text("AutoExpFile")
        self.file_lines[idx] = MicroVuProgram.set_node_text(
                self.file_lines[idx], "(InsIdx", instruction_count, " ", ")")
        instruction_line_idx = next((i for i, l in enumerate(self.file_lines) if l.startswith("Instructions")), 0)
        self.file_lines[instruction_line_idx] = MicroVuProgram.set_node_text(
                self.file_lines[instruction_line_idx], "Instructions", instruction_count, " ")
        return

    def update_feature_name(self, line_index: int, feature_name: str) -> None:
        if self._does_name_already_exist(feature_name):
            return
        current_line = self.file_lines[line_index]
        self.file_lines[line_index] = MicroVuProgram.set_node_text(current_line, "(Name ", feature_name, "\"")


class SmartProfileMicroVuProgram(MicroVuProgram):
    def __init__(self, input_filepath: str, op_number: str, rev_number: str, smartprofile_file_name: str):
        super().__init__(input_filepath, op_number, rev_number)
        self.smartprofile_file_name = smartprofile_file_name

    @property
    def smartprofile_call_insertion_index(self) -> int:
        return len(self.file_lines)

    @property
    def smartprofile_filepath(self) -> str:
        if smartprofile_filepath := get_filepath_by_name(
                'CallSmartProfile_text.txt'
        ):
            return smartprofile_filepath
        else:
            raise MicroVuException("Can't find 'CallSmartProfile_text' file.")

    @property
    def export_filepath(self) -> str:
        return "C:\\TEXT\\OUTPUT.txt"

    @property
    def report_filepath(self) -> str:
        return ""

    @report_filepath.setter
    def report_filepath(self, value: str) -> None:
        line_idx = self._get_index_containing_text("AutoRptFileName")
        if not line_idx:
            return
        line_text = self.file_lines[line_idx]
        updated_line_text = MicroVuProgram.set_node_text(line_text, "(AutoRptFileName ", value, "\"")
        self.file_lines[line_idx] = updated_line_text
        line_idx = self._get_index_containing_text("AutoRptFileName")
        if not line_idx:
            return
        line_text = self.file_lines[line_idx]
        updated_line_text = MicroVuProgram.set_node_text(line_text, "(AutoRptFileName ", "", "\"")
        self.file_lines[line_idx] = updated_line_text

    @property
    def prompt_filename(self) -> str:
        return 'sp_prompt_text.txt'

    @property
    def dimension_names(self) -> list[DimensionName]:
        return []

    @export_filepath.setter
    def export_filepath(self, value: str) -> None:
        line_idx = self._get_index_containing_text("AutoExpFile")
        if not line_idx:
            return
        line_text = self.file_lines[line_idx]
        updated_line_text = MicroVuProgram.set_node_text(line_text, "(ExpFile ", value, "\"")
        updated_line_text = MicroVuProgram.set_node_text(updated_line_text, "(AutoExpFile ", value, "\"")
        updated_line_text = updated_line_text.replace("(AutoExpFSApSt DT)", "(AutoExpFSApSt None)")
        updated_line_text = updated_line_text.replace("(FldDlm Tab)", "(FldDlm CrLf)")
        self.file_lines[line_idx] = updated_line_text


class MicroVuException(Exception):
    pass
