"""
Project: Sound detector
Author: Juan Carlos Miranda. https://github.com/juancarlosmiranda
Date: August 2021
Description:

This is an application to detect jokes in .mp4 files received from WhatsApp groups.
It analyzes the files and issues a result indicating what was detected.

Use:
 python UI_main_recognition.py
"""

import logging
import os
from ui.gui_recognition_classes import UIRecognitionManagerConsole
from ui.recognition_config import RecognitionConfig

if __name__ == '__main__':
    BASE_DIR = os.path.abspath('.')
    path_config_file = os.path.join(BASE_DIR, 'conf','ui_recognition_settings.conf')
    recognition_config_obj = RecognitionConfig(path_config_file)
    app = UIRecognitionManagerConsole(recognition_config_obj)
    app.mainloop()
    # todo:config files
    # todo:log files
    # todo:save config form
