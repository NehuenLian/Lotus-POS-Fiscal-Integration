from service.payload_builder.builder import add_auth_to_payload
from service.response_errors_handler.error_handler import handle_error
from service.soap_management.analyze_response import find_error_code
from service.soap_management.soap_client import fecae_solicitar
from service.utils.convert_to_dict import convert_zeep_object_to_dict
from service.utils.find_errors_in_response import response_has_errors
from service.utils.logger import console_logger, file_logger
from service.xml_management.xml_builder import extract_token_and_sign_from_xml


def generate_invoice(parsed_data: dict) -> dict:

    console_logger.info("Generating invoice...")
    token, sign = extract_token_and_sign_from_xml("loginTicketResponse.xml")
    full_built_invoice = add_auth_to_payload(parsed_data, token, sign)
    
    returned_cae = fecae_solicitar(full_built_invoice)

    console_logger.info("Verifying if the response has errors...")
    if response_has_errors(returned_cae):
        console_logger.info("Response has errors. Resolving...")
        error_code = find_error_code(returned_cae)
        updated_parsed_data = handle_error(error_code, parsed_data)

        error_solved = response_has_errors(returned_cae) # Verify again
        if error_solved: 
            returned_cae = fecae_solicitar(updated_parsed_data)

    CAE_response = convert_zeep_object_to_dict(returned_cae)
    console_logger.info("Invoice generated.")

    return CAE_response 