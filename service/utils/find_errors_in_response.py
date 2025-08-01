from service.utils.logger import console_logger, file_logger


# Handle if response_cae_dict its None too.
def response_has_errors(response_cae_dict: dict) -> bool:
    
    if response_cae_dict['Errors']:
        console_logger.info("Errors identified in the response.")
        return True
    
    else:
        console_logger.info("No errors in the response.")
        return False