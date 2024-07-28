import logging

import requests
from time import time

import consts
import utils
from gui_data.constants import MDX_ARCH_TYPE
from separate import SeperateMDX, SeperateMDXC
from UVR import ModelData, MainWindow, init_root


def _do_nothing(*args, **kwargs):
    pass


def _return_none(*args, **kwargs):
    return None, None


def _wav_to_mp3_return_out_path(path_wav) -> str:
    from pydub import AudioSegment
    path_mp3 = path_wav.replace('.wav', '.mp3')
    audio = AudioSegment.from_wav(path_wav)
    audio.export(path_mp3, format="mp3")
    logging.info(f"Converted {path_wav} to {path_mp3}")
    return path_mp3


def separate_mp3_tracks(
        in_file_path: str,
        out_dir_path:str,
        model_name=consts.DEFAULT_MODEL_NAME,
        arch_type=consts.DEFAULT_ARCH_TYPE
) -> list[str]:
    # Initialize
    root = MainWindow()
    init_root(root)
    root.is_root_defined_var.set(True)  # possibly removed
    root.is_check_splash = True  # possibly removed

    current_model = ModelData(model_name, arch_type)
    current_model.mdxnet_stem_select = 'Vocals'
    input_file_name_no_extension = in_file_path.split('/')[-1].split('.')[0]

    process_data = {
        'model_data': current_model,
        'export_path': out_dir_path,
        'audio_file_base': input_file_name_no_extension,
        'audio_file': in_file_path,
        'set_progress_bar': _do_nothing,
        'write_to_console': _do_nothing,
        'process_iteration': _do_nothing,
        'cached_source_callback': _return_none,
        'cached_model_source_holder': _do_nothing,
        'list_all_models': [model_name],
        'is_ensemble_master': False,
        'is_4_stem_ensemble': False
    }

    logging.info(f'current_model.process_method {current_model.process_method}')
    logging.info(f'current_model.is_mdx_c {current_model.is_mdx_c}')

    # if current_model.process_method == VR_ARCH_TYPE:
    #     seperator = SeperateVR(current_model, process_data)
    # if current_model.process_method == DEMUCS_ARCH_TYPE:
    #     seperator = SeperateDemucs(current_model, process_data)

    # Only allow this arch type for now
    if current_model.process_method == MDX_ARCH_TYPE:
        seperator = SeperateMDXC(current_model, process_data) if current_model.is_mdx_c else SeperateMDX(current_model, process_data)

    # Separate
    logging.info('Separating Track')
    start_time = time()
    seperator.seperate()
    logging.info(f'Finished in {time() - start_time} seconds')

    logging.info('Converting to mp3')
    path_out_vocal_wav = f"{out_dir_path}/{input_file_name_no_extension}_(Vocals).wav"
    path_out_instru_wav = f"{out_dir_path}/{input_file_name_no_extension}_(Instrumental).wav"
    path_out_vocal_mp3 = _wav_to_mp3_return_out_path(path_out_vocal_wav)
    path_out_instru_mp3 = _wav_to_mp3_return_out_path(path_out_instru_wav)

    logging.info('Tracks ready')
    logging.info(path_out_vocal_mp3)
    logging.info(path_out_instru_mp3)

    return [path_out_vocal_mp3, path_out_instru_mp3]
