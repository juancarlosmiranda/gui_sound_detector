import os
import subprocess
from scipy.io import wavfile
from helpers.helper_filesystem import remove_files


class ProcessorFrame:
    def split_one_audio_file(self, path_name_audio_to_split, name_audio_to_split, extension_file, split_at_timestamp,
                             output_folder):
        # todo: clean split in folder
        # ---------------------------------------
        remove_files(output_folder, extension_file)
        # ---------------------------------------------------

        # read the file and get the sample rate and data
        rate, data = wavfile.read(path_name_audio_to_split)

        # # get the frame to split at
        split_at_frame = rate * split_at_timestamp
        audio_size = data.size
        total_frames = audio_size / split_at_frame
        frame_counter = 1
        name_string = '_split_'
        # # ---------------------------------------
        while split_at_frame < data.size:
            # split
            left_data, right_data = data[:split_at_frame - 1], data[split_at_frame:]  # split
            frame_str = str(frame_counter)

            if frame_counter < 10:
                frame_str = "0" + str(frame_counter)

            # save in file
            file_name_output_split = name_audio_to_split + name_string + frame_str + extension_file
            path_output_split = output_folder + file_name_output_split
            wavfile.write(path_output_split, rate, left_data)
            frame_counter = frame_counter + 1
            data = right_data

    def split_audio_file(self, audio_folder, name_audio_to_split, extension_file, split_at_timestamp):
        # ---------------------------------------
        # read the file and get the sample rate and data
        rate, data = wavfile.read(audio_folder + '/' + name_audio_to_split)

        # get the frame to split at
        split_at_frame = rate * split_at_timestamp
        audio_size = data.size
        total_frames = audio_size / split_at_frame
        frame_counter = 1
        name_string = '_split_'
        # ---------------------------------------
        print(name_audio_to_split, 'rate ->', rate, 'data.size->', audio_size, 'split_at_timestamp', split_at_timestamp,
              'split_at_frame', split_at_frame)
        # ---------------------------------------
        while split_at_frame < data.size:
            # split
            left_data, right_data = data[:split_at_frame - 1], data[split_at_frame:]  # split
            # save in file
            wavfile.write(audio_folder + '/' + name_audio_to_split + name_string + str(frame_counter) + extension_file,
                          rate, left_data)
            frame_counter = frame_counter + 1
            print(frame_counter)
            data = right_data

    def get_list_to_train(self, input_folder, extension_files, split_at_timestamp):
        """
        From an input folder, this build a list with file names and labels.
        Labels are taken from subfolder name.
        :param input_folder:
        :param extension_files:
        :return: a list with directories
        """
        # ---------------------------------------------------
        label_training_files_list = []
        for a_filename in sorted(os.listdir(input_folder)):
            if a_filename.endswith(extension_files):
                # print(a_filename)
                self.split_audio_file(input_folder, a_filename, extension_files, split_at_timestamp)
                # label_training_files_list.append(('./' + subfolder + '/' + a_filename, a_filename, label))
        # ---------------------------------------------------
        return label_training_files_list

    def normalize_one_audio_file(self, path_name_audio_to_normalize, name_audio_to_normalize, extension_file,
                                 output_normalized_folder):
        # todo: clean split in folder
        # todo: change this method with a ffmpeg library in Python
        # ---------------------------------------
        remove_files(output_normalized_folder, extension_file)
        # ---------------------------------------------------
        print(path_name_audio_to_normalize)
        print(name_audio_to_normalize)
        print(extension_file)
        print(output_normalized_folder)
        cmd_ffmpeg = '/usr/bin/ffmpeg'
        cmd_param = '-y -i'
        middle = '-ar 44100 -b:1 192k'
        final_extension = '.wav'
        CMD_BY_FILE = cmd_ffmpeg + ' ' + cmd_param + ' ' + path_name_audio_to_normalize + ' ' + middle + ' ' + output_normalized_folder + name_audio_to_normalize + final_extension
        process = subprocess.Popen(CMD_BY_FILE.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        return output_normalized_folder + name_audio_to_normalize + final_extension
