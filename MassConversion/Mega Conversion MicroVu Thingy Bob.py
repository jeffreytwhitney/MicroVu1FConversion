import os
from pathlib import Path
from typing import List
import logging
from fuzzywuzzy import fuzz
import re
import lib
import lib.Utilities
from lib import MicroVuFileProcessor
from lib.MicroVuFileProcessor import get_processor, ProcessorException
from lib.MicroVuProgram import MicroVuProgram


class MegaConversionThingyBob:

    _sp_lines: List[str] = []
    _op_regex: re
    _rev_regex: re
    _processor: MicroVuFileProcessor

    def __init__(self, smart_profile_filepath: str):
        with open(smart_profile_filepath, "r") as f:
            self._sp_lines = f.readlines()
        self._op_regex = re.compile(r"^(.*)([ _-]OP)( *)(\d+)(.*)(\.IWP)$")
        self._rev_regex = re.compile(r"(REV)( *)(\w+)")
        self._processor = get_processor("JTW")
        logging.basicConfig(filename="C:\\Users\\JTWhitney\\PycharmProjects\\MicroVu1FConversion\\MassConversion\\ErrorLog.txt", filemode='a', format='%(message)s')

    def find_highest_fuzzy_match(self, target_line, lines):
        max_ratio = 0
        best_match = ""

        for line in lines:
            ratio: int = fuzz.ratio(target_line, line)
            if ratio > max_ratio:
                max_ratio = ratio
                best_match = line.rstrip("\n")

        return best_match

    def parse_operation_from_file_name(self, file_name) -> str:
        return f"{match[3]}" if (match := self._op_regex.search(file_name)) else "10"

    def parse_rev_from_file_name(self, directory_name) -> str:
        if match := self._rev_regex.search(directory_name):
            return f"{match[3]}" if match[2] == " " else f"{match[2]}"
        else:
            return "A"

    def parse_part_number(self, file_name) -> str:
        filestem = Path(file_name).stem
        parts = re.split("[ _]", filestem)
        return parts[0]

    def mass_process_microvus(self, input_file_path: str, output_root_path: str) -> None:
        lib.Utilities.StoreIniValue(output_root_path, "Paths", "output_rootpath", "Settings")

        with open(input_file_path, "r") as f:
            filelines = f.readlines()
        for file_path in filelines:
            file_path = file_path.rstrip("\n")
            file_name = os.path.basename(file_path)
            part_number = self.parse_part_number(file_name)
            directory_name = os.path.basename(os.path.dirname(file_path))
            op_number = self.parse_operation_from_file_name(file_name)
            rev_number = self.parse_rev_from_file_name(directory_name)
            micro_vu = MicroVuProgram(file_path, op_number, rev_number, "")
            if micro_vu.is_smartprofile:
                micro_vu.smartprofile_projectname = self.find_highest_fuzzy_match(part_number, self._sp_lines)
            try:
                self._processor.process_file(micro_vu)
            except ProcessorException as e:
                logging.error(f"FilePath:{file_path}: {e.args[0]}", exc_info=False)


sp_filepath = "C:\\Users\\JTWhitney\\PycharmProjects\\MicroVu1FConversion\\MassConversion\\SmartProfiles.txt"
three_elevens = "C:\\Users\\JTWhitney\\PycharmProjects\\MicroVu1FConversion\\MassConversion\\311s.txt"
three_forty_ones = "C:\\Users\\JTWhitney\\PycharmProjects\\MicroVu1FConversion\\MassConversion\\341s.txt"
four_twenties = "C:\\Users\\JTWhitney\\PycharmProjects\\MicroVu1FConversion\\MassConversion\\420s.txt"
three_eleven_output = "V:\\Inspect Programs\\Micro-Vu\\1Factory_Untested\\311"
three_forty_one_output = "V:\\Inspect Programs\\Micro-Vu\\1Factory_Untested\\341"
four_twenty_output = "V:\\Inspect Programs\\Micro-Vu\\1Factory_Untested\\420"

megaConverter = MegaConversionThingyBob(sp_filepath)
megaConverter.mass_process_microvus(three_elevens, three_eleven_output)
megaConverter.mass_process_microvus(three_forty_ones, three_forty_one_output)
megaConverter.mass_process_microvus(four_twenties, four_twenty_output)
