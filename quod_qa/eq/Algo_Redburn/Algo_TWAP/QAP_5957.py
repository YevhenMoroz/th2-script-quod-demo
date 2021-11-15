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

# text
text_pn = 'Pending New status'
text_n = 'New status'
text_f = 'Fill'
text_c = 'order canceled'

# order param
qty = 300000
qty_nav_trade = 250000
qty_nav_second = qty - qty_nav_trade
qty_twap = 30000
side = 1
price = 29.995  # Primary - 1 tick
price_nav = 30
tif_day = 0
order_type = 2
waves = 10
nav_exec = 1
nav_rebalance = 10

# venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

# connectivity
case_name = os.path.basename(__file__)
FIRST = DataSet.DirectionEnum.FromQuod.value
SECOND = DataSet.DirectionEnum.ToQuod.value
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value
instrument = DataSet.Instrument.BUI.value


def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                         ex_destination_1, price)
    nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account,
                                                                          ex_destination_1, price_nav)
    nos_ioc = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, True)
    nos_trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account,
                                                                                ex_destination_1, price_nav, price_nav,
                                                                                qty_nav_trade, qty_nav_trade, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)

    return [nos_rule, nos_rule1, nos_ioc, nos_trade_rule1, ocr_rule]


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

        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)

        fix_message = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator()
        fix_message.add_ClordId((os.path.basename(__file__)[:-3]))
        fix_message.change_parameters(dict(Account=client, OrderQty=qty))
        fix_message.update_fields_in_component('QuodFlatParameters', dict(NavigatorExecution = nav_exec, NavigatorLimitPrice = price_nav, Waves = waves, NavigatorRebalanceTime = nav_rebalance))

        fix_manager = FixManager(connectivity_sell_side, case_id)
        response_new_order_single = fix_manager.send_message_and_receive_response(fix_message, case_id_1)

        time.sleep(1)

        nos_1 = dict(
            fix_message.get_parameters(),
            TransactTime='*',
            ClOrdID=fix_message.get_parameter('ClOrdID'))

        fix_verifier_ss.CheckNewOrderSingle(nos_1, response_new_order_single, direction='SECOND', case=case_id_1,
                                            message_name='FIXQUODSELL7 receive 35=D')

        # region 1st TWAP slice + Navigator
        case_id_2 = bca.create_event("First slise", case_id)
        er_1 = {
            'Account': account,
            'ExecID': '*',
            'OrderQty': qty_twap,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'TimeInForce': tif_day,
            'ExecType': "A",
            'LeavesQty': qty_twap,
            'CumQty': '0',
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_pn,
            'Price': price,
            'ExDestination': ex_destination_1

        }
        fix_verifier_bs.CheckExecutionReport(er_1, response_new_order_single, direction=SECOND, case=case_id_2,
                                             message_name='FIXBUYTH2 sent 35=8 TWAP slice Pending New',
                                             key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_2 = dict(
            er_1,
            ExecType="0",
            OrdStatus='0',
            Text=text_n
        )
        fix_verifier_bs.CheckExecutionReport(er_2, response_new_order_single, direction=SECOND, case=case_id_2,
                                             message_name='FIXQUODSELL7 sent 35=8 TWAP slice New',
                                             key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        er_3 = {
            'Account': account,
            'ExecID': '*',
            'OrderQty': qty_nav_trade,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'TimeInForce': tif_day,
            'ExecType': "A",
            'LeavesQty': qty_nav_trade,
            'CumQty': '0',
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_pn,
            'Price': price_nav,
            'ExDestination': ex_destination_1

        }
        fix_verifier_bs.CheckExecutionReport(er_3, response_new_order_single, direction=SECOND, case=case_id_2,
                                             message_name='FIXQUODSELL7 sent 35=8 Navigator slice Pending New',
                                             key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_4 = dict(
            er_3,
            ExecType="0",
            OrdStatus='0',
            Text=text_n
        )
        fix_verifier_bs.CheckExecutionReport(er_4, response_new_order_single, direction=SECOND, case=case_id_2,
                                             message_name='FIXQUODSELL7 sent 35=8 Navigator slice New',
                                             key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        time.sleep(2)

        # Fill First Navigator child order
        er_5 = {
            'Account': account,
            'CumQty': qty_nav_trade,
            'LastPx': price_nav,
            'ExecID': '*',
            'OrderQty': qty_nav_trade,
            'OrdType': order_type,
            'ClOrdID': '*',
            'LastQty': qty_nav_trade,
            'Text': text_f,
            'OrderCapacity': fix_message.get_parameter('OrderCapacity'),
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '*',
            'OrdStatus': '2',
            'Price': price_nav,
            'Currency': currency,
            'TimeInForce': tif_day,
            'Instrument': '*',
            'ExecType': "F",
            'LeavesQty': '0'
        }
        fix_verifier_bs.CheckExecutionReport(er_5, response_new_order_single, direction=SECOND, case=case_id_2,
                                             message_name='BS FIXBUYTH2 sent 35=8 Navigator Fill',
                                             key_parameters=['OrderQty', 'ExecType', 'OrdStatus', 'Text', 'Price'])

        # Cancel First TWAP child order
        er_6 = {
            'ExecID': '*',
            'OrderQty': qty_twap,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': '4',
            'ExecType': "4",
            'LeavesQty': '0',
            'CumQty': '0',
            'ClOrdID': '*',
            'Text': text_c,
            'OrigClOrdID': '*'
        }
        fix_verifier_bs.CheckExecutionReport(er_6, response_new_order_single, direction=SECOND, case=case_id_2,
                                             message_name='FIXBUYTH2 sent 35=8 TWAP slice Cancelled',
                                             key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Text'])
        # endregion

        time.sleep(3)

        case_id_3 = bca.create_event("Rebalance", case_id)
        # region Rebalance
        er_7 = {
            'Account': account,
            'ExecID': '*',
            'OrderQty': qty_nav_second,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'TimeInForce': tif_day,
            'ExecType': "A",
            'LeavesQty': qty_nav_second,
            'CumQty': '0',
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_pn,
            'Price': price_nav,
            'ExDestination': ex_destination_1

        }
        fix_verifier_bs.CheckExecutionReport(er_7, response_new_order_single, direction=SECOND, case=case_id_3,
                                             message_name='FIXQUODSELL7 sent 35=8 Navigator slice Pending New',
                                             key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_8 = dict(
            er_7,
            ExecType="0",
            OrdStatus='0',
            Text=text_n
        )
        fix_verifier_bs.CheckExecutionReport(er_8, response_new_order_single, direction=SECOND, case=case_id_3,
                                             message_name='FIXQUODSELL7 sent 35=8 Navigator slice New',
                                             key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        #endregion

        time.sleep(10)

        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", case_id)
        # Cancel Order
        fix_cancel = FixMessageOrderCancelRequest(fix_message)
        responce_cancel = fix_manager_316.send_message_and_receive_response(fix_cancel, case_id_4)

        time.sleep(1)

        # Check SS sent 35=F
        cancel_ss_param = {
            'Side': side,
            'Account': client,
            'ClOrdID': fix_cancel.get_parameter('ClOrdID'),
            'TransactTime': '*',
            'OrigClOrdID': fix_message.get_parameter('ClOrdID')
        }
        fix_verifier_ss.CheckOrderCancelRequest(cancel_ss_param, responce_cancel, direction='SECOND', case=case_id_4,
                                                message_name='SS FIXSELLQUOD7 sent 35=F Cancel',
                                                key_parameters=['OrderQty', 'ExecType', 'OrdStatus'])

        time.sleep(1)

        # Check ss (on FIXQUODSELL5 sent 35=8 on cancel)
        er_11 = {
            'Account': client,
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
            'LeavesQty': '0',
            'NoParty': '*',
            'CumQty': qty_nav_trade,
            'LastPx': '0',
            'OrdType': order_type,
            'ClOrdID': fix_cancel.get_parameter('ClOrdID'),
            'SecAltIDGrp': '*',
            'OrderCapacity': fix_message.get_parameter('OrderCapacity'),
            'QtyType': '0',
            'ExecRestatementReason': '*',
            'Price': price_nav,
            'TargetStrategy': fix_message.get_parameter('TargetStrategy'),
            'Instrument': instrument,
            'OrigClOrdID': fix_message.get_parameter('ClOrdID')
        }

        fix_verifier_ss.CheckExecutionReport(er_11, responce_cancel, case=case_id_4,
                                             message_name='SS FIXSELLQUOD5 sent 35=8 Cancel',
                                             key_parameters=['Price', 'OrderQty', 'ExecType', 'OrdStatus', 'ClOrdID'])

    # endregion
    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rule_list)
