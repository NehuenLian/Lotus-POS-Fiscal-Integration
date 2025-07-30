from service.controllers.request_invoice_controller import \
    request_invoice_controller
from service.payload_builder.builder import build_sale_summary_payload
from service.utils.find_errors_in_response import response_has_errors
from service.utils.logger import console_logger, file_logger


def invoicing_controller(sale_object) -> bool:

    invoice_payload = build_sale_summary_payload(sale_object)
    CAE_response = request_invoice_controller(invoice_payload)

    if response_has_errors(CAE_response):
        console_logger.error("Middleware: response contains errors.")
        return False
    else:
        console_logger.debug("Middleware: invoice processed successfully.")
        return True
