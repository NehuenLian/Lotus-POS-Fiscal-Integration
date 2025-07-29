import datetime

from service.controllers.request_invoice_controller import \
    request_invoice_controller


def receive_sale_summary2(sale_list: list) -> dict:

    # Sale info
    imp_total = sale_list.amount
    imp_neto = sale_list.amount_excl_vat
    imp_total_iva = sale_list.amount_incl_vat

    # Fiscal info
    cuit = 29034857234
    pto_vta = 1
    cbte_tipo = 6
    doc_tipo = 96
    doc_nro = 12345678
    cond_iva_receptor = 5
    iva_id = 5

    today = datetime.date.today().strftime("%Y%m%d")
    today_str = str(today)

    invoice = {
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
                    "CbteDesde": 69,
                    "CbteHasta": 69,
                    "CbteFch": today_str,
                    "ImpTotal": imp_total,
                    "ImpTotConc": 0.0,
                    "ImpNeto": imp_neto,
                    "ImpOpEx": 0.0,
                    "ImpTrib": 0.0,
                    "ImpIVA": imp_total_iva,
                    "MonId": "PES",
                    "MonCotiz": 1.0,
                    "CondicionIVAReceptorId": cond_iva_receptor,
                    "Iva": {
                        "AlicIva": {
                            "Id": iva_id,
                            "BaseImp": imp_neto,
                            "Importe": imp_total_iva
                        }
                    }
                }
            }
        }
    }

    return invoice

def middleware_controller(sale_object):
    invoice = receive_sale_summary2(sale_object)
    request_invoice_controller(invoice)
