import datetime
from service.controllers.request_invoice_controller import request_invoice_controller

def receive_sale_summary(sale_list, cuit="your_cuit", doc_tipo=96, doc_nro=12345678,
                       pto_vta=1, cbte_tipo=6, cond_iva_receptor=5, iva_id=5):
    """
    Builds the invoice JSON expected by AFIP from the sales list.
    """

    total_neto = 0.0
    total_iva = 0.0
    total_final = 0.0

    for unit in sale_list:
        quantity = unit.subquantity if unit.subquantity else 1
        price_excl_vat = float(unit.product.price_excl_vat)
        price_incl_vat = float(unit.product.price_incl_vat)
        customer_price = float(unit.product.customer_price)

        subtotal_excl_vat = price_excl_vat * quantity
        subtotal_incl_vat = price_incl_vat * quantity
        subtotal_customer = customer_price * quantity

        total_neto += subtotal_excl_vat
        total_iva += (subtotal_incl_vat - subtotal_excl_vat)
        total_final += subtotal_customer

    # Actual date in YYYYMMDD format.
    today_str = datetime.date.today().strftime("%Y%m%d")

    invoice_json = {
        "Auth": {
            "Cuit": cuit
        },
        "FeCAEReq": {
            "FeCabReq": {
                "CantReg": 1,
                "PtoVta": pto_vta,
                "CbteTipo": cbte_tipo
            },
            "FeDetReq": {
                "FECAEDetRequest": {
                    "Concepto": 1,
                    "DocTipo": doc_tipo,
                    "DocNro": doc_nro,
                    "CbteDesde": 1,
                    "CbteHasta": 1,
                    "CbteFch": today_str,
                    "ImpTotal": round(total_final, 2),
                    "ImpTotConc": 0.00,
                    "ImpNeto": round(total_neto, 2),
                    "ImpOpEx": 0.00,
                    "ImpTrib": 0.00,
                    "ImpIVA": round(total_iva, 2),
                    "MonId": "PES",
                    "MonCotiz": 1.00,
                    "CondicionIVAReceptorId": cond_iva_receptor,
                    "Iva": {
                        "AlicIva": {
                            "Id": iva_id,
                            "BaseImp": round(total_neto, 2),
                            "Importe": round(total_iva, 2)
                        }
                    }
                }
            }
        }
    }

    return invoice_json

def middleware_controller(sale_list):
    invoice_summary = receive_sale_summary(sale_list)
    print("=================")
    print(invoice_summary)
    print("=================")
    request_invoice_controller(invoice_summary)
