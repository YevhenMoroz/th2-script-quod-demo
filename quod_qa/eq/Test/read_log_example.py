import logging
import time
from datetime import datetime

from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):
    # Generation id and time for test run
    report_id = bca.create_event('Ziuban tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    Stubs.frontend_is_open = True
    try:
        verifier = Stubs.verifier
        dma_params = {
            'Account': "CLIENT1",
            'ClOrdID': bca.client_orderid(9),
            'HandlInst': "2",
            'Side': 1,
            'OrderQty': 100,
            'TimeInForce': "0",
            'Price': "20",
            'OrdType': "2",
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': {
                'Symbol': "FR0010542647_EUR",
                'SecurityID': "FR0010542647",
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR'
            },
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            "ExDestination": "XPAR"
        }
        responce = Stubs.fix_act.placeOrderFIX(
            request=convert_to_request(
            'Send NewOrderSingle',
            "gtwquod5",
            report_id,

        ))
        time.sleep(120)


        readlog_nos_params = {
            "AuthenticationBlock": {
                "UserID": "HD3",
                "RoleID": "HeadOfSaleDealer",
                "SessionKey": "*"
            },
            "NewOrderSingleBlock": {
                "ListingList": [
                    {
                        "ListingID": "*"
                    }
                ],
                "RouteList": [
                    {
                        "RouteID": "4"
                    }
                ],
                "Side": "Buy",
                "Price": '{:.9f}'.format(int("20")),
                "QtyType": '*',
                "OrdType": "Limit",
                "TimeInForce": "Day",
                "Currency": "EUR",
                "PositionEffect": "Open",
                "InstrID": "Tw0YIXMh7qxfYws80U9DCA",
                "ExecutionPolicy": "DMA",
                "ExternalCare": "No"
            }
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                "Readlog NewOrderSingle Received",
                bca.filter_to_grpc("OrderSubmit", readlog_nos_params),
                responce.checkpoint_id,
                'log30 5-ors',
                report_id
            )
        )

    except Exception:
        logging.error("Error execution", exc_info=True)
