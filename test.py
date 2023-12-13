import os
import re


def get_index_containing_text(text_to_find):
    for i, l in enumerate(file_lines):
        if l.find(text_to_find) > 1:
            return i


def get_mv_filename():
    part_number_line = file_lines[get_index_containing_text("AutoRptFileName")]
    title_index = part_number_line.find("AutoRptFileName")
    begin_quote_index = part_number_line.find("\"", title_index)
    end_quote_index = part_number_line.find("\"", begin_quote_index + 1)
    filepath_text = part_number_line[begin_quote_index + 1:end_quote_index]
    file_parts = filepath_text.split("\\")
    mv_filename = file_parts[2]
    return mv_filename[:-5]


def get_part_number():
    part_name = re.split(" |_", get_mv_filename())
    return part_name[0].upper()


def get_rev_number():
    filename_parts = re.split(" |_", get_mv_filename())
    for i, p in enumerate(filename_parts):
        if p.find("REV") > -1:
            if p == "REV":
                return filename_parts[i + 1]
            else:
                return p[3:]


def get_view_name():
    filename_parts = re.split(' |_', get_mv_filename())
    count_of_parts = filename_parts.count

    for i, p in enumerate(filename_parts):
        if p.find("REV") > -1:
            if p == "REV" and i == count_of_parts:
                return ""
            elif i + 1 == count_of_parts:
                return ""



filepath = os.getcwd() + os.sep + "2923-C001-001 BOTTOM VIEW.iwp"

with open(filepath, "r", encoding='utf-16-le') as f:
    file_lines = f.readlines()

print(get_mv_filename())

# print(get_index_containing_text("AutoRptFileName", file_lines))
# print(get_index_containing_text("Name \"PT #\"", file_lines))
# print(get_index_containing_text("Name \"Employee #\"", file_lines))
# print(get_index_containing_text("Name \"Machine #\"", file_lines))
# print(get_index_containing_text("Name \"Run-Setup\"", file_lines))
