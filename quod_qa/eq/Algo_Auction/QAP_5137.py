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
from test_framework.old_wrappers.fix_message import FixMessage
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

waves = 4
historical_volume = 600
initial_multiplier = 200
percentage = 40
qty = 1200
child_qty = historical_volume * (percentage / 100) / (1 - percentage / 100) * (initial_multiplier/100)
price = 20
side = 1
tif = 2
ex_destination_1 = "XPAR"
client = "CLIENT2"
order_type = 2
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '704'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-buy-side-316-ganymede"
connectivity_sell_side = "fix-sell-side-316-ganymede"
connectivity_fh = 'fix-feed-handler-316-ganymede'

instrument = {
    'Symbol': 'FR0010436584',
    'SecurityID': 'FR0010436584',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XPAR'
}


def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(session=connectivity_buy_side,
                                                                         account=account,
                                                                         venue=ex_destination_1,
                                                                         price=price)
    ocr_rule = rule_manager.add_OrderCancelRequest(session=connectivity_buy_side,
                                                   account=account,
                                                   venue=ex_destination_1,
                                                   cancel=True)
    return [nos_rule, ocr_rule]


def rule_destroyer(list_rules):
    if list_rules != None:
        rule_manager = RuleManager()
        for rule in list_rules:
            rule_manager.remove_rule(rule)


def     execute(report_id):
    try:
        now = datetime.today() - timedelta(hours=2)
        rule_list = rule_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_manager_ss = FixManager(connectivity_sell_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        # region Send Market Data
        case_id_0 = bca.create_event("Send Market Data", case_id)
        market_data1 = {
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '20',
                    'MDEntrySize': '1000',
                    'MDEntryPositionNo': '1',
                    'TradingSessionSubID': '2',
                    'SecurityTradingStatus': '3'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '30',
                    'MDEntrySize': '1000',
                    'MDEntryPositionNo': '1',
                    'TradingSessionSubID': '2',
                    'SecurityTradingStatus': '3'
                }
            ]
        }
        message_1 = FixMessage(market_data1)
        fix_manager_fh.set_case_id(case_id_0)
        fix_manager_fh.Send_MarketDataFullSnapshotRefresh_FixMessage(fix_message=message_1, symbol=s_par,
                                                                     message_name="Send Trading phase")
        market_data2 = {
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '20',
                    'MDEntrySize': '100',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
                }
            ]
        }
        message_2 = FixMessage(market_data2)
        fix_manager_fh.Send_MarketDataIncrementalRefresh_FixMessage(fix_message=message_2, symbol=s_par,
                                                                    message_name="Send Last Traded Qty")
        # endregion

        # region Create algo order
        order_1 = {
            'Account': client,
            'HandlInst': 2,
            'Side': side,
            'OrderQty': qty,
            'TimeInForce': tif,
            'OrdType': order_type,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Price': price,
            'Currency': currency,
            'TargetStrategy': 1012,
            'ExDestination': ex_destination_1,
            'NoStrategyParameters': [
                {
                    'StrategyParameterName': 'StartDate',
                    'StrategyParameterType': '19',
                    'StrategyParameterValue': now.strftime("%Y%m%d-%H:%M:%S")
                },
                {
                    'StrategyParameterName': 'MaxParticipation',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': percentage
                },
                {
                    'StrategyParameterName': 'AuctionInitialSliceMultiplier',
                    'StrategyParameterType': '6',
                    'StrategyParameterValue': initial_multiplier
                }
            ]
        }
        case_id_1 = bca.create_event("Create algo order", case_id)
        fix_message_new_order_single = FixMessage(order_1)
        fix_message_new_order_single.add_random_ClOrdID()
        fix_manager_ss.set_case_id(case_id_1)
        responce = fix_manager_ss.Send_NewOrderSingle_FixMessage(fix_message=fix_message_new_order_single)

        nos_1 = dict(
            fix_message_new_order_single.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message_new_order_single.get_parameter('ClOrdID'))

        fix_verifier_ss.CheckNewOrderSingle(nos_1, responce, direction='SECOND', case=case_id_1,
                                            message_name='Sell-side receive 35=D')

        er_1 = {
            'ExecID': '*',
            'OrderQty': qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Currency': currency,
            'TimeInForce': tif,
            'ExecType': "A",
            'HandlInst': 2,
            'LeavesQty': qty,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': "A",
            'QtyType': '0',
            'Price': price,
            'Instrument': instrument

        }
        fix_verifier_ss.CheckExecutionReport(er_1, responce, case=case_id_1,
                                             message_name='Sell-side sent 35=8 Pending New',
                                             key_parameters=['ClOrdID', 'OrdStatus', 'ExecType', 'Price', 'OrderQty'])
        time.sleep(1)
        er_2 = dict(
            er_1,
            ExecType="0",
            OrdStatus='0',
            SettlType='*',
            SettlDate='*',
            ExecRestatementReason='*',
        )
        fix_verifier_ss.CheckExecutionReport(er_2, responce, case=case_id_1, message_name='Sell-side sent 35=8 New',
                                             key_parameters=['ClOrdID', 'OrdStatus', 'ExecType', 'Price', 'OrderQty'])
        # endregion

        # region Check buy side
        case_id_2 = bca.create_event("Check buy side", case_id)
        dma_order = {
            'NoParty': '*',
            'Account': account,
            'OrderQty': int(min(child_qty, qty)),
            'OrdType': order_type,
            'ClOrdID': '*',
            'OrderCapacity': "A",
            'TransactTime': '*',
            'Side': side,
            'Price': price,
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif,
            'Instrument': '*',
            'HandlInst': '1',
            'ExDestination': instrument['SecurityExchange']
        }
        fix_verifier_bs.CheckNewOrderSingle(dma_order, responce, case=case_id_2,
                                            message_name='NewOrderSingle sended to buy-side',
                                            key_parameters=['OrderQty', 'Price', 'Account', 'TimeInForce'])
        # Check that FIXBUYQUOD5 sent 35=8 IOC pending new
        er_3 = {
            'Account': account,
            'CumQty': '0',
            'ExecID': '*',
            'OrderQty': int(min(child_qty, qty)),
            'Text': '*',
            'OrdType': '2',
            'ClOrdID': '*',
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Price': price,
            'TimeInForce': tif,
            'ExecType': "A",
            'ExDestination': ex_destination_1,
            'LeavesQty': int(min(child_qty, qty))
        }

        fix_verifier_bs.CheckExecutionReport(er_3, responce, direction='SECOND', case=case_id_2,
                                             message_name='TH2 sim send ExecutionReport PendingNew',
                                             key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price',
                                                             'TimeInForce'])

        # Check that FIXBUYQUOD5 sent 35=8 new
        er_4 = dict(
            er_3,
            OrdStatus='0',
            ExecType="0"
        )
        fix_verifier_bs.CheckExecutionReport(er_4, responce, direction='SECOND', case=case_id_2,
                                             message_name='TH2 sim send ExecutionReport New',
                                             key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Price',
                                                             'TimeInForce'])

        # endregion

        # region Cancel algo order
        case_id_3 = bca.create_event("Cancel algo order", case_id)
        cancel_parms = {
            "ClOrdID": fix_message_new_order_single.get_ClOrdID(),
            "Account": fix_message_new_order_single.get_parameter('Account'),
            "Side": fix_message_new_order_single.get_parameter('Side'),
            "TransactTime": datetime.utcnow().isoformat(),
            "OrigClOrdID": fix_message_new_order_single.get_ClOrdID()
        }

        fix_cancel = FixMessage(cancel_parms)
        responce_cancel = fix_manager_ss.Send_OrderCancelRequest_FixMessage(fix_cancel, case=case_id_3)

        time.sleep(1)

        cancel_ss_param = {
            'Side': side,
            'Account': client,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'TransactTime': '*',
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
        }
        fix_verifier_ss.CheckOrderCancelRequest(cancel_ss_param, responce_cancel, direction='SECOND', case=case_id_3,
                                                message_name='Sell-side receive OrderCancelRequest',
                                                key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        er_5 = {
            'ExecID': '*',
            'OrderQty': qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': responce.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '*',
            "OrdStatus": "4",
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif,
            'ExecType': '4',
            'HandlInst': 2,
            'CxlQty': '*',
            'LeavesQty': '0',
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message_new_order_single.get_ClOrdID(),
            'OrderCapacity': 'A',
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'SettlType': '*',
            'Price': price,
            'Instrument': instrument,
            'OrigClOrdID': fix_message_new_order_single.get_ClOrdID()
        }
        fix_verifier_ss.CheckExecutionReport(er_5, responce_cancel, case=case_id_3,
                                             message_name='Sell-side send ExecutionReportCanceled',
                                             key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'ClOrdID'])
        time.sleep(2)
        # endregion
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_destroyer(rule_list)
