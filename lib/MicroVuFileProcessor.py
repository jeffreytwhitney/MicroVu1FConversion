import os
import re
import shutil
from abc import ABCMeta, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List

import lib.Utilities
from lib import Utilities
from lib.MicroVuProgram import MicroVuProgram, MicroVuException, DimensionName
from lib.Utilities import get_unencoded_file_lines, get_utf_encoded_file_lines, get_filepath_by_name


def get_processor(user_initials: str):
    return (
            CoonRapidsProcessor(user_initials)
            if Utilities.GetStoredIniValue("Location", "Site", "Settings") == "CoonRapids"
            else AnokaProcessor(user_initials)
    )


class Processor(metaclass=ABCMeta):
    dimension_root: str
    _microvu_programs: List[MicroVuProgram]

    def __init__(self, user_initials: str):
        self.user_initials = user_initials
        self.dimension_root: str = lib.Utilities.GetStoredIniValue("GlobalSettings", "dimension_root", "Settings")

    @property
    def micro_vu_programs(self) -> list[MicroVuProgram]:
        return self._microvu_programs

    def add_micro_vu_program(self, micro_vu: MicroVuProgram):
        self._microvu_programs.append(micro_vu)

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

    @abstractmethod
    def process_files(self) -> None:
        pass


class CoonRapidsProcessor(Processor):

    def _replace_export_filepath(self, micro_vu: MicroVuProgram) -> None:
        part_rev = f"REV{micro_vu.rev_number}"
        export_filepath: str = "C:\\Users\\Public\\CURL\\in\\"
        export_filepath += micro_vu.part_number
        export_filepath += f"_OP{micro_vu.op_number}"
        view_name = str(micro_vu.view_name)
        if view_name != "":
            export_filepath += f"_{micro_vu.view_name}"
        export_filepath += f"_{part_rev}"
        export_filepath += "_.csv"
        micro_vu.export_filepath = export_filepath

    def _replace_report_filepath(self, micro_vu: MicroVuProgram) -> None:
        view_name = micro_vu.view_name
        part_rev = f"REV{micro_vu.rev_number}"
        report_filepath: str = Utilities.GetStoredIniValue("Paths", "reporting_root_path", "Settings")
        report_filepath += micro_vu.part_number
        report_filepath += f"_OP{micro_vu.op_number}"
        if len(view_name) > 0:
            report_filepath += f"_{view_name}"
        report_filepath += f"_{part_rev}_.pdf"
        micro_vu.report_filepath = report_filepath

    def _update_comments(self, micro_vu: MicroVuProgram) -> None:
        date_text = datetime.now().strftime("%m/%d/%Y")
        new_comment = f"\\r\\nConverted program to work with 1Factory. {self.user_initials} {date_text}."
        current_comment = micro_vu.comment
        current_comment += new_comment
        micro_vu.comment = current_comment

    def _replace_prompt_section(self, micro_vu: MicroVuProgram) -> None:
        insert_index = micro_vu.prompt_insertion_index
        if insert_index == -1:
            raise ProcessorException("There is either no 'Edited By' or 'Created By' line. Cannot process file.")

        micro_vu.delete_line_containing_text("Name \"PT #\"")
        micro_vu.delete_line_containing_text("Name \"Employee #\"")
        micro_vu.delete_line_containing_text("Name \"Machine #\"")
        micro_vu.delete_line_containing_text("Name \"PT#\"")
        micro_vu.delete_line_containing_text("Name \"Employee#\"")
        micro_vu.delete_line_containing_text("Name \"Machine#\"")
        micro_vu.delete_line_containing_text("Name \"Run-Setup\"")
        micro_vu.delete_line_containing_text("Name \"Job #\"")
        micro_vu.delete_line_containing_text("Name \"Job#\"")

        insert_index += 1
        pattern = micro_vu.prompt_filename

        prompt_file = get_filepath_by_name(pattern)
        if not prompt_file:
            raise ProcessorException("Can't find 'prompt_text' file.")

        prompt_lines = get_utf_encoded_file_lines(prompt_file)
        if not prompt_lines:
            raise ProcessorException("Can't find 'prompt_text' file.")

        for line in prompt_lines:
            if line.find("(Name \"IN PROCESS\")") > 0:
                micro_vu.insert_line(insert_index, line)
                continue
            if line.find("(Name \"MACHINE\")") > 0:
                micro_vu.insert_line(insert_index, line)
                continue
            if line.find("(Name \"JOB\")") > 0:
                micro_vu.insert_line(insert_index, line)
                continue
            if line.find("(Name \"EMPLOYEE\")") > 0:
                micro_vu.insert_line(insert_index, line)
                continue
            if line.find("(Name \"OPERATION\")") > 0:
                line = line.replace("<O>", str(micro_vu.op_number))
                micro_vu.insert_line(insert_index, line)
                continue
            if line.find("(Name \"REV LETTER\")") > 0:
                line = line.replace("<R>", str(micro_vu.rev_number))
                micro_vu.insert_line(insert_index, line)
                continue
            if line.find("(Name \"PT\")") > 0:
                line = line.replace("<P>", str(micro_vu.part_number))
                micro_vu.insert_line(insert_index, line)
                continue
            if line.find("(Name \"SEQUENCE\")") > 0:
                micro_vu.insert_line(insert_index, line)
                continue
            if line.find("(Name \"SPFILENAME\")") > 0:
                try:
                    smartprofile_filepath = micro_vu.smartprofile_filepath
                except MicroVuException as e:
                    raise ProcessorException(e.args[0]) from e
                line = line.replace("<SPF>", smartprofile_filepath)
                micro_vu.insert_line(insert_index, line)
                continue
        return

    def _replace_dimension_names(self, micro_vu: MicroVuProgram) -> None:
        dimension_names: list[DimensionName] = micro_vu.dimension_names
        for dimension_name in dimension_names:
            new_dimension_name = Processor._parse_dimension_name(dimension_name.name, self.dimension_root)
            micro_vu.update_feature_name(dimension_name.index, new_dimension_name)

    def _add_smart_profile_call(self, micro_vu: MicroVuProgram):

        smartprofile_call_insertion_index = micro_vu.smartprofile_call_insertion_index
        if smartprofile_call_insertion_index == -1:
            return

        microvu_system_id: str = micro_vu.last_microvu_system_id
        if not microvu_system_id:
            return

        smartprofile_filepath = get_filepath_by_name('CallSmartProfile_text.txt')
        if not smartprofile_filepath:
            raise ProcessorException("Can't find 'CallSmartProfile_text' file.")

        prompt_lines = get_unencoded_file_lines(smartprofile_filepath)
        if not prompt_lines:
            raise ProcessorException("Can't find 'CallSmartProfile_text' file.")

        smartprofile_line = prompt_lines[1]
        smartprofile_script_path = lib.Utilities.GetStoredIniValue("Paths", "smart_profile_script_filepath", "Settings")
        smartprofile_exe_path = lib.Utilities.GetStoredIniValue("Paths", "smart_profile_exe_filepath", "Settings")
        smartprofile_line = smartprofile_line.replace("<?SYS>", microvu_system_id)
        smartprofile_line = smartprofile_line.replace("<?EXE>", smartprofile_exe_path)
        smartprofile_line = smartprofile_line.replace("<?SCR>", smartprofile_script_path)
        micro_vu.file_lines.append(smartprofile_line)
        micro_vu.file_lines.append(prompt_lines[2])
        micro_vu.file_lines.append(prompt_lines[3])

    def _archive_file(self, micro_vu: MicroVuProgram):
        if os.path.exists(micro_vu.output_filepath):
            file_name = Path(micro_vu.output_filepath).name
            dir_name = os.path.dirname(micro_vu.output_filepath)
            raise ProcessorException(
                    f"File '{file_name}' already exists in output directory '{dir_name}'."
            )
        os.makedirs(micro_vu.archive_directory, exist_ok=True)
        os.makedirs(micro_vu.output_directory, exist_ok=True)
        shutil.copy(micro_vu.filepath, micro_vu.archive_filepath)
        with open(micro_vu.output_filepath, 'w+', encoding='utf-16-le', newline='\r\n') as f:
            for line in micro_vu.file_lines:
                f.write(f"{line}")
        old_directory = os.path.dirname(micro_vu.filepath)
        os.remove(micro_vu.filepath)
        if len(os.listdir(old_directory)) == 0:
            os.rmdir(old_directory)

    def process_files(self) -> None:
        try:
            for micro_vu in self.micro_vu_programs:
                self._replace_export_filepath(micro_vu)
                self._replace_report_filepath(micro_vu)
                self._replace_dimension_names(micro_vu)
                self._add_smart_profile_call(micro_vu)
                self._update_comments(micro_vu)
                self._replace_prompt_section(micro_vu)
                micro_vu.update_instruction_count()
                self._archive_file(micro_vu)
        except Exception as e:
            raise ProcessorException(e.args[0]) from e


class AnokaProcessor(CoonRapidsProcessor):
    def __init__(self, user_initials: str):
        super().__init__(user_initials)

    def _replace_prompt_section(self, micro_vu: MicroVuProgram) -> None:
        try:
            super()._replace_prompt_section(micro_vu)
        except ProcessorException:
            self._anoka_replace_prompt_section(micro_vu)
        return

    def _anoka_replace_prompt_section(self, micro_vu: MicroVuProgram) -> None:
        pass
        # insert_idx: int = self._get_index_containing_text("(Name \"START")
        # if insert_idx == 0:
        #     raise ProcessorException(f"Can't determine where to put the prompts. Cannot process file {Path(self.input_filepath).name}.")
        #
        # start_idx: int = self._get_index_containing_text("AutoExpFile")
        # for idx in range(insert_idx, start_idx, -1):
        #     if self.file_lines[idx].startswith("Prmt"):
        #         del self.file_lines[idx]
        # insert_index: int = self._get_index_containing_text("(Name \"START")
        # pattern = 'sp_prompt_text.txt' if self.is_profile else 'prompt_text.txt'
        #
        # prompt_file = _get_filepath_by_name(pattern)
        # if not prompt_file:
        #     raise ProcessorException("Can't find 'prompt_text' file.")
        #
        # prompt_lines = _get_utf_encoded_file_lines(prompt_file)
        # if not prompt_lines:
        #     raise ProcessorException("Can't find 'prompt_text' file.")
        #
        # for line in prompt_lines:
        #     if line.find("(Name \"IN PROCESS\")") > 0:
        #         self.file_lines.insert(insert_index, line)
        #         continue
        #     if line.find("(Name \"MACHINE\")") > 0:
        #         self.file_lines.insert(insert_index, line)
        #         continue
        #     if line.find("(Name \"JOB\")") > 0:
        #         self.file_lines.insert(insert_index, line)
        #         continue
        #     if line.find("(Name \"EMPLOYEE\")") > 0:
        #         self.file_lines.insert(insert_index, line)
        #         continue
        #     if line.find("(Name \"OPERATION\")") > 0:
        #         line = line.replace("<O>", str(self.op_number))
        #         self.file_lines.insert(insert_index, line)
        #         continue
        #     if line.find("(Name \"REV LETTER\")") > 0:
        #         line = line.replace("<R>", str(self.rev_number))
        #         self.file_lines.insert(insert_index, line)
        #         continue
        #     if line.find("(Name \"PT\")") > 0:
        #         line = line.replace("<P>", str(self.part_number))
        #         self.file_lines.insert(insert_index, line)
        #         continue
        #     if line.find("(Name \"SEQUENCE\")") > 0:
        #         self.file_lines.insert(insert_index, line)
        #         continue
        #     if line.find("(Name \"SPFILENAME\")") > 0:
        #         line = line.replace("<SPF>", str(self.smartprofile_filepath))
        #         self.file_lines.insert(insert_index, line)
        #         continue
        # return


class ProcessorException(Exception):
    pass
