"""
Project:
Author:
Date:
Description:
...

Use:
"""
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog

from classifier.classifier_frame import ClassifierFrame
from classifier.split_files_main import ProcessorFrame
from ui.recognition_config import RecognitionConfig
from helpers.helper_filesystem import remove_files


class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry(RecognitionConfig.geometry_about)
        self.title('About...')
        self.resizable(width=False, height=False)  # do not change the size
        self.attributes('-topmost', True)

        aboutLabel = tk.Label(self, text='About')
        aboutLabel.config(bg="#00ffff", font=("Verdana", 12))
        aboutLabel.pack(anchor=tk.CENTER)
        tinfo = tk.Text(self, width=40, height=5)

        about_text_info = "I made this software to detect jokes sent by friends in WhatsApp groups." + "\n"
        about_text_info += "https://github.com/juancarlosmiranda" + "\n"
        about_text_info += "Juan Carlos Miranda\n August 2021 " + "\n"

        tinfo.insert("1.0", about_text_info)
        tinfo.pack(anchor=tk.CENTER)
        buttonClose = tk.Button(self, text='Close', command=self.destroy)
        buttonClose.pack(expand=True)


class UIRecognitionManagerConsole(tk.Tk):
    r_config = None

    def __init__(self, r_config, master=None):
        super().__init__(master)
        self.r_config = r_config  # assign config
        self.geometry(self.r_config.geometry_main)
        self.title("MOAN detector")
        self.resizable(width=False, height=False)  # do not change the size
        self.attributes('-topmost', True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.createWidgets()
        self.createMenuBars()

    def createWidgets(self):
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(column=0, row=0)
        # ---------------
        self.analyze_file_button = tk.Button(self.left_frame, text='Analyze a file', command=self.analyze_data)
        self.analyze_file_button.grid(row=1, column=0, sticky=tk.EW)
        self.training_button = tk.Button(self.left_frame, text='Train', command=self.folder_to_training)
        self.training_button.grid(row=2, column=0, sticky=tk.EW)
        # ---------------
        self.training_button = tk.Button(self.left_frame, text='Clean temporal files',
                                         command=self.clean_temporal_files)
        self.training_button.grid(row=3, column=0, sticky=tk.EW)

        self.quitButton = tk.Button(self.left_frame, text='Quit', command=self.quit_app)
        self.quitButton.grid(row=4, column=0, sticky=tk.EW)

        self.messages_info = tk.Text(self.left_frame, width=40, height=5)
        self.messages_info.grid(row=5, column=0, sticky=tk.EW)

        self.file_to_test_label = tk.Label(self.left_frame, text='Results:')
        self.file_to_test_label.grid(row=6, column=0, sticky=tk.EW)

        self.results_info = tk.Text(self.left_frame, width=40, height=20)
        self.results_info.grid(row=7, column=0, sticky=tk.EW)

    def createMenuBars(self):
        self.menubar = tk.Menu(self)
        self.menu_help = tk.Menu(self.menubar, tearoff=False)  # delete dash lines
        self.menu_help.add_command(label="About...", command=self.not_implemented_yet)
        self.menubar.add_cascade(menu=self.menu_help, label='About', underline=0)
        self.config(menu=self.menubar)  # add menu to window

    def not_implemented_yet(self):
        print("Not implemented yet!!!")
        about_windows = AboutWindow(self)
        about_windows.grab_set()

    def clean_temporal_files(self):
        self.messages_info.delete("1.0", "end")
        self.results_info.delete("1.0", "end")
        remove_files(self.r_config.output_split_folder, self.r_config.file_type)
        remove_files(self.r_config.output_normalized_folder, self.r_config.file_type)

    def clean_text_widgets(self):
        self.messages_info.delete("1.0", "end")
        self.results_info.delete("1.0", "end")

    def folder_to_training(self):
        self.clean_text_widgets

        directory_selected = filedialog.askdirectory(initialdir=self.r_config.input_training_folder)

        if directory_selected == ():
            analyze_status_str = "A directory has not been selected " + "\n"
        else:
            speaker_recognizer = ClassifierFrame(self.r_config.file_name_training, self.r_config.file_type,
                                                 self.r_config.split_at_timestamp)
            speaker_recognizer.build_audio_models(self.r_config.input_training_folder, self.r_config.file_type,
                                                  self.r_config.split_at_timestamp)
            speaker_recognizer.save_audio_models(self.r_config.file_name_training)
        analyze_status_str = f"Trained model saved at {self.r_config.file_name_training}" + "\n"
        results_info_str = "Click the \"Analize a file\" button to detect sounds " + "\n"
        self.messages_info.insert("1.0", analyze_status_str)
        self.results_info.insert("1.0", results_info_str)

    def analyze_data(self):
        self.clean_text_widgets
        analyze_status_str = ""
        results_info_str = ""
        if os.path.isfile(self.r_config.file_name_training):
            # ---------------------------------------------
            path_filename_selected = filedialog.askopenfilename(initialdir=self.r_config.file_browser_input_folder,
                                                                title="Select a File", filetypes=(
                    ("Text files", self.r_config.file_extension_to_search), ("all files", "*.*")))

            if path_filename_selected == ():
                analyze_status_str = "A file has not been selected " + "\n"
            else:
                analyze_status_str = path_filename_selected
                file_name_selected = os.path.basename(path_filename_selected)
                pro_audio = ProcessorFrame()
                path_filename_wav_selected = pro_audio.normalize_one_audio_file(path_filename_selected,
                                                                                file_name_selected,
                                                                                self.r_config.file_type,
                                                                                self.r_config.output_normalized_folder)
                file_name_wav_selected = os.path.basename(path_filename_wav_selected)
                pro_audio.split_one_audio_file(path_filename_wav_selected, file_name_wav_selected,
                                               self.r_config.file_type, self.r_config.split_at_timestamp,
                                               self.r_config.output_split_folder)
                speaker_recognizer = ClassifierFrame(self.r_config.file_name_training, self.r_config.file_type,
                                                     self.r_config.split_at_timestamp)  # declare wrapper for speech recognition
                speaker_recognizer.load_audio_models(self.r_config.file_name_training)
                speaker_recognizer.run_audio_tests(self.r_config.output_split_folder)
                results_info_str = speaker_recognizer.search_label_tests(self.r_config.label_to_search)
            # ----------------------------------------
        else:
            analyze_status_str = "There is no trained model, you must first train one to classify the sounds." + "\n"

        self.messages_info.insert("1.0", analyze_status_str)
        self.results_info.insert("1.0", results_info_str)

    def quit_app(self):
        # ---------------------------------------------
        self.quit
        self.destroy()
