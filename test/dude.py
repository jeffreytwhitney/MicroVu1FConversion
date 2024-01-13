import os



def _get_filepath_by_name(file_name: str) -> str:
    current_dir = os.path.dirname(__file__)
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file == file_name:
                return str(os.path.join(root, file))
    return ""


class dude():

    def __init__(self):
        self._setup_test_environment()
        super().__init__()

    def _setup_test_environment(self):
        config_filepath = _get_filepath_by_name("TESTSettings.ini")
        os.environ['MICRO_VU_CONVERTER_CONFIG_LOCATION'] = config_filepath


def main():
    tester = dude()


if __name__ == "__main__":
    main()