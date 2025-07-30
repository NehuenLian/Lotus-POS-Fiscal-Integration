from service.response_errors_handler.sync_invoice_number_controller import \
    sync_invoice_number
from service.utils.logger import console_logger, file_logger


# Dictionary of known errors.
# Format: {Error code: Solution}
errors_catalog = {
    10016 : sync_invoice_number,
}

def handle_error(error_code: int, parsed_data: dict) -> dict:

    for error, handler in errors_catalog.items():
        if error_code == error:
            response = handler(parsed_data)
            console_logger.info("Error resolved. Retrying invoice submission")
            return response

    console_logger.error(f"Error code not found in the error catalog: {error_code}")
    file_logger.error(f"Error code not found in the error catalog: {error_code}")

    return parsed_data
