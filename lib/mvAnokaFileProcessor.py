import lib.mvFileProcessor


class Processor(lib.mvFileProcessor.Processor):
    def __init__(self, mv_input_filepath, op_num, user_initials, mv_output_filepath, is_profile):
        super().__init__(mv_input_filepath, op_num, user_initials, mv_output_filepath, is_profile)

    def replace_prompt_section(self):
        super()._replace_prompt_section()
