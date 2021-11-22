from copy import deepcopy
from datetime import datetime, timedelta
from custom import basic_custom_actions
from quod_qa.wrapper.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from custom import basic_custom_actions as bca
import logging

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

buy_connectivity = "fix-buy-317-standard-test"  # fix-buy-317ganymede-standard fix-bs-310-columbia fix-buy-317-standard-test
sell_connectivity = "fix-sell-317-standard-test"  # fix-sell-317ganymede-standard fix-ss-310-columbia-standart
# fix-sell-317-standard-test  fix-sell-310-newdict
bo_connectivity = "fix-sell-310-backoffice"  # fix-sell-310-backoffice  fix-sell-317-backoffice

def get_buy_connectivity():
    return buy_connectivity


def get_sell_connectivity():
    return sell_connectivity


def get_bo_connectivity():
    return bo_connectivity


def set_fix_order_detail(handl_inst, side, client, ord_type, qty, tif, price=None, stop_price=None, no_allocs=None,
                         instrument=None,currency='EUR',ListSeqNo=None):
    fix_params = {
        'Account': client,
        'OrderQtyData': {'OrderQty': qty},
        # 'OrderQty': qty,
        'HandlInst': handl_inst,
        'TimeInForce': tif,
        'OrdType': ord_type,
        'Side': side,
        'Price': price,
        'StopPx': stop_price,
        'ListSeqNo': ListSeqNo,
        'PreAllocGroup': {'NoAllocs': no_allocs},
        'ExpireDate': datetime.strftime(datetime.now() + timedelta(days=2), "%Y%m%d"),
        'TransactTime': datetime.utcnow().isoformat(),

        'Instrument': {
            'Symbol': 'FR0004186856_EUR',
            'SecurityID': 'FR0004186856',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        },
        'Currency': currency,
    }
    if price is None:
        fix_params.pop('Price')
    if stop_price is None:
        fix_params.pop('StopPx')
    if no_allocs is None:
        fix_params.pop('PreAllocGrp')
    if ListSeqNo is None:
        fix_params.pop('ListSeqNo')
    if instrument is not None:
        fix_params.update(Instrument=instrument)
    fix_message = FixMessage(fix_params)
    fix_message.add_random_ClOrdID()
    return fix_message.get_parameters()


def create_order_via_fix(case_id, handl_inst, side, client, ord_type, qty, tif, price=None,stop_price=None, no_allocs=None,
                         instrument=None, currency="EUR"):
    try:
        fix_manager = FixManager(sell_connectivity, case_id)
        fix_params = set_fix_order_detail(handl_inst, side, client, ord_type, qty, tif, price,stop_price, no_allocs,
                                          instrument,currency)
        fix_message = FixMessage(fix_params)
        response = fix_manager.Send_NewOrderSingle_FixMessage(fix_message)
        fix_params['response'] = response
        return fix_params
    except Exception:
        basic_custom_actions.create_event('Fail create_order_via_fix', status="FAIL")
        logger.error("Error execution", exc_info=True)


def amend_order_via_fix(case_id, fix_message, parametr_list):
    fix_manager = FixManager(sell_connectivity, case_id)
    fix_message = FixMessage(fix_message)
    fix_modify_message = deepcopy(fix_message)
    fix_modify_message.change_parameters(parametr_list)
    fix_modify_message.add_tag({'OrigClOrdID': fix_modify_message.get_ClOrdID()})
    try:
        fix_manager.Send_OrderCancelReplaceRequest_FixMessage(fix_modify_message, case=case_id)
    except Exception:
        logger.error("Error execution", exc_info=True)
        basic_custom_actions.create_event('Fail amend_order_via_fix', status="FAIL")


def cancel_order_via_fix(case_id, cl_order_id, org_cl_order_id, client, side):
    try:
        fix_manager_qtwquod = FixManager(sell_connectivity, case_id)
        cancel_parms = {
            "ClOrdID": cl_order_id,
            "Account": client,
            "Side": side,
            "TransactTime": datetime.utcnow().isoformat(),
            "OrigClOrdID": org_cl_order_id,
        }
        fix_cancel = FixMessage(cancel_parms)
        fix_manager_qtwquod.Send_OrderCancelRequest_FixMessage(fix_cancel)
    except Exception:
        basic_custom_actions.create_event('Fail cancel_order_via_fix', status="FAIL")
        logger.error("Error execution", exc_info=True)


def create_order_list_via_fix(case_id, no_orders: []):
    try:
        fix_manager = FixManager(sell_connectivity, case_id)
        fix_params = {
            'BidType': "1",
            'TotNoOrders': len(no_orders),
            'ListOrdGrp': {"NoOrders": no_orders},
        }

        fix_message = FixMessage(fix_params)
        fix_message.add_tag({'ListID': bca.client_orderid(10)})
        response = fix_manager.Send_NewOrderList_FixMessage(fix_message)
        fix_params['response'] = response
        return fix_params
    except Exception:
        basic_custom_actions.create_event('Fail create_order_list_via_fix', status="FAIL")
        logger.error("Error execution", exc_info=True)


def cancel_order_list_via_fix(case_id, list_id):
    try:
        fix_manager_qtwquod = FixManager(sell_connectivity, case_id)
        cancel_parms = {
            "ListID": list_id,
            "TransactTime": datetime.utcnow().isoformat(),
        }
        fix_cancel = FixMessage(cancel_parms)
        fix_manager_qtwquod.Send_ListCancelRequest_FixMessage(fix_cancel)
    except Exception:
        basic_custom_actions.create_event('Fail cancel_order_list_via_fix', status="FAIL")
        logger.error("Error execution", exc_info=True)
