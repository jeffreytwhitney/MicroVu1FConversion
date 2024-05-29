import re
from abc import ABCMeta, abstractmethod
from typing import List


class DimensionParser(metaclass=ABCMeta):
    _regex: re

    def does_pattern_match(self, search_string: str) -> bool:
        return bool(_ := self._regex.fullmatch(search_string))

    @abstractmethod
    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        return ""


class Parser1(DimensionParser):
    def __init__(self):
        # Matches "ITEM_12.1A 1X"
        self._regex = re.compile(r"^(?:#*)(?:ITEM|INSP)([ _-])(\d+)\.(\d+)([A-Za-z])([ _-])\d+(?:X*)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[2]}.{match[3]}{match[4]}"
        else:
            return search_string


class Parser2(DimensionParser):
    def __init__(self):
        # Matches "INSP-12.1_1X"
        self._regex = re.compile(r"^(?:#*)(ITEM|INSP)([ _-])(\d+)\.(\d+)([ _-])(\d+)X$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if not (match := self._regex.search(search_string)):
            return search_string
        letter = chr(ord('@') + int(match[6]))
        return f"{prefix}{match[3]}.{match[4]}{letter}"


class Parser3(DimensionParser):
    def __init__(self):
        # Matches "ITEM_12A_1X"
        self._regex = re.compile(r"^(?:#*)(ITEM|INSP)([ _-])(\d+)([A-Za-z])([ _-])\d+(?:X*)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[3]}{match[4]}"
        else:
            return search_string


class Parser4(DimensionParser):
    def __init__(self):
        # Matches "INSP_12 1X"
        self._regex = re.compile(r"^(?:#*)(ITEM|INSP)([ _-])(\d+)([ _-])(\d+)(?:X*)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if not (match := self._regex.search(search_string)):
            return search_string
        letter = chr(ord('@') + int(match[5]))
        return f"{prefix}{match[3]}{letter}"


class Parser5(DimensionParser):
    def __init__(self):
        # Matches "INSP 12.1"
        self._regex = re.compile(r"^(?:#*)(ITEM|INSP)([ _-])(\d+)\.(\d+)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[3]}.{match[4]}"
        else:
            return search_string


class Parser6(DimensionParser):
    def __init__(self):
        # Matches "12.1A_1X"
        self._regex = re.compile(r"^(?:#*)(\d+)\.(\d+)([A-Za-z])([ _-])(\d+)(?:X*)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if not (match := self._regex.search(search_string)):
            return search_string
        letter = chr(ord('@') + int(match[5]))
        return f"{prefix}{match[1]}.{match[2]}{letter}"


class Parser7(DimensionParser):
    def __init__(self):
        # Matches "12.1_1"
        self._regex = re.compile(r"^(?:#*)(\d+)\.(\d+)([ _-])(\d+)(?:X*)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if not (match := self._regex.search(search_string)):
            return search_string
        letter = chr(ord('@') + int(match[4]))
        return f"{prefix}{match[1]}.{match[2]}{letter}"


class Parser8(DimensionParser):
    def __init__(self):
        # Matches "#12.1_A"
        self._regex = re.compile(r"^(?:#*)(\d+)\.(\d+)([ _-])([A-Za-z])$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[1]}.{match[2]}{match[4]}"
        else:
            return search_string


class Parser9(DimensionParser):
    def __init__(self):
        # Matches "#12.16A"
        self._regex = re.compile(r"^(?:#*)(\d+)\.(\d+)([A-Za-z])$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[1]}.{match[2]}{match[3]}"
        else:
            return search_string


class Parser10(DimensionParser):
    def __init__(self):
        # Matches "#12_1"
        self._regex = re.compile(r"^(?:#*)(\d+)[ _-](\d+)(?:X*)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if not (match := self._regex.search(search_string)):
            return search_string
        letter = chr(ord('@') + int(match[2]))
        return f"{prefix}{match[1]}{letter}"


class Parser11(DimensionParser):
    def __init__(self):
        # Matches "#ITEM-12"
        self._regex = re.compile(r"^(?:#*)(?:ITEM|INSP)([ _-])(\d+)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[2]}"
        else:
            return search_string


class Parser12(DimensionParser):
    def __init__(self):
        # Matches "12 1"
        self._regex = re.compile(r"^(?:#*)(\d+)([ _-])(\d+)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if not (match := self._regex.search(search_string)):
            return search_string
        letter = chr(ord('@') + int(match[3]))
        return f"{prefix}{match[1]}{letter}"


class Parser13(DimensionParser):
    def __init__(self):
        # Matches "12_B"
        self._regex = re.compile(r"^(?:#*)(\d+)([ _-])([A-Za-z])$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[1]}{match[3]}"
        else:
            return search_string


class Parser14(DimensionParser):
    def __init__(self):
        # Matches "12.16"
        self._regex = re.compile(r"^(?:#*)(\d+)\.(\d+)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[1]}.{match[2]}"
        else:
            return search_string


class Parser15(DimensionParser):
    def __init__(self):
        # Matches "12A"
        self._regex = re.compile(r"^(?:#*)(\d+)([A-Za-z])$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[1]}{match[2]}"
        else:
            return search_string


class Parser16(DimensionParser):
    def __init__(self):
        # Matches "#12"
        self._regex = re.compile(r"^(?:#*)(\d+)$")

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        if match := self._regex.search(search_string):
            return f"{prefix}{match[1]}"
        else:
            return search_string


class DimensionNameSorter:
    _dimension_parsers: List[DimensionParser] = []

    def __init__(self):
        self._dimension_parsers.append(Parser1())
        self._dimension_parsers.append(Parser2())
        self._dimension_parsers.append(Parser3())
        self._dimension_parsers.append(Parser4())
        self._dimension_parsers.append(Parser5())
        self._dimension_parsers.append(Parser6())
        self._dimension_parsers.append(Parser7())
        self._dimension_parsers.append(Parser8())
        self._dimension_parsers.append(Parser9())
        self._dimension_parsers.append(Parser10())
        self._dimension_parsers.append(Parser11())
        self._dimension_parsers.append(Parser12())
        self._dimension_parsers.append(Parser13())
        self._dimension_parsers.append(Parser14())
        self._dimension_parsers.append(Parser15())
        self._dimension_parsers.append(Parser16())

    def get_dimension_name(self, search_string: str, prefix: str) -> str:
        for p in self._dimension_parsers:
            if p.does_pattern_match(search_string):
                return p.get_dimension_name(search_string, prefix)

        return search_string
