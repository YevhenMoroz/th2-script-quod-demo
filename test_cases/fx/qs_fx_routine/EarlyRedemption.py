import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo
from stubs import Stubs


def send_swap_and_filled(case_id):
    quote_req_id = bca.client_orderid(8)
    params = {
        'QuoteReqID': quote_req_id,
        'ClOrdID': "A0211460BPDE01",
        'NumOfCompetitors': "1",
        'InCompetition': "N",
        'NoRelatedSym': [{
            'Instrument': {
                'Symbol': "USD",
                'Product': "9",
            },
            "NoPartyIDs" : [
                {
                    "PartyID":"CLIENT1",
                    "PartyIDSource":"D",
                    "PartyRole":"1"
                },
                {
                    "PartyID": "CLIENT1",
                    "PartyIDSource": "D",
                    "PartyRole": "3"
                }
        ],
            'SettlDate': spo(),
            'MaturityDate': wk1(),
            'DayCount': "30/360",
            'Side': "2",
            'OrderQty': '1000000'
        }
        ]
    }


    act = Stubs.fix_act
    response = act.placeQuoteFIX(
        request=bca.convert_to_request(
            "QuoteRequest",
            "fix-sell-rfq-m-314-cnx",
            case_id,
            bca.message_to_grpc("QuoteRequest", params, "fix-sell-rfq-m-314-cnx")
        )
    )

def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)


