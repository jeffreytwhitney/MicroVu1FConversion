import os
import re
from datetime import datetime


class Processor:

    def __init__(self, mv_input_filepath, op_num, user_initials, mv_output_filepath, is_profile):
        self.user_initials = user_initials
        self.input_filepath = mv_input_filepath
        self.output_filepath = mv_output_filepath
        self.op_number = op_num
        with open(mv_input_filepath, "r", encoding='utf-16-le') as f:
            self.file_lines = f.readlines()
        self.rev_number = self._get_rev_number()
        self.part_number = self._get_part_number()
        self.view_name = self._get_view_name()
        self.is_profile = is_profile

    def _parse_dimension_name(self, dimension_name):
        charstr = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        chars = list(charstr)
        dim_parts = re.split("[ _X.-]", dimension_name)
        while "" in dim_parts:
            dim_parts.remove("")
        if len(dim_parts) == 1:
            dim_part = dim_parts[0]
            dim_part = dim_part.upper().replace("INSP", "").replace("ITEM", "")
            if dim_part.isnumeric():
                return dim_part
            elif dim_part[0:-1].isnumeric():
                return dim_part
        if len(dim_parts) == 2 and dim_parts[1].isnumeric():
            return "#" + dim_parts[1]
        if len(dim_parts) == 2:
            last_part = dim_parts[1][:-1]
            if last_part.isnumeric():
                return "#" + dim_parts[1]
        if dim_parts[1].isnumeric() and dim_parts[2].isnumeric():
            return "#" + dim_parts[1] + chars[int(dim_parts[2])]
        if dim_parts[1].isnumeric() and dim_parts[2].isalpha() and len(dim_parts[2]) == 1:
            return "#" + dim_parts[1] + dim_parts[2]

    def _global_replace(self, old_value, new_value):
        quoted_old_value = "\"" + old_value + "\""
        quoted_new_value = "\"" + new_value + "\""
        for i, l in enumerate(self.file_lines):
            if l.find(quoted_old_value) > 0:
                new_line = l.replace(quoted_old_value, quoted_new_value)
                self.file_lines[i] = new_line

    def _get_node_text(self, line_text, search_value):
        node_search_text = f"({search_value} "
        title_index = line_text.find(node_search_text)
        begin_quote_index = line_text.find("\"", title_index)
        end_quote_index = line_text.find("\"", begin_quote_index + 1)
        return line_text[begin_quote_index + 1:end_quote_index]

    def _set_node_text(self, line_text, search_value, set_value):
        current_value = self._get_node_text(line_text, search_value)
        return line_text.replace(current_value, set_value)

    def _get_index_containing_text(self, text_to_find):
        for i, l in enumerate(self.file_lines):
            if l.find(text_to_find) > 1:
                return i

    def _does_name_already_exist(self, name_to_find):
        search_text = "(Name \"" + name_to_find + "\")"
        return any(l.find(search_text) > 1 for l in self.file_lines)

    def _get_mv_filename(self):
        part_number_line = self.file_lines[self._get_index_containing_text("AutoRptFileName")]
        filepath_text = self._get_node_text(part_number_line, "AutoRptFileName")
        file_parts = filepath_text.split("\\")
        mv_filename = file_parts[2]
        return mv_filename[:-5]

    def _get_part_number(self):
        part_name = re.split("[ _]", self._get_mv_filename())
        return part_name[0].upper()

    def _get_rev_number(self):
        filename_parts = re.split("[ _]", self._get_mv_filename())
        for i, p in enumerate(filename_parts):
            if p.find("REV") > -1:
                return filename_parts[i + 1] if p == "REV" else p[3:]

    def _get_view_name(self):
        filename_parts = re.split("[ _]", self._get_mv_filename())
        count_of_parts = len(filename_parts)
        rev_index = 0
        for i, p in enumerate(filename_parts):
            if p.find("REV") > -1:
                if p == "REV" and count_of_parts == 2:
                    return ""
                elif i == count_of_parts == 3:
                    return ""
                else:
                    rev_index = i
        view_name = "".join(f"{line} " for line in filename_parts[1:rev_index])
        return view_name.strip()

    def _get_export_filepath(self):
        if self.is_profile:
            return "C:\\TEXT\\OUTPUT.txt"
        part_rev = f"REV{self.rev_number}"
        curl_filepath = "C:\\Users\\Public\\CURL\\in\\"
        curl_filepath += self.part_number
        curl_filepath += f"_OP{self.op_number}"
        if len(self.view_name) > 0:
            curl_filepath += f"_{self.view_name}"
        curl_filepath += f"_{part_rev}"
        curl_filepath += ".csv"
        return curl_filepath

    def _get_report_filepath(self):
        if self.is_profile:
            return ""
        view_name = self.view_name
        part_rev = f"REV{self.rev_number}"
        report_filepath = "S:\\Micro-Vu\\"
        report_filepath += self.part_number
        report_filepath += f"_OP{self.op_number}"
        if len(view_name) > 0:
            report_filepath += f"_{view_name}"
        report_filepath += f"_{part_rev}_.pdf"
        return report_filepath

    def _replace_export_filepath(self):
        line_idx = self._get_index_containing_text("AutoRptFileName")
        line_text = self.file_lines[line_idx]
        curl_filepath = self._get_export_filepath()
        updated_line_text = self._set_node_text(line_text, "ExpFile", curl_filepath)
        updated_line_text = self._set_node_text(updated_line_text, "AutoExpFile", curl_filepath)
        self.file_lines[line_idx] = updated_line_text

    def _replace_report_filepath(self):
        line_idx = self._get_index_containing_text("AutoRptFileName")
        line_text = self.file_lines[line_idx]
        report_filepath = self._get_report_filepath()
        updated_line_text = self._set_node_text(line_text, "AutoRptFileName", report_filepath)
        self.file_lines[line_idx] = updated_line_text

    def _update_comments(self):
        date_text = datetime.now().strftime("%m/%d/%Y")
        comment_idx = self._get_index_containing_text("(Name \"Edited By and Comments:\")")
        new_comment = "\\r\\nConverted program to work with 1Factory. " + self.user_initials + " " + date_text + "."
        current_comment = self._get_node_text(self.file_lines[comment_idx], "Txt")
        current_comment += new_comment
        updated_comment_line = self._set_node_text(self.file_lines[comment_idx], "Txt", current_comment)
        self.file_lines[comment_idx] = updated_comment_line

    def _replace_prompt_section(self):
        insert_index = self._get_index_containing_text("(Name \"Created By:\")")
        temp_idx = self._get_index_containing_text("(Name \"Edited By and Comments:\")")
        if temp_idx > insert_index:
            insert_index = temp_idx
        del self.file_lines[self._get_index_containing_text("Name \"PT #\"")]
        del self.file_lines[self._get_index_containing_text("Name \"Employee #\"")]
        del self.file_lines[self._get_index_containing_text("Name \"Machine #\"")]
        del self.file_lines[self._get_index_containing_text("Name \"Run-Setup\"")]
        del self.file_lines[self._get_index_containing_text("Name \"Job #\"")]
        insert_index += 1
        prompt_file = os.getcwd() + os.sep + "prompt_text.txt"
        with open(prompt_file, "r", encoding='utf-16-le') as f:
            prompt_lines = f.readlines()
        for line in prompt_lines[::-1]:
            if line.find("(Name \"SEQUENCE\")") > 0:
                self.file_lines.insert(insert_index, line + "\n")
            if line.find("(Name \"IN PROCESS\")") > 0:
                self.file_lines.insert(insert_index, line)
            if line.find("(Name \"MACHINE\")") > 0:
                self.file_lines.insert(insert_index, line)
            if line.find("(Name \"JOB\")") > 0:
                self.file_lines.insert(insert_index, line)
            if line.find("(Name \"EMPLOYEE\")") > 0:
                self.file_lines.insert(insert_index, line)
            if line.find("(Name \"OPERATION\")") > 0:
                line = line.replace("<O>", str(self.op_number))
                self.file_lines.insert(insert_index, line)
            if line.find("(Name \"REV LETTER\")") > 0:
                line = line.replace("<R>", str(self.rev_number))
                self.file_lines.insert(insert_index, line)
            if line.find("(Name \"PT\")") > 0:
                line = line.replace("<P>", str(self.part_number))
                self.file_lines.insert(insert_index, line)

    def _replace_dimension_names(self):
        matches = ["(Name \"ITEM", "(Name \"INSP"]
        for i, line in enumerate(self.file_lines):
            if any(x in line for x in matches):
                if line.startswith("Calc"):
                    continue
                old_dimension_name = self._get_node_text(line, "Name")
                new_dimension_name = self._parse_dimension_name(old_dimension_name)
                if self._does_name_already_exist(new_dimension_name):
                    continue
                self.file_lines[i] = self._set_node_text(line, "Name", new_dimension_name)

    def process_file(self):
        self._replace_export_filepath()
        if not self.is_profile:
            self._replace_report_filepath()
        self._update_comments()
        self._replace_prompt_section()
        if not self.is_profile:
            self._replace_dimension_names()
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)
        file_directory = os.path.dirname(self.output_filepath)
        if not os.path.exists(file_directory):
            os.mkdir(file_directory)
        with open(self.output_filepath, 'w+', encoding='utf-16-le', newline='\r\n') as f:
            for line in self.file_lines:
                f.write(f"{line}")
