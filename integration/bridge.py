from service.controllers.request_invoice_controller import \
    request_invoice_controller
from service.payload_builder.builder import build_sale_summary_payload


def middleware_controller(sale_object):
    invoice_payload = build_sale_summary_payload(sale_object)
    request_invoice_controller(invoice_payload)
