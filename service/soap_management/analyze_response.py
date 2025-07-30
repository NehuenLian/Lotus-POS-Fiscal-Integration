from service.utils.logger import console_logger, file_logger


def find_error_code(response_cae_dict: dict) -> int:

    errors_level = response_cae_dict['Errors']

    err_level = errors_level['Err']

    error_code = err_level[0]['Code']
    error_message = err_level[0]['Msg']

    console_logger.debug(f'Error code: {error_code}')
    console_logger.debug(f'Error message: {error_message}')

    return error_code