import logging
import requests
from time import time

import consts


def download_model(model_name=consts.DEFAULT_MODEL_NAME):
    """
    because hosting large file on GitHub is not free
    for now let's download it everytime
    we can move this to S3 later
    """
    logging.info(f"Downloading model {model_name}")
    start_time = time()
    file_name = consts.MODEL_NAME_TO_FILE_NAME_MAP[model_name]
    url = "https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/" + file_name
    save_path = './models/MDX_Net_Models/'+file_name

    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    logging.info(f"Model file {file_name} downloaded successfully and saved to {save_path} in {time() - start_time} seconds")


if __name__ == '__main__':
    download_model(consts.DEFAULT_MODEL_NAME)
