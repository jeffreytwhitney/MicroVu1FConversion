import os

from lib.MicroVuProgram import MicroVuProgram


def _write_file_to_harddrive(micro_vu: MicroVuProgram) -> None:
    try:
        with open(micro_vu.filepath, "w", encoding="utf-16-le", newline="\r\n") as f:
            for line in micro_vu.file_lines:
                f.write(f"{line}")
    except:
        pass



for file in os.listdir("C:\\TEST\\MassUpdateAnokaMV\\"):
    new_file = str(os.path.join("C:\\TEST\\MassUpdateAnokaMV\\", file))
    microvu = MicroVuProgram()