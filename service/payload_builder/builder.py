import datetime

from service.utils.logger import console_logger, file_logger


def build_sale_summary_payload(sale_list: list) -> dict:

    # Sale info
    total_amount = sale_list.amount
    net_amount = sale_list.amount_excl_vat
    total_amount_iva = sale_list.amount_only_vat

    # Fiscal info
    cuit = 23904352345
    pto_vta = 1
    cbte_tipo = 6
    doc_tipo = 96
    doc_nro = 12345678
    cond_iva_receptor = 5
    iva_id = 5

    today = datetime.date.today().strftime("%Y%m%d")
    today_str = str(today)

    invoice_payload = {
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
                    "ImpTotal": total_amount,
                    "ImpTotConc": 0.0,
                    "ImpNeto": net_amount,
                    "ImpOpEx": 0.0,
                    "ImpTrib": 0.0,
                    "ImpIVA": total_amount_iva,
                    "MonId": "PES",
                    "MonCotiz": 1.0,
                    "CondicionIVAReceptorId": cond_iva_receptor,
                    "Iva": {
                        "AlicIva": {
                            "Id": iva_id,
                            "BaseImp": net_amount,
                            "Importe": total_amount_iva
                        }
                    }
                }
            }
        }
    }

    return invoice_payload

def add_auth_to_payload(sale_data: dict, token: str, sign: str) -> dict:
    
    sale_data['Auth']['Token'] = token
    sale_data['Auth']['Sign'] = sign
    console_logger.debug("Auth added to payload.")

    return sale_data

def extract_ptovta_and_cbtetipo(parsed_data: dict) -> tuple[int, str, str]:
    cuit = int(parsed_data["Auth"]["Cuit"])
    ptovta = int(parsed_data["FeCAEReq"]["FeCabReq"]["PtoVta"])
    cbtetipo = int(parsed_data["FeCAEReq"]["FeCabReq"]["CbteTipo"])

    return cuit, ptovta, cbtetipo

def build_auth(token: str, sign: str, cuit: int) -> dict:

    auth = {
        "Token" : token,
        "Sign" : sign,
        "Cuit" : cuit,
    }

    return auth

def extract_cbtenro(last_authorized_info: dict) -> int:
    """
    last_authorized_info structure:

    last_authorized_info = {
        'PtoVta': 1,
        'CbteTipo': 6,
        'CbteNro': 69,
        'Errors': None,
        'Events': None
    }

    """
    cbte_nro =  last_authorized_info['CbteNro']
    return cbte_nro

def update_sale_data(parsed_data: dict, cbte_nro: int) -> dict:

    parsed_data['FeCAEReq']['FeDetReq']['FECAEDetRequest']['CbteDesde'] = cbte_nro + 1
    parsed_data['FeCAEReq']['FeDetReq']['FECAEDetRequest']['CbteHasta'] = cbte_nro + 1
    
    updated_invoice = parsed_data

    return updated_invoice
