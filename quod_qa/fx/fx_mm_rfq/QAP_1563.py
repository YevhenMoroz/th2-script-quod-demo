import logging
import os
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from custom.tenor_settlement_date import get_expire_time
from custom.verifier import Verifier as Ver, Verifier, VerificationMethod
from quod_qa.fx.default_params_fx import text_messages
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import (BaseTableDataRequest, ModificationRequest,
                                                          ExtractionDetailsRequest, RFQExtractionDetailsRequest)
from win_gui_modules.order_book_wrappers import ExtractionDetail, OrdersDetails, OrderInfo, ExtractionAction
from win_gui_modules.utils import prepare_fe_2, get_opened_fe, set_session_id, get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def prepare_fe(case_id, session_id):
    Stubs.frontend_is_open = True
    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
        # ,
        #          fe_dir='qf_trading_fe_folder_308',
        #          fe_user='qf_trading_fe_user_308',
        #          fe_pass='qf_trading_fe_password_308')
    else:
        get_opened_fe(case_id, session_id)


def send_rfq(reusable_params, ttl, case_params, case_id, act, rfq_id):
    print(f'quote sent with qty={reusable_params["OrderQty"]}')
    rfq_params = {
        'QuoteReqID': rfq_id,
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': reusable_params['OrderQty'],
            'OrdType': 'D',
            'ExpireTime': get_expire_time(ttl),
            'TransactTime': (datetime.utcnow().isoformat())}]
        }
    logger.debug("Send new order with ClOrdID = {}".format(rfq_params['QuoteReqID']))

    quote = act.placeQuoteFIX(
            bca.convert_to_request(
                    text_messages['sendQR'],
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params, case_params['TraderConnectivity'])
                    ))
    return quote


def send_incorrect_qty_order(reusable_params, send_rfq, act, connectivity, case_id, price):
    print('send_incorrect_qty_order')
    order_params = {
        **reusable_params,
        'QuoteID': send_rfq.response_messages_list[0].fields['QuoteID'],
        'ClOrdID': bca.client_orderid(9),
        'OrdType': 'D',
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': reusable_params['OrderQty'],
        'Price': price,
        'TimeInForce': 4
        }

    send_order = act.placeOrderFIX(
            bca.convert_to_request(
                    text_messages['sendNOS'],
                    connectivity,
                    case_id,
                    bca.message_to_grpc('NewOrderSingle', order_params, connectivity)
                    ))

    return send_order


def verify_ord_reject_fix(case_id, order, reusable_params, quote):
    print('verify_ord_reject_fix')
    ver = Ver(case_id)
    ver.set_event_name("Check Execution Report Fix Message")
    ver.compare_values('MsgType',
                       "8",
                       order.response_messages_list[0].fields['header'].message_value.fields['MsgType'].simple_value)
    ver.compare_values('OrderQty',
                       reusable_params['OrderQty'],
                       order.response_messages_list[0].fields['OrderQty'].simple_value)
    ver.compare_values('Price',
                       quote.response_messages_list[0].fields['OfferSpotRate'].simple_value,
                       order.response_messages_list[0].fields['Price'].simple_value,
                       VerificationMethod.NOT_EQUALS)
    ver.verify()


def check_ord_reject_fe(base_request, ob_service, case_id, order, exp_ord):
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id('ex_id')
    ob.set_filter(['ClOrdID', str(order.response_messages_list[0].fields['ClOrdID'].simple_value)])
    fre_notes = ExtractionDetail("orderBook.LmtPrice", "Limit Price")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob_exec_sts = ExtractionDetail("orderBook.ExecSts", "ExecSts")

    ob.add_single_order_info(
            OrderInfo.create(
                    action=ExtractionAction.create_extraction_action(extraction_details=[fre_notes,
                                                                                         ob_sts,
                                                                                         ob_exec_sts])))

    response = call(ob_service.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('FreeNotes', exp_ord, response[fre_notes.name])
    verifier.compare_values('Sts', 'Terminated', response[ob_sts.name])
    verifier.compare_values('ExecSts', 'Filled', response[ob_exec_sts.name])
    verifier.verify()


def execute(report_id, case_params, session_id):
    # region Preparation
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    act = Stubs.fix_act
    verifier = Stubs.verifier
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    seconds, nanos = bca.timestamps()  # Store case start time
    service = Stubs.win_act_dealer_intervention_service
    ob_service = Stubs.win_act_order_book
    ttl = 180
    base_request = get_base_request(session_id, case_id)

    print(tsd.spo())
    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT',
            'Product': '4',
            },
        'SettlDate': tsd.spo(),
        'SettlType': '2',
        'OrderQty': '2130000'
        }
    rfq_id = bca.client_orderid(9)
    # endregion
    try:
        quote = send_rfq(reusable_params, ttl, case_params, case_id, act, rfq_id)
        expected_price = f"{quote.response_messages_list[0].fields['OfferPx'].simple_value}4"

        order = send_incorrect_qty_order(reusable_params, quote, act, case_params['TraderConnectivity'],
                                         case_id, expected_price)

        verify_ord_reject_fix(case_id, order, reusable_params, quote)


        check_ord_reject_fe(base_request, ob_service, case_id, order, expected_price)



    except Exception as e:
        logging.error("Error execution", exc_info=True)
    # TODO: quod: add OrderBook clear filter
    # finally:
    #     try:
    #         clear_filters(base_request, service)
    #     except Exception:
    #         logging.error("Error finalization", exc_info=True)

    logger.info("Case {} was executed in {} sec.".format(
            case_name, str(round(datetime.now().timestamp() - seconds))))
