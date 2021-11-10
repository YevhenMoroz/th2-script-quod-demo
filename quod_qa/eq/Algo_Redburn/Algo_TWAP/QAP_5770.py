import os
import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from quod_qa.wrapper_test.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from quod_qa.wrapper_test import DataSet
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#text
text_pn = 'Pending New status'
text_n = 'New status'
text_pf = 'Partial fill'

#order param
qty = 300000
qty_nav_trade = 200000
qty_nav = 50000
qty_twap_1 = 5000
side = 1
price = 110
price_nav = 30
tif_day = 0
order_type = 2

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

#connectivity
case_name = os.path.basename(__file__)
FIRST = DataSet.DirectionEnum.FIRST.value
SECOND = DataSet.DirectionEnum.SECOND.value
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value
instrument = DataSet.Instrument.FR0000062788.value

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price_nav)
    nos_trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price_nav, price_nav, qty, qty_nav_trade, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)

    return [nos_rule, nos_rule1, nos_trade_rule1, ocr_rule]


def send_market_data(symbol: str, case_id: str, market_data):
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


def send_market_dataT(symbol: str, case_id: str, market_data):
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


def execute(report_id):
    try:
        rule_list = rule_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_manager_316 = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
        market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '100000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '40',
                'MDEntrySize': '100000',
                'MDEntryPositionNo': '1'
            }
        ]
        send_market_data(s_par, case_id_0, market_data1)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)

        fix_message = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator()
        fix_message.add_ClordId('QAP_5766')
        fix_message.change_parameters(dict(Account= client,  OrderQty = qty))
        fix_message.update_fields_in_component('QuodFlatParameters', dict(NavigatorExecution= 1, NavigatorLimitPrice= price_nav, Waves = 3))

        fix_manager = FixManager(connectivity_sell_side, case_id)
        response_new_order_single = fix_manager.send_message_and_receive_response(fix_message)

        time.sleep(1)

        nos_1 = dict(
            fix_message.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message.get_parameter('ClOrdID'))

        fix_verifier_ss.CheckNewOrderSingle(nos_1, response_new_order_single, direction='SECOND', case=case_id_1, message_name='FIXQUODSELL7 receive 35=D')

        #region NavSlice with NavigatorInitialSweepTime
        #Check that FIXQUODSELL5 sent 35=8 pending new
        case_id_2 = bca.create_event("Nav child", case_id)
        er_1 = {
            'Account': client,
            'ExecID': '*',
            'OrderQty': qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': response_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Currency': currency,
            'TimeInForce': tif_day,
            'ExecType': "A",
            'HandlInst': fix_message.get_parameter('HandlInst'),
            'LeavesQty': qty,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message.get_parameter('ClOrdID'),
            'OrderCapacity': fix_message.get_parameter('OrderCapacity'),
            'QtyType': '0',
            'Price': price_nav,
            'TargetStrategy': fix_message.get_parameter('TargetStrategy'),
            'Instrument': instrument

        }
        fix_verifier_ss.CheckExecutionReport(er_1, response_new_order_single, case=case_id_2,   message_name='FIXQUODSELL7 sent 35=8 Pending New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_2 = dict(
            er_1,
            ExecType="0",
            OrdStatus='0',
            SettlDate='*',
            SettlType='*',
            ExecRestatementReason='*',
        )
        er_2.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_2, response_new_order_single, case=case_id_2, message_name='FIXQUODSELL7 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        er_3 = {
            'Account': account,
            'CumQty': qty_nav_trade,
            'LastPx': price_nav,
            'ExecID': '*',
            'OrderQty': qty,
            'OrdType': order_type,
            'ClOrdID': '*',
            'LastQty': qty,
            'Text': text_pf,
            'OrderCapacity': fix_message.get_parameter('OrderCapacity'),
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '*',
            'OrdStatus': '1',
            'Price': price_nav,
            'Currency': currency,
            'TimeInForce': tif_day,
            'Instrument': '*',
            'ExecType': "F",
            'ExDestination': ex_destination_1,
            'LeavesQty': '0'
        }
        fix_verifier_bs.CheckExecutionReport(er_3, response_new_order_single, direction='SECOND', case=case_id_2, message_name='BS FIXBUYTH2 sent 35=8 Nav Partical Fill',key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])
        #endregion
        time.sleep(15)

        #region 1st TWAP slice + Nav
        case_id_3 = bca.create_event("1st TWAP slise", case_id)
        er_4 = {
            'Account': client,
            'ExecID': '*',
            'OrderQty': qty_twap_1,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': response_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Currency': currency,
            'TimeInForce': tif_day,
            'ExecType': "A",
            'HandlInst': fix_message.get_parameter('HandlInst'),
            'LeavesQty': qty_twap_1,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message.get_parameter('ClOrdID'),
            'OrderCapacity': fix_message.get_parameter('OrderCapacity'),
            'QtyType': '0',
            'Price': price,
            'TargetStrategy': fix_message.get_parameter('TargetStrategy'),
            'Instrument': instrument

        }
        fix_verifier_ss.CheckExecutionReport(er_4, response_new_order_single, case=case_id_3,   message_name='FIXQUODSELL7 sent 35=8 TWAP slice Pending New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_5 = dict(
            er_4,
            ExecType="0",
            OrdStatus='0',
            SettlDate='*',
            SettlType='*',
            ExecRestatementReason='*',
        )
        er_5.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_5, response_new_order_single, case=case_id_3, message_name='FIXQUODSELL7 sent 35=8 TWAP slice New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        er_6 = {
            'Account': client,
            'ExecID': '*',
            'OrderQty': qty_nav,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': response_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'Currency': currency,
            'TimeInForce': tif_day,
            'ExecType': "A",
            'HandlInst': fix_message.get_parameter('HandlInst'),
            'LeavesQty': qty_nav,
            'NoParty': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message.get_parameter('ClOrdID'),
            'OrderCapacity': fix_message.get_parameter('OrderCapacity'),
            'QtyType': '0',
            'Price': price_nav,
            'TargetStrategy': fix_message.get_parameter('TargetStrategy'),
            'Instrument': instrument

        }
        fix_verifier_ss.CheckExecutionReport(er_6, response_new_order_single, case=case_id_3,   message_name='FIXQUODSELL7 sent 35=8 Nav slice Pending New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_7 = dict(
            er_6,
            ExecType="0",
            OrdStatus='0',
            SettlDate='*',
            SettlType='*',
            ExecRestatementReason='*',
        )
        er_7.pop('Account')
        fix_verifier_ss.CheckExecutionReport(er_7, response_new_order_single, case=case_id_3, message_name='FIXQUODSELL7 sent 35=8 Nav slice New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType'])

        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", case_id)
        # Cancel Order
        cancel_parms = {
            "ClOrdID": fix_message.get_parameter('ClOrdID'),
            "Account": fix_message.get_parameter('Account'),
            "Side": fix_message.get_parameter('Side'),
            "TransactTime": datetime.utcnow().isoformat(),
            "OrigClOrdID": fix_message.get_parameter('ClOrdID')
        }

        fix_cancel = FixMessageOrderCancelRequest(parameters= cancel_parms)
        responce_cancel = fix_manager_316.send_message_and_receive_response(fix_cancel)

        time.sleep(1)

        # Check SS sent 35=F
        cancel_ss_param = {
            'Side': side,
            'Account': client,
            'ClOrdID': fix_message.get_parameter('ClOrdID'),
            'TransactTime': '*',
            'OrigClOrdID': fix_message.get_parameter('ClOrdID')
        }
        fix_verifier_ss.CheckOrderCancelRequest(cancel_ss_param, responce_cancel, direction='SECOND', case=case_id_4,
                                                message_name='SS FIXSELLQUOD7 sent 35=F Cancel',
                                                key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        time.sleep(1)

        # Check ss (on FIXQUODSELL5 sent 35=8 on cancel)
        er_11 = {
            'ExecID': '*',
            'OrderQty': qty,
            'NoStrategyParameters': '*',
            'LastQty': '0',
            'OrderID': response_new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '*',
            "OrdStatus": "4",
            'SettlDate': '*',
            'Currency': currency,
            'TimeInForce': tif_day,
            'ExecType': '4',
            'HandlInst': fix_message.get_parameter('HandlInst'),
            'CxlQty': '*',
            'LeavesQty': '0',
            'NoParty': '*',
            'CumQty': qty_nav_trade,
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_message.get_parameter('ClOrdID'),
            'OrderCapacity': fix_message.get_parameter('OrderCapacity'),
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'SettlType': '*',
            'Price': price,
            'TargetStrategy': fix_message.get_parameter('TargetStrategy'),
            'Instrument': instrument,
            'OrigClOrdID': fix_message.get_parameter('ClOrdID')
        }

        fix_verifier_ss.CheckExecutionReport(er_11, responce_cancel, case=case_id_4,
                                             message_name='SS FIXSELLQUOD5 sent 35=8 Cancel',
                                             key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'ClOrdID'])


    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rule_list)
