from pydub import AudioSegment
import functions
import logging

logging.basicConfig(level=logging.INFO)

file_name = 'test-input.mp3'
input_folder = './testing-src'
output_folder_path = './testing-src/output'
input_file_path = f'{input_folder}/{file_name}'

functions.download_model()
path_out_vocal, path_out_instru = functions.separate_mp3_tracks(
    input_file_path,
    output_folder_path
)


def are_mp3_files_same(path_1, path_2):
    audio1 = AudioSegment.from_mp3(path_1)
    audio2 = AudioSegment.from_mp3(path_2)
    result = audio1.raw_data == audio2.raw_data
    print(f'{result}: comparing', path_1, path_2)
    return result


path_expected_vocal = f'{input_folder}/expected-out-vocals.mp3'
path_expected_instru = f'{input_folder}/expected-out-instru.mp3'

assert are_mp3_files_same(path_expected_vocal, path_out_vocal)
assert are_mp3_files_same(path_expected_instru, path_out_instru)

print('this works great!!')

exit(0)