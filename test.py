import os
import MicroVuProcessor

input_filepath = os.getcwd() + os.sep + "2923-C001-001 BOTTOM VIEW.iwp"
output_filepath = os.getcwd() + os.sep + "text.iwp"
bob = MicroVuProcessor.MicroVuProcessor(input_filepath, "10", "JTW", output_filepath, False)
bob.process_file()
