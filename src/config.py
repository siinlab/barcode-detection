from os.path import join, dirname
from os import environ

__MODELS_PATH = join(dirname(__file__), '..', 'models')


def __get_model_path(model_name: str) -> str:
    """ Get the path to the model.

    Args:
        model_name (str): The name of the model.

    Returns:
        str: The path to the model.
    """
    return join(__MODELS_PATH, model_name, 'best.pt')


BARCODE_PATH =  __get_model_path('barcode-model')
BARCODE_DECODER_PATH = __get_model_path('barcode-decoder')

API_KEY_URL = environ.get('API_KEY_URL', 'https://localhost:7777/user/api-key/verify')