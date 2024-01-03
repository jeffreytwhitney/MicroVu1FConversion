import os
import re
import shutil
from abc import ABCMeta, abstractmethod
from datetime import datetime
from pathlib import Path

import lib.Utilities
from lib import Utilities


def get_processor(input_filepath: str, op_num: str, user_initials: str, rev_number: str, smartprofile_file_name: str,
                  is_profile: bool):
    return (
        CoonRapidsProcessor(input_filepath, op_num, user_initials, rev_number, smartprofile_file_name, is_profile)
        if Utilities.GetStoredIniValue("Location", "Site", "Settings") == "CoonRapids"
        else AnokaProcessor(input_filepath, op_num, user_initials, rev_number, smartprofile_file_name, is_profile)
    )


def _get_filepath_by_name(file_name: str) -> str:
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == file_name:
                return os.path.join(root, file)
    return ""


def _get_microvu_version_from_filepath(program_filepath):
    if program_filepath.find("\\311\\") != -1:
        return "311"
    if program_filepath.find("\\341\\") != -1:
        return "341"
    if program_filepath.find("\\420\\") != -1:
        return "420"


def _get_utf_encoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    with open(file_path, "r", encoding='utf-16-le') as f:
        return f.readlines()


def _get_unencoded_file_lines(file_path: str) -> list[str]:
    if not file_path:
        return []
    with open(file_path, "r") as f:
        return f.readlines()


class Processor(metaclass=ABCMeta):
    def __init__(self, mv_input_filepath: str, op_num: str, user_initials: str, rev_number: str,
                 smartprofile_file_name: str, is_profile: bool):
        self.filepath = mv_input_filepath
        self.user_initials = user_initials
        self.input_filepath = mv_input_filepath
        self.smartprofile_filepath = smartprofile_file_name
        self.op_number = op_num
        self.is_profile = is_profile
        self.rev_number = rev_number
        self._load_data()

    @abstractmethod
    def _load_data(self):
        pass


class CoonRapidsProcessor(Processor):
    dimension_root: str

    def _load_data(self):
        self.file_lines = _get_utf_encoded_file_lines(self.filepath)
        self.part_number: str = self._get_part_number()
        self.view_name: str = self._get_view_name()
        self.output_filepath = _get_output_filepath(self.input_filepath)
        self.archive_filepath = _get_archive_filepath(self.input_filepath)
        self.dimension_root: str = lib.Utilities.GetStoredIniValue("GlobalSettings", "dimension_root", "Settings")

    def _global_replace(self, old_value: str, new_value: str) -> None:
        quoted_old_value = f"\"{old_value}\""
        quoted_new_value = f"\"{new_value}\""
        for i, l in enumerate(self.file_lines):
            if l.find(quoted_old_value) > 0:
                new_line = l.replace(quoted_old_value, quoted_new_value)
                self.file_lines[i] = new_line

    def _get_index_containing_text(self, text_to_find: str) -> int:
        return next(
            (i for i, l in enumerate(self.file_lines)
             if l.upper().find(text_to_find.upper()) > 1), 0
        )

    def _does_name_already_exist(self, name_to_find: str) -> bool:
        search_text = f"(Name \"{name_to_find}\")"
        return any(line.find(search_text) > 1 for line in self.file_lines)

    def _replace_export_filepath(self) -> None:
        line_idx = self._get_index_containing_text("AutoExpFile")
        if not line_idx:
            return
        line_text = self.file_lines[line_idx]
        export_filepath = self._get_export_filepath()
        updated_line_text = _set_node_text(line_text, "(ExpFile ", export_filepath, "\"")
        updated_line_text = _set_node_text(updated_line_text, "(AutoExpFile ", export_filepath, "\"")

        if self.is_profile:
            updated_line_text = updated_line_text.replace("(AutoExpFSApSt DT)", "(AutoExpFSApSt None)")
        else:
            updated_line_text = updated_line_text.replace("(AutoExpFSApSt None)", "(AutoExpFSApSt DT)")
        updated_line_text = updated_line_text.replace("(FldDlm Tab)", "(FldDlm CrLf)")
        self.file_lines[line_idx] = updated_line_text

    def _replace_report_filepath(self) -> None:
        line_idx = self._get_index_containing_text("AutoRptFileName")
        if not line_idx:
            return
        line_text = self.file_lines[line_idx]
        report_filepath = self._get_report_filepath()
        updated_line_text = _set_node_text(line_text, "(AutoRptFileName ", report_filepath, "\"")
        self.file_lines[line_idx] = updated_line_text

    def _update_comments(self) -> None:
        date_text = datetime.now().strftime("%m/%d/%Y")
        comment_idx = self._get_index_containing_text("(Name \"Edited")
        if not comment_idx:
            return
        new_comment = f"\\r\\nConverted program to work with 1Factory. {self.user_initials} {date_text}."
        current_comment = _get_node_text(self.file_lines[comment_idx], "(Txt ", "\"")
        current_comment += new_comment
        updated_comment_line = _set_node_text(self.file_lines[comment_idx], "(Txt ", current_comment, "\"")
        self.file_lines[comment_idx] = updated_comment_line

    def _delete_line_containing_text(self, text_to_find: str) -> None:
        idx_to_delete = self._get_index_containing_text(text_to_find)
        if idx_to_delete > 0:
            del self.file_lines[idx_to_delete]
        return

    def _replace_prompt_section(self) -> None:
        insert_index: int = self._get_index_containing_text("(Name \"Created")
        if not insert_index or not self.file_lines[insert_index].startswith("Txt"):
            raise ProcessorException("There is no 'Created By' line. Cannot process file.")

        temp_idx: int = self._get_index_containing_text("(Name \"Edited")
        if not temp_idx or not self.file_lines[temp_idx].startswith("Txt"):
            raise ProcessorException("There is no 'Edited By' line. Cannot process file.")

        insert_index = max(temp_idx, insert_index)
        self._delete_line_containing_text("Name \"PT #\"")
        self._delete_line_containing_text("Name \"Employee #\"")
        self._delete_line_containing_text("Name \"Machine #\"")
        self._delete_line_containing_text("Name \"PT#\"")
        self._delete_line_containing_text("Name \"Employee#\"")
        self._delete_line_containing_text("Name \"Machine#\"")
        self._delete_line_containing_text("Name \"Run-Setup\"")
        self._delete_line_containing_text("Name \"Job #\"")
        self._delete_line_containing_text("Name \"Job#\"")

        insert_index += 1
        pattern = 'sp_prompt_text.txt' if self.is_profile else 'prompt_text.txt'

        prompt_file = _get_filepath_by_name(pattern)
        if not prompt_file:
            raise ProcessorException("Can't find 'prompt_text' file.")

        prompt_lines = _get_utf_encoded_file_lines(prompt_file)
        if not prompt_lines:
            raise ProcessorException("Can't find 'prompt_text' file.")

        for line in prompt_lines:
            if line.find("(Name \"IN PROCESS\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"MACHINE\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"JOB\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"EMPLOYEE\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"OPERATION\")") > 0:
                line = line.replace("<O>", str(self.op_number))
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"REV LETTER\")") > 0:
                line = line.replace("<R>", str(self.rev_number))
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"PT\")") > 0:
                line = line.replace("<P>", str(self.part_number))
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"SEQUENCE\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"SPFILENAME\")") > 0:
                line = line.replace("<SPF>", str(self.smartprofile_filepath))
                self.file_lines.insert(insert_index, line)
                continue
        return

    def _replace_dimension_names(self) -> None:
        matches = ["(Name \"ITEM", "(Name \"INSP"]
        for i, line in enumerate(self.file_lines):
            if any(x in line for x in matches):
                if line.startswith("Calc"):
                    continue
                old_dimension_name = _get_node_text(line, "(Name ", "\"")
                new_dimension_name = _parse_dimension_name(old_dimension_name, self.dimension_root)
                if new_dimension_name == "":
                    continue
                if self._does_name_already_exist(new_dimension_name):
                    continue
                self.file_lines[i] = _set_node_text(line, "(Name ", new_dimension_name, "\"")

    def _get_last_microvu_system_id(self) -> str:
        last_system_reference_line = [line for line in self.file_lines if line.upper().find("(SYS ") > 1][-1]
        if last_system_reference_line.startswith("Sys 1"):
            return _get_node_text(last_system_reference_line, "Sys 1", " ")
        else:
            return _get_node_text(last_system_reference_line, "(Sys", " ", ")")

    def _get_instructions_count(self) -> str:
        return str(len([line for line in self.file_lines if line.find("(Name ") > 1]))

    def _update_instruction_count(self) -> None:
        instruction_count = self._get_instructions_count()
        idx: int = self._get_index_containing_text("AutoExpFile")
        self.file_lines[idx] = _set_node_text(self.file_lines[idx], "(InsIdx", instruction_count, " ", ")")
        instruction_line_idx = next((i for i, l in enumerate(self.file_lines) if l.startswith("Instructions")), 0)
        self.file_lines[instruction_line_idx] = _set_node_text(
            self.file_lines[instruction_line_idx], "Instructions", instruction_count, " ")
        return

    def _add_smart_profile_call(self):
        microvu_system_id: str = self._get_last_microvu_system_id()
        if not microvu_system_id:
            return

        smartprofile_filepath = _get_filepath_by_name('CallSmartProfile_text.txt')
        if not smartprofile_filepath:
            raise ProcessorException("Can't find 'CallSmartProfile_text' file.")

        prompt_lines = _get_unencoded_file_lines(smartprofile_filepath)
        if not prompt_lines:
            raise ProcessorException("Can't find 'CallSmartProfile_text' file.")

        smartprofile_line = prompt_lines[1]
        smartprofile_script_path = lib.Utilities.GetStoredIniValue("Paths", "smart_profile_script_filepath", "Settings")
        smartprofile_exe_path = lib.Utilities.GetStoredIniValue("Paths", "smart_profile_exe_filepath", "Settings")
        smartprofile_line = smartprofile_line.replace("<?SYS>", microvu_system_id)
        smartprofile_line = smartprofile_line.replace("<?EXE>", smartprofile_exe_path)
        smartprofile_line = smartprofile_line.replace("<?SCR>", smartprofile_script_path)
        self.file_lines.append(smartprofile_line)
        self.file_lines.append(prompt_lines[2])
        self.file_lines.append(prompt_lines[3])

    def _archive_file(self):
        if os.path.exists(self.output_filepath):
            file_name = Path(self.output_filepath).name
            dir_name = os.path.dirname(self.output_filepath)
            raise OutputFileExistsError(
                f"File '{file_name}' already exists in output directory '{dir_name}'."
            )
        os.makedirs(_get_archive_directory(self.filepath), exist_ok=True)
        os.makedirs(_get_output_directory(self.filepath), exist_ok=True)
        shutil.copy(self.filepath, self.archive_filepath)
        with open(self.output_filepath, 'w+', encoding='utf-16-le', newline='\r\n') as f:
            for line in self.file_lines:
                f.write(f"{line}")
        old_directory = os.path.dirname(self.filepath)
        os.remove(self.filepath)
        if len(os.listdir(old_directory)) == 0:
            os.rmdir(old_directory)

    def process_file(self) -> None:
        try:
            self._replace_export_filepath()
            if not self.is_profile:
                self._replace_report_filepath()
                self._replace_dimension_names()
            else:
                self._add_smart_profile_call()
            self._update_comments()
            self._replace_prompt_section()
            self._update_instruction_count()
            self._archive_file()
        except OutputFileExistsError as e:
            raise OutputFileExistsError(e.args[0]) from e
        except Exception as e:
            raise ProcessorException(e.args[0]) from e


class AnokaProcessor(CoonRapidsProcessor):
    def __init__(self, mv_input_filepath: str, op_num: str, user_initials: str, rev_number: str,
                 smartprofile_file_name: str, is_profile: bool):
        super().__init__(mv_input_filepath, op_num, user_initials, rev_number, smartprofile_file_name, is_profile)

    def _replace_prompt_section(self) -> None:
        try:
            super()._replace_prompt_section()
        except ProcessorException:
            self._anoka_replace_prompt_section()
        return

    def _anoka_replace_prompt_section(self) -> None:
        insert_idx: int = self._get_index_containing_text("(Name \"START")
        if insert_idx == 0:
            raise ProcessorException(f"Can't determine where to put the prompts. Cannot process file {Path(self.input_filepath).name}.")

        start_idx: int = self._get_index_containing_text("AutoExpFile")
        for idx in range(insert_idx, start_idx, -1):
            if self.file_lines[idx].startswith("Prmt"):
                del self.file_lines[idx]
        insert_index: int = self._get_index_containing_text("(Name \"START")
        pattern = 'sp_prompt_text.txt' if self.is_profile else 'prompt_text.txt'

        prompt_file = _get_filepath_by_name(pattern)
        if not prompt_file:
            raise ProcessorException("Can't find 'prompt_text' file.")

        prompt_lines = _get_utf_encoded_file_lines(prompt_file)
        if not prompt_lines:
            raise ProcessorException("Can't find 'prompt_text' file.")

        for line in prompt_lines:
            if line.find("(Name \"IN PROCESS\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"MACHINE\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"JOB\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"EMPLOYEE\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"OPERATION\")") > 0:
                line = line.replace("<O>", str(self.op_number))
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"REV LETTER\")") > 0:
                line = line.replace("<R>", str(self.rev_number))
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"PT\")") > 0:
                line = line.replace("<P>", str(self.part_number))
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"SEQUENCE\")") > 0:
                self.file_lines.insert(insert_index, line)
                continue
            if line.find("(Name \"SPFILENAME\")") > 0:
                line = line.replace("<SPF>", str(self.smartprofile_filepath))
                self.file_lines.insert(insert_index, line)
                continue
        return

    def process_file(self) -> None:
        try:
            self._replace_export_filepath()
            if self.is_profile:
                self._add_smart_profile_call()
            self._update_comments()
            self._replace_prompt_section()
            if os.path.exists(self.output_filepath):
                os.remove(self.output_filepath)
            self._update_instruction_count()
            self._archive_file()
        except OutputFileExistsError as e:
            raise OutputFileExistsError(e.args[0]) from e
        except Exception as e:
            raise ProcessorException(e.args[0]) from e


class ProcessorException(Exception):
    pass


class OutputFileExistsError(Exception):
    pass


class MicroVuProgram:

    def __init__(self, input_filepath: str, op_number: str, rev_number: str):
        self.filepath = input_filepath
        self.op_number = op_number
        self.rev_number = rev_number

    @staticmethod
    def _parse_dimension_name(dimension_name: str, dimension_root: str) -> str:
        dim_parts = re.split("[ _Xx.-]", dimension_name)
        while "" in dim_parts:
            dim_parts.remove("")
        if len(dim_parts) == 1:
            dim_part = dim_parts[0]
            dim_part = dim_part.upper().replace("INSP", "").replace("ITEM", "")
            if dim_part.isnumeric():
                return dim_part
            elif dim_part[:-1].isnumeric():
                return dim_part
        if len(dim_parts) == 2 and dim_parts[1].isnumeric():
            return f"{dimension_root}{dim_parts[1]}"
        if len(dim_parts) == 2:
            last_part = dim_parts[1][:-1]
            if last_part.isnumeric():
                return f"{dimension_root}{dim_parts[1]}"
        if dim_parts[1].isnumeric() and dim_parts[2].isnumeric():
            charstr = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            chars = list(charstr)
            return f"{dimension_root}{dim_parts[1]}{chars[int(dim_parts[2])]}"
        if dim_parts[1].isnumeric() and dim_parts[2].isalpha() and len(dim_parts[2]) == 1:
            return f"{dimension_root}{dim_parts[1]}{dim_parts[2]}"
        return ""

    @staticmethod
    def _get_node_text(line_text: str, search_value: str, start_delimiter: str, end_delimiter: str = "") -> str:
        if not end_delimiter:
            end_delimiter = start_delimiter
        title_index: int = line_text.upper().find(search_value.upper())
        begin_index: int = line_text.find(start_delimiter, title_index + len(search_value))
        end_index: int = line_text.find(end_delimiter, begin_index + 1)
        if end_index == -1:
            end_index = len(line_text)
        return line_text[begin_index + 1:end_index].strip()

    @staticmethod
    def _set_node_text(line_text: str, search_value: str, set_value: str, start_delimiter: str,
                       end_delimiter: str = "") -> str:
        current_value: str = MicroVuProgram._get_node_text(line_text, search_value, start_delimiter, end_delimiter)
        current_node: str = search_value + start_delimiter + current_value + end_delimiter
        new_node: str = search_value + start_delimiter + set_value + end_delimiter
        return line_text.replace(current_node, new_node)

    @staticmethod
    def _get_increment_filename(file_name: str, increment: int) -> str:
        file_stem = Path(file_name).stem
        file_extension = Path(file_name).suffix
        return f"{file_stem}-{increment}{file_extension}"

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
    def export_filepath(self) -> str:
        part_rev = f"REV{self.rev_number}"
        export_filepath = "C:\\Users\\Public\\CURL\\in\\"
        export_filepath += self.part_number
        export_filepath += f"_OP{self.op_number}"
        if len(self.view_name) > 0:
            export_filepath += f"_{self.view_name}"
        export_filepath += f"_{part_rev}"
        export_filepath += "_.csv"
        return export_filepath

    @property
    def report_filepath(self) -> str:
        view_name = self.view_name
        part_rev = f"REV{self.rev_number}"
        report_filepath: str = Utilities.GetStoredIniValue("Paths", "reporting_root_path", "Settings")
        report_filepath += self.part_number
        report_filepath += f"_OP{self.op_number}"
        if len(view_name) > 0:
            report_filepath += f"_{view_name}"
        report_filepath += f"_{part_rev}_.pdf"
        return report_filepath

    @property
    def output_directory(self) -> str:
        output_rootpath = lib.Utilities.GetStoredIniValue("Paths", "output_rootpath", "Settings")
        microvu_version = _get_microvu_version_from_filepath(self.filepath)
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
    def is_writable(self) -> bool:
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
                increment_filename = MicroVuProgram._get_increment_filename(archive_filename, increment)
                archive_filepath = os.path.join(archive_directory, increment_filename)
                if not os.path.exists(archive_filepath):
                    break
        return archive_filepath

    @property
    def archive_directory(self) -> str:
        archive_root_directory = lib.Utilities.GetStoredIniValue("Paths", "archive_root_directory", "Settings")
        microvu_version = _get_microvu_version_from_filepath(self.filepath)
        parts = Path(self.filepath).parts
        machine_type_idx = parts.index(microvu_version)
        program_idx = parts.index(microvu_version) + 2
        program_directory = parts[program_idx]
        for i in range(program_idx + 1, len(parts) - 1):
            program_directory = os.path.join(program_directory, parts[i])
        machine_type_directory = parts[machine_type_idx]
        parent_directory = Path(program_directory, machine_type_directory)
        return str(Path(archive_root_directory, parent_directory))


class SmartProfileMicroVuProgram(MicroVuProgram):
    def __init__(self, input_filepath: str, op_number: str, rev_number: str, smartprofile_file_name: str):
        super().__init__(input_filepath, op_number, rev_number)
        self.smartprofile_file_name = smartprofile_file_name

    @property
    def export_filepath(self) -> str:
        return "C:\\TEXT\\OUTPUT.txt"

    @property
    def report_filepath(self) -> str:
        return ""
