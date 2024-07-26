import platform
from time import time

from pydub import AudioSegment

from gui_data.constants import VR_ARCH_TYPE, MDX_ARCH_TYPE, DEMUCS_ARCH_TYPE, BG_COLOR
from separate import SeperateDemucs, SeperateMDX, SeperateMDXC, SeperateVR
from UVR import ModelData, MainWindow, is_windows, init_root

file_name = 'test-input.mp3'
input_folder = './testing-src'
export_path = './testing-src/output'
input_path = f'{input_folder}/{file_name}'

arch_type = 'MDX-Net'
model_name = 'MDX23C-InstVoc HQ'

# main of UVR.py
if not is_windows:
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
else:
    from ctypes import windll, wintypes
try:
    windll.user32.SetThreadDpiAwarenessContext(wintypes.HANDLE(-1))
except Exception as e:
    if platform.system() == 'Windows':
        print(e)

root = MainWindow()
init_root(root)
# root.update_checkbox_text()
root.is_root_defined_var.set(True)
root.is_check_splash = True

# root.update() if is_windows else root.update_idletasks()
# root.deiconify()
# root.configure(bg=BG_COLOR)
# root.mainloop()

current_model = ModelData(root, model_name, arch_type)
current_model.mdxnet_stem_select = 'Vocals'
audio_file_base = input_path.split('/')[-1].split('.')[0]
def do_nothing(*args, **kwargs): pass
def return_none(*args, **kwargs): return None, None
all_models = [model_name]

process_data = {
'model_data': current_model,
'export_path': export_path,
'audio_file_base': audio_file_base,
'audio_file': input_path,
'set_progress_bar': do_nothing,
'write_to_console': do_nothing,
'process_iteration': do_nothing,
'cached_source_callback': return_none,
'cached_model_source_holder': do_nothing,
'list_all_models': all_models,
'is_ensemble_master': False,
'is_4_stem_ensemble': False
}

print('current_model.process_method', current_model.process_method)
print('current_model.is_mdx_c', current_model.is_mdx_c)

if current_model.process_method == VR_ARCH_TYPE:
    seperator = SeperateVR(current_model, process_data)
if current_model.process_method == MDX_ARCH_TYPE:
    seperator = SeperateMDXC(current_model, process_data) if current_model.is_mdx_c else SeperateMDX(current_model, process_data)
if current_model.process_method == DEMUCS_ARCH_TYPE:
    seperator = SeperateDemucs(current_model, process_data)

# Separate
start_time = time()
print('seperating')
seperator.seperate()
end_time = time()
print('elapsed', f'{end_time - start_time}')
path_out_vocal_wav = f"{export_path}/{file_name.replace('.mp3', '_(Vocals).wav')}"
path_out_instru_wav = f"{export_path}/{file_name.replace('.mp3', '_(Instrumental).wav')}"


# .wav to .mp3
def wav_to_mp3_return_out_path(path_wav) -> str:
    from pydub import AudioSegment
    path_mp3 = path_wav.replace('.wav', '.mp3')
    audio = AudioSegment.from_wav(path_wav)
    audio.export(path_mp3, format="mp3")
    print(f"Converted {path_wav} to {path_mp3}")
    return path_mp3


print('converting to mp3')
path_out_vocal_mp3 = wav_to_mp3_return_out_path(path_out_vocal_wav)
path_out_instru_mp3 = wav_to_mp3_return_out_path(path_out_instru_wav)


# compare test output
def are_mp3_files_same(path_1, path_2):
    audio1 = AudioSegment.from_mp3(path_1)
    audio2 = AudioSegment.from_mp3(path_2)
    result = audio1.raw_data == audio2.raw_data
    print(f'{result}: comparing', path_1, path_2)
    return result


path_expected_vocal = f'{input_folder}/expected-out-vocals.mp3'
path_expected_instru = f'{input_folder}/expected-out-instru.mp3'

assert are_mp3_files_same(path_expected_vocal, path_out_vocal_mp3)
assert are_mp3_files_same(path_expected_instru, path_out_instru_mp3)
print('this works great!!')
