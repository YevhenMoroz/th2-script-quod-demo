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
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(report_id))
        checkpoint_id1 = checkpoint_response1.checkpoint
        # time.sleep(120)

        # 5XRAA7DXZg14IOkuNrAfsg = VETO.[PARIS]

        readlog_nos_params = {
            "AuthenticationBlock": {
                "UserID": "HD5",
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
                "SettlCurrency": "EUR",
                "OrdCapacity": "Agency",
                "TransactTime": "*",
                "MaxPriceLevels": "1",
                "ExecutionOnly": "No",
                "ClientInstructionsOnly": "No",
                "BookingType": "RegularBooking",
                "OrdQty": '{:.9f}'.format(int("800")),
                "AccountGroupID": "CLIENT1",
                "InstrID": "5XRAA7DXZg14IOkuNrAfsg",
                "ExecutionPolicy": "DMA",
                "ExternalCare": "No"
            }
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                "Readlog check OrderSubmit",
                bca.filter_to_grpc("OrderSubmit", readlog_nos_params),
                checkpoint_id1,
                'log305-ors',
                report_id
            )
        )

    except Exception:
        logging.error("Error execution", exc_info=True)
