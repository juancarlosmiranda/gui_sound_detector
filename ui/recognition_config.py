import os
import configparser


class RecognitionConfig():
    width = 320
    height = 480
    geometry_about = '300x480'
    geometry_main = '320x480'
    file_extension_to_search = "*.mp4"
    file_name_training = 'TRAINING_MODEL.txt'
    split_at_timestamp = 2  # time used to split files, values in seconds
    file_type = '.wav'
    input_test_folder = ""
    base_folder = os.path.abspath('.')
    input_training_folder = os.path.join(base_folder, "sound_db/training_data/")
    output_split_folder = os.path.join(base_folder, "sound_db/test_data_split/")
    file_browser_input_folder = os.path.join(base_folder, "sound_db/test_data/")
    output_normalized_folder = os.path.join(base_folder, "sound_db/test_data/wav_files/")
    label_to_search = "gemido"

    def __init__(self, file_config_name=None):
        if file_config_name is not None:
            if os.path.isfile(file_config_name):
                self.f_config_name = file_config_name
                self.read_config()

    def read_config(self):
        '''
        Read config from file ui_settings.conf
        :return:
        '''
        f_config = configparser.ConfigParser()
        f_config.read(self.f_config_name)
        self.width = f_config['DEFAULT']['WIDTH']
        self.height = f_config['DEFAULT']['HEIGHT']
        self.geometry_about = f_config['DEFAULT']['geometry_about']
        self.geometry_main = f_config['DEFAULT']['geometry_main']
        self.file_extension_to_search = f_config['DEFAULT']['file_extension_to_search']
        self.file_name_training = f_config['DEFAULT']['file_name_training']
        self.split_at_timestamp = int(f_config['DEFAULT']['split_at_timestamp'])
        self.file_type = f_config['DEFAULT']['file_type']
        self.input_test_folder = f_config['DEFAULT']['input_test_folder']
        self.base_folder = f_config['DEFAULT']['base_folder']
        self.input_training_folder = f_config['DEFAULT']['input_training_folder']
        self.output_split_folder = f_config['DEFAULT']['output_split_folder']
        self.file_browser_input_folder = f_config['DEFAULT']['file_browser_input_folder']
        self.output_normalized_folder = f_config['DEFAULT']['output_normalized_folder']
        self.label_to_search = f_config['DEFAULT']['label_to_search']
