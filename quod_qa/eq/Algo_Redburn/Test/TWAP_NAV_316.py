import os
import logging
import time
import math
from datetime import datetime, timedelta
from copy import deepcopy
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-buy-side-316-ganymede"
connectivity_sell_side = "fix-sell-side-316-ganymede"
connectivity_fh = 'fix-feed-handler-316-ganymede'

waves = 3
qty = 500000
child_day_qty = round(qty / waves)
text_pn = 'Pending New status'
text_n = 'New status'
text_ocrr = 'OCRRRule'
text_c = 'order canceled'
text_f = 'Fill'
text_ret = 'reached end time'
text_s = 'sim work'
text_r = 'order replaced'
side = 1
price = 110
tif_day = 0
tif_ioc = 3
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = 2
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

instrument = {
            'Symbol': 'FR0000062788_EUR',
            'SecurityID': 'FR0000062788',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

def send_market_data(symbol: str, case_id :str, market_data ):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntries': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', md_params, connectivity_fh)
    ))

def send_market_dataT(symbol: str, case_id :str, market_data ):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol,
            connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntriesIR': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataIncrementalRefresh', md_params, connectivity_fh)
    ))


def rule_creation():
    rule_manager = RuleManager()
    #nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, 110)
    #nos_iok = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, False, 10000, 110)
    nos_trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, 100, 100, 401574, 401574, 0)
    #ocrr = rule_manager.add_OrderCancelReplaceRequest(connectivity_buy_side, account, ex_destination_1, True)

    # nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    # nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price, price, child_day_qty - 1, child_day_qty - 1, 0)

    #ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [nos_trade_rule1]
    #return [nos_rule1, nos_rule, nos_trade_rule, ocr_rule, nos_trade_rule1]

def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def execute(report_id):
    try:
        rule_list = rule_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_manager_310 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
        market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '100',
                'MDEntrySize': '1000000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '105',
                'MDEntrySize': '1000000',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_0, market_data1)

        market_data2 = [
            {
                'MDUpdateAction': '0',
                'MDEntryType': '2',
                'MDEntryPx': 110,
                'MDEntrySize': 250000,
                'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
            }
        ]
        send_market_dataT(s_par, case_id_0, market_data2)


        case_id_1 = bca.create_event("Create Algo Order", case_id)

        new_order_single_params = {
            # 'header': {
            #     'OnBehalfOfCompID': 'kames_ul_DCOI'
            # },
            'Account': account,
            'ClOrdID': 'TWAP_NAV_05_01' + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif_day,
            'Price': price,
            'OrdType': order_type,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': currency,
            'TargetStrategy': 1005,
            'ExDestination': ex_destination_1,
            'QuodFlatParameters': {
                # 'MaxPercentageVolume': '10',
                'NavigatorPercentage': '100',
                # 'NavigatorMaxTotalShares': '500000',
                'NavigatorExecution': '1',
                # 'NavigatorInitialSweepTime': '5',
                'NavGuard': '0',
                'NavigatorLimitPrice': '100',
                #'NavigatorLimitPriceReference': 'LTP',
                # 'NavigatorLimitPriceOffset': '100',
                # 'NavigatorMaxSliceSize': '10000',
                # 'NavigatorMinBookReloadSeconds': '10',
                'NavigatorRebalanceTime': '10',
                #'AllowedVenues': 'XLON',
                #'StartDate2': '20211027-09:50:00.000',
                #'EndDate2': '20211026-10:20:00.000',
                #'Waves': '4',
                #'TriggerPriceRed': '112.42'
            }
        }

        # fix_message_new_order_single = FixMessage(new_order_single_params)
        # fix_message_new_order_single.add_random_ClOrdID()
        # responce_new_order_single = fix_manager_310.Send_NewOrderSingle_FixMessage(fix_message_new_order_single, case=case_id_1)

    except:
        logging.error("Error execution", exc_info=True)
    # finally:
    #     rule_destroyer(rule_list)
