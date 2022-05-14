"""
Based in Artificial Intelligence with Python, Chapter 12
Speech Recognition.
Adapted to detect sounds like: graoans and others

python speaker_recognizer_main.py --test-folder test_data/
python speaker_recognizer_main.py --input-folder ./training_data/

"""
import os
import warnings
import pickle
import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
from classifier.ModelHMM import ModelHMM


def features_extraction_from_file(a_filepath, split_at_timestamp):
    """
    Take a file and get featrures, in this case we get MFCC, if ypu have other features
    add here
    https://python-speech-features.readthedocs.io/en/latest/
    :param a_filepath:
    :return:
    """
    sampling_freq, signal = wavfile.read(a_filepath)
    split_at_frame = sampling_freq * split_at_timestamp
    signal = signal[:split_at_frame]
    print('sampling_freq->', sampling_freq, 'split_at_timestamp->', split_at_timestamp, 'split_at_frame->', split_at_frame)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        features_mfcc = mfcc(signal, sampling_freq)

    return features_mfcc



class ClassifierFrame:
    """
    This is a wrapper with methods for load files, save models.
    """

    predicted_list = []

    def __init__(self, file_to_save_trained_model, extension_files, split_at_timestamp):
        """
        Constructor class
        :param file_to_save_trained_model: initialize with a file name 
        :param extension_files: here we initialize extensions files liek: .wav
        """
        print('Constructor -->')
        self.file_to_save_trained_model = file_to_save_trained_model
        self.extension_files = extension_files  # for compatibility
        self.split_at_timestamp = split_at_timestamp
        self.speech_models_list = []  # we save trained models after train process
        self.predicted_list = []
        # type of features extraction

    # -----------------------------------------------
    def get_list_to_train(self, input_folder, extension_files):
        """
        From an input folder, this build a list with file names and labels.
        Labels are taken from subfolder name.
        :param input_folder:
        :param extension_files:
        :return: a list with directories
        """
        # ---------------------------------------------------
        # Initialize the variable to store all the models
        label_training_files_list = []
        # Parse the input directory
        for dirname in os.listdir(input_folder):
            # Get the name of the subfolder
            subfolder = os.path.join(input_folder, dirname)
            if not os.path.isdir(subfolder):
                continue
            # Extract the label for file
            label = subfolder[subfolder.rfind('/') + 1:]
            # Create a list of files to be used for training
            # We will leave one file per folder for testing
            for a_filename in os.listdir(subfolder):
                if a_filename.endswith(extension_files):
                    print(a_filename)
                    label_training_files_list.append(('./' + subfolder + '/' + a_filename, a_filename, label))
        # ---------------------------------------------------
        return label_training_files_list

    def save_models(self):
        """
        Save a trained classifier object
        :return:
        """
        # ---------------------------------------
        # Save the model
        with open(self.file_to_save_trained_model, 'wb') as f:
            pickle.dump(self.classifier_trained, f)
        # ---------------------------------------


    def get_list_to_test(self, input_test_folder, extension_files):
        """
        From an input test folder, this build a list with file names, it is used to test
        :param input_test_folder:
        :param extension_files:
        :return: a list with directories
        """
        # Initialize the variable to store all the models
        label_test_files_list = []
        # Parse the input directory
        for a_filename in os.listdir(input_test_folder):
            # Get the name of the subfolder
            if a_filename.endswith(extension_files):
                print(a_filename)
                file_name = os.path.join(input_test_folder, a_filename)
                if os.path.isdir(file_name):
                    continue
                    # Extract the label for file
                label_test_files_list.append(('./' + file_name))
        return label_test_files_list

    def get_features_extraction_list(self, a_test_files_list):
        """
        From a list with names, it generates a list with features
        :param a_test_files_list:
        :return: list, with features and files names
        """
        features_list = []
        print('features_extraction_from_list -->')
        # Iterate through the training files and build the models
        for filename in a_test_files_list:
            # Extract the current filepath
            # features extraction from each file
            features_mfcc = features_extraction_from_file(filename)
            # creates here a sample tuple to put in list
            sample_tuple = (filename, features_mfcc)
            features_list.append(sample_tuple)

        return features_list


    def load_audio_models(self, file_name_model):
        # ----------------------------------------
        # Load the model
        with open(file_name_model, 'rb') as f:
            self.speech_models_list = pickle.load(f)
        # ----------------------------------------

    def save_audio_models(self, file_to_save_trained_model):
        """
        Save a trained classifier object
        :param file_name_model:
        :param file_to_save_trained_model:
        :return:
        """
        # Save the model
        with open(file_to_save_trained_model, 'wb') as f:
            pickle.dump(self.speech_models_list, f)

    def build_audio_models(self, input_folder, file_extension, split_at_timestamp):
        """
        Build model from input folder
        :param input_folder:
        :return:
        """
        # Initialize the variable to store all the models
        speech_model_for_label = []

        # Parse the input directory
        for dirname in os.listdir(input_folder):
            # Get the name of the subfolder
            subfolder = os.path.join(input_folder, dirname)

            if not os.path.isdir(subfolder):
                continue
            # Extract the label
            label = subfolder[subfolder.rfind('/') + 1:]

            # Initialize the variables
            audio_data_to_train = np.array([])

            # Create a list of files to be used for training
            # We will leave one file per folder for testing
            training_files = [x for x in os.listdir(subfolder) if x.endswith(file_extension)][:-1]

            # Iterate through the training files and build the models
            for filename in training_files:
                # Extract the current filepath
                filepath = os.path.join(subfolder, filename)
                # Read the audio signal from the input file
                features_mfcc = features_extraction_from_file(filepath, split_at_timestamp)
                # Append to the variable X
                if len(audio_data_to_train) == 0:
                    audio_data_to_train = features_mfcc
                else:
                    audio_data_to_train = np.append(audio_data_to_train, features_mfcc, axis=0)

            # Create the HMM model
            model = ModelHMM()
            # Train the HMM
            model.train(audio_data_to_train)
            # Save the model for the current word
            speech_model_for_label.append((model, label))
            # Reset the variable
            model = None
        # add model trained for an specific label
        self.speech_models_list = speech_model_for_label

    # ------------------------------------------------
    def run_audio_tests(self, audio_test_folder):
        self.predicted_list = []
        for dirname in sorted(os.listdir(audio_test_folder)):
            # Get the name of the subfolder
            test_file = os.path.join(audio_test_folder, dirname)
            if os.path.isdir(test_file):
                continue
            # Extract the label for file
            features_mfcc = features_extraction_from_file(test_file, self.split_at_timestamp)
            # Define variables
            max_score = -float('inf')
            # output_label = None

            # Run the current feature vector through all the HMM
            # models and pick the one with the highest score
            for item in self.speech_models_list:
                model, label = item
                score = model.compute_score(features_mfcc)
                if score > max_score:
                    max_score = score
                    predicted_label = label

            # Print the predicted output
            start_index = test_file.find('/') + 1
            end_index = test_file.rfind('/')
            original_label = test_file[start_index:end_index]

            self.predicted_list.append((test_file,predicted_label)) # used to formt results

            print('Name:', test_file, '| Predicted:', predicted_label)
            print('-------------------------------------------------')

    def search_label_tests(self, label_to_search):
        frame = 1
        results_found_str = ""

        for a_row in self.predicted_list:
            #print(a_row[0], a_row[1])
            if a_row[1].__contains__(label_to_search):
                seconds_find = frame * self.split_at_timestamp
                #print(f"ENCONTRE EN el {frame}, aprox. a los {seconds_find} segundos")
                results_found_str += f"{label_to_search} en frame {frame}, aprox. a los {seconds_find} segundos" + "\n"
            frame = frame + 1
        if results_found_str == []:
            results_found_str += f"Parece que NO hay {label_to_search}" + "\n"

        return results_found_str
