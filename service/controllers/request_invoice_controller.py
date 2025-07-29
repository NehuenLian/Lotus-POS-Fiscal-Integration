from service.controllers.generate_invoice_controller import generate_invoice
from service.controllers.request_access_token_controller import (
    generate_token_from_existing, generate_token_from_scratch)
from service.utils.file_validations import xml_exists
from service.utils.logger import console_logger, file_logger
from service.xml_management.xml_builder import is_expired


def request_invoice_controller(parsed_data: dict) -> dict:

    # Main flow: validates the existence and validity of tickets and tokens to generate an AFIP/ARCA invoice

    console_logger.info("Starting the invoice request process...")
    console_logger.info("Checking if loginTicketResponse exists...")
    
    if xml_exists("loginTicketResponse.xml"):
        console_logger.info("loginTicketResponse exists.")
        console_logger.info("Checking if the token has expired...")
        is_token_expired = is_expired("loginTicketRequest.xml")

        if is_token_expired:
            console_logger.info("The token has expired")
            generate_token_from_scratch()
            CAE_response = generate_invoice(parsed_data)
        
        else:
            console_logger.info("The token is valid")
            CAE_response = generate_invoice(parsed_data)
        
    else:
        console_logger.info("loginTicketResponse does not exist.")
        console_logger.info("Checking if loginTicketRequest exists...")

        if xml_exists("loginTicketRequest.xml"):

            console_logger.info("loginTicketRequest exists.")
            console_logger.info("Checking if the <expirationTime> of loginTicketRequest has expired...")
            is_expiration_time_reached = is_expired("loginTicketRequest.xml")
            if is_expiration_time_reached:

                console_logger.info("<expirationTime> has expired. Generating a new one...")
                generate_token_from_scratch()
                CAE_response = generate_invoice(parsed_data)

            else:
                console_logger.info("<expirationTime> is still valid.")

                console_logger.info("Checking if the token has expired...")
                is_token_expired = is_expired("loginTicketRequest.xml")
                if is_token_expired:

                    console_logger.info("The token has expired, generating a new one...")
                    generate_token_from_scratch()
                    CAE_response = generate_invoice(parsed_data)

                else:
                    generate_token_from_existing()
                    CAE_response = generate_invoice(parsed_data)

        else:
            console_logger.info("loginTicketRequest does not exist. It needs to be generated from scratch.")
            console_logger.info("Generating token (loginTicketResponse)...")
            generate_token_from_scratch()
            CAE_response = generate_invoice(parsed_data)
        
    return CAE_response
