from abc import ABCMeta, abstractmethod
import re
from typing import List


class DimensionParser(metaclass=ABCMeta):
    _regex: re

    def does_pattern_match(self, search_string: str) -> bool:
        return bool(_ := self._regex.fullmatch(search_string))

    @abstractmethod
    def get_dimension_name(self, search_string: str) -> str:
        return ""


class Parser1(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(?:ITEM|INSP)([ _-])(\\d+)\\.(\\d+)([A-Za-z])([ _-])\\d+X$")

    def get_dimension_name(self, search_string: str) -> str:

        if match := self._regex.search(search_string):
            return f"INSP_{match[2]}.{match[3]}{match[4]}"
        else:
            return search_string


class Parser2(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(ITEM|INSP)([ _-])(\\d+)\\.(\\d+)([ _-])\\d+X$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):
            return f"INSP_{match[3]}.{match[4]}"
        else:
            return search_string


class Parser3(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(ITEM|INSP)([ _-])(\\d+)([A-Za-z])([ _-])\\d+X$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):
            return f"INSP_{match[3]}{match[4]}"
        else:
            return search_string


class Parser4(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(ITEM|INSP)([ _-])(\\d+)([ _-])(\\d+)X$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):
            letter = chr(ord('@') + int(match[5]))
            return f"INSP_{match[3]}{letter}"
        else:
            return search_string


class Parser5(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(ITEM|INSP)([ _-])(\\d+)\.(\\d+)$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):

            return f"INSP_{match[3]}.{match[4]}"
        else:
            return search_string


class Parser6(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)\\.(\\d+)([A-Za-z])([ _-])(\d+)X$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):
            letter = chr(ord('@') + int(match[5]))
            return f"INSP_{match[1]}.{match[2]}{letter}"
        else:
            return search_string


class Parser7(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)\\.(\\d+)([ _-])(\\d+)X$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):
            letter = chr(ord('@') + int(match[4]))
            return f"INSP_{match[1]}.{match[2]}{letter}"
        else:
            return search_string


class Parser8(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)\\.(\\d+)([ _-])(\\d+)$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):
            letter = chr(ord('@') + int(match[4]))
            return f"INSP_{match[1]}.{match[2]}{letter}"
        else:
            return search_string


class Parser9(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)\\.(\\d+)([ _-])([A-Za-z])$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):

            return f"INSP_{match[1]}.{match[2]}{match[4]}"
        else:
            return search_string


class Parser10(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)\\.(\\d+)([A-Za-z])$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):

            return f"INSP_{match[1]}.{match[2]}{match[3]}"
        else:
            return search_string


class Parser11(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)[ _-](\\d+)X+$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):
            letter = chr(ord('@') + int(match[2]))
            return f"INSP_{match[1]}{letter}"
        else:
            return search_string


class Parser12(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(?:ITEM|INSP)([ _-])(\\d+)$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):

            return f"INSP_{match[2]}"
        else:
            return search_string


class Parser13(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)([ _-])(\\d+)$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):
            letter = chr(ord('@') + int(match[3]))
            return f"INSP_{match[1]}{letter}"
        else:
            return search_string


class Parser14(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)([ _-])([A-Za-z])$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):

            return f"INSP_{match[1]}{match[3]}"
        else:
            return search_string


class Parser15(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)\\.(\\d+)$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):

            return f"INSP_{match[1]}.{match[2]}"
        else:
            return search_string


class Parser16(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\d+)([A-Za-z])$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):

            return f"INSP_{match[1]}{match[2]}"
        else:
            return search_string


class Parser17(DimensionParser):
    def __init__(self):
        self._regex = re.compile("^(\\d+)$")

    def get_dimension_name(self, search_string: str) -> str:
        if match := self._regex.search(search_string):

            return f"INSP_{match[1]}"
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
        self._dimension_parsers.append(Parser17())

    def get_dimension_name(self, search_string: str) -> str:
        for p in self._dimension_parsers:
            if p.does_pattern_match(search_string):
                return p.get_dimension_name(search_string)

        return search_string


# sorter = DimensionNameSorter()
# print(sorter.get_dimension_name("ITEM 12.1A 1X"))
# print(sorter.get_dimension_name("ITEM_11.1A 1X"))
# print(sorter.get_dimension_name("ITEM_10.1A 1X"))
# print(sorter.get_dimension_name("ITEM_9.1A 1X"))
# print(sorter.get_dimension_name("INSP-12.1_1X"))
# print(sorter.get_dimension_name("INSP_12.1-1X"))
# print(sorter.get_dimension_name("INSP-12.1-1X"))
# print(sorter.get_dimension_name("ITEM-12.1_1X"))
# print(sorter.get_dimension_name("ITEM_12.1-1X"))
# print(sorter.get_dimension_name("ITEM-12.1-1X"))
# print(sorter.get_dimension_name("ITEM 12.1 1X"))
# print(sorter.get_dimension_name("ITEM_12.1 1X"))
# print(sorter.get_dimension_name("ITEM_12.1_1X"))
# print(sorter.get_dimension_name("ITEM 12.1_1X"))
# print(sorter.get_dimension_name("INSP 12.1 1X"))
# print(sorter.get_dimension_name("INSP_12.1 1X"))
# print(sorter.get_dimension_name("INSP_12.1_1X"))
# print(sorter.get_dimension_name("INSP 12.1_1X"))
# print(sorter.get_dimension_name("ITEM 12A 1X"))
# print(sorter.get_dimension_name("ITEM_12A 1X"))
# print(sorter.get_dimension_name("ITEM_12A_1X"))
# print(sorter.get_dimension_name("ITEM 12A_1X"))
# print(sorter.get_dimension_name("ITEM 12 1X"))
# print(sorter.get_dimension_name("ITEM_12 1X"))
# print(sorter.get_dimension_name("ITEM_12_1X"))
# print(sorter.get_dimension_name("ITEM 12_12X"))
# print(sorter.get_dimension_name("INSP 12 1X"))
# print(sorter.get_dimension_name("INSP_12 1X"))
# print(sorter.get_dimension_name("INSP_12_1X"))
# print(sorter.get_dimension_name("INSP 12_1X"))
# print(sorter.get_dimension_name("INSP-12_1X"))
# print(sorter.get_dimension_name("INSP_12-1X"))
# print(sorter.get_dimension_name("INSP-12-1X"))
# print(sorter.get_dimension_name("ITEM-12_1X"))
# print(sorter.get_dimension_name("ITEM_12-1X"))
# print(sorter.get_dimension_name("ITEM-12-1X"))
# print(sorter.get_dimension_name("ITEM 12.16"))
# print(sorter.get_dimension_name("ITEM_12.16"))
# print(sorter.get_dimension_name("INSP 12.16"))
# print(sorter.get_dimension_name("INSP_12.16"))
# print(sorter.get_dimension_name("ITEM-12.1"))
# print(sorter.get_dimension_name("INSP-12.1"))
# print(sorter.get_dimension_name("ITEM 12.1"))
# print(sorter.get_dimension_name("ITEM_12.1"))
# print(sorter.get_dimension_name("INSP 12.1"))
# print(sorter.get_dimension_name("INSP_12.1"))
# print(sorter.get_dimension_name("12.1A_1X"))
# print(sorter.get_dimension_name("12.16C_9X"))
# print(sorter.get_dimension_name("12.1 1X"))
# print(sorter.get_dimension_name("12.14_5X"))
# print(sorter.get_dimension_name("12.1-1X"))
# print(sorter.get_dimension_name("12.1-1"))
# print(sorter.get_dimension_name("12.1_1"))
# print(sorter.get_dimension_name("12.1 A"))
# print(sorter.get_dimension_name("12.1_A"))
# print(sorter.get_dimension_name("12.1A"))
# print(sorter.get_dimension_name("12.16A"))
# print(sorter.get_dimension_name("12_1X"))
# print(sorter.get_dimension_name("12 4X"))
# print(sorter.get_dimension_name("12-8X"))
# print(sorter.get_dimension_name("ITEM 12"))
# print(sorter.get_dimension_name("ITEM_12"))
# print(sorter.get_dimension_name("INSP 12"))
# print(sorter.get_dimension_name("INSP_12"))
# print(sorter.get_dimension_name("ITEM-12"))
# print(sorter.get_dimension_name("INSP-12"))
# print(sorter.get_dimension_name("12-1"))
# print(sorter.get_dimension_name("12_6"))
# print(sorter.get_dimension_name("12 1"))
# print(sorter.get_dimension_name("12 A"))
# print(sorter.get_dimension_name("12_B"))
# print(sorter.get_dimension_name("12.1"))
# print(sorter.get_dimension_name("12.16"))
# print(sorter.get_dimension_name("12A"))
# print(sorter.get_dimension_name("16B"))
# print(sorter.get_dimension_name("12"))