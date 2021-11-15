import os
import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from quod_qa.wrapper_test.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from quod_qa.wrapper_test.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from quod_qa.wrapper_test import DataSet
from quod_qa.wrapper_test.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#text
text_pn = 'Pending New status'
text_n = 'New status'
text_pf = 'Partial fill'

#order param
qty = 300000
qty_nav = 250000
qty_twap_1 = 30000
side = 1
price = 29.995
price_nav = 30
tif_day = 0
order_type = 2
waves = 10
nav_exec = 1
nav_init_sweep = 10

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
instrument = DataSet.Instrument.BUI.value

def rule_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price_nav)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)

    return [nos_rule, nos_rule1, ocr_rule]

def execute(report_id):
    try:
        rule_list = rule_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        case_id_0 = bca.create_event("Send Market Data", case_id)
        FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data()

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)

        fix_message = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator()
        fix_message.add_ClordId((os.path.basename(__file__)[:-3]))
        fix_message.change_parameters(dict(Account= client,  OrderQty = qty))
        fix_message.update_fields_in_component('QuodFlatParameters', dict(NavigatorExecution= nav_exec, NavigatorLimitPrice= price_nav, NavigatorInitialSweepTime= nav_init_sweep, Waves= waves))

        fix_manager.send_message_and_receive_response(fix_message, case_id_1)

        time.sleep(3)

        # region Check Sell side
        fix_verifier_ss.check_fix_message(fix_message, direction=SECOND, message_name='Sell side 35=D')

        exec_report = FixMessageExecutionReportAlgo().execution_report(fix_message)
        fix_verifier_ss.check_fix_message(exec_report, message_name='Sell side Pending new')

        exec_report_2 = FixMessageExecutionReportAlgo().execution_report(fix_message).change_from_pending_new_to_new()
        fix_verifier_ss.check_fix_message(exec_report_2, message_name='Sell side New')
        # endregion

        # region Check Buy side
        case_id_2 = bca.create_event("First Navigator child", case_id)
        fix_verifier_bs.set_case_id(case_id_2)

        #NavSlice with NavigatorInitialSweepTime
        navigator_child_1 = FixMessageNewOrderSingleAlgo().set_DMA()
        navigator_child_1.change_parameters(dict(OrderQty=qty, Price=price_nav))
        fix_verifier_bs.check_fix_message(navigator_child_1, key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'], message_name='Buy side 35=D First Navigator')

        exec_report_3 = FixMessageExecutionReportAlgo().execution_report_buy(navigator_child_1)
        fix_verifier_bs.check_fix_message(exec_report_3, key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'], direction=SECOND, message_name='Buy side Pending new')

        exec_report_4 = FixMessageExecutionReportAlgo().execution_report_buy(navigator_child_1).change_buy_from_pending_new_to_new()
        fix_verifier_bs.check_fix_message(exec_report_4,key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'], direction=SECOND, message_name='Buy side New')


        # Check that FIXQUODSELL5 sent 35=8 new
        er_2 = dict(
            er_1,
            ExecType="0",
            OrdStatus='0',
            SettlDate='*',
            ExecRestatementReason='*',
            SecAltIDGrp= '*',
            Account= client
        )
        fix_verifier_ss.CheckExecutionReport(er_2, response_new_order_single, case=case_id_2, message_name='FIXQUODSELL7 sent 35=8 New', key_parameters=['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        #endregion
        time.sleep(15)

        #region 1st TWAP slice + Nav
        case_id_3 = bca.create_event("First slise", case_id)
        er_4 = {
            'Account': account,
            'ExecID': '*',
            'OrderQty': qty_twap_1,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'TimeInForce': tif_day,
            'ExecType': "A",
            'LeavesQty': qty_twap_1,
            'CumQty': '0',
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_pn,
            'Price': price,
            'ExDestination': ex_destination_1

        }
        fix_verifier_bs.CheckExecutionReport(er_4, response_new_order_single, direction=SECOND, case=case_id_3, message_name='FIXBUYTH2 sent 35=8 TWAP slice Pending New', key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_5 = dict(
            er_4,
            ExecType="0",
            OrdStatus='0',
            Text= text_n
        )
        fix_verifier_bs.CheckExecutionReport(er_5, response_new_order_single, direction=SECOND, case=case_id_3, message_name='FIXQUODSELL7 sent 35=8 TWAP slice New', key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        er_6 = {
            'Account': account,
            'ExecID': '*',
            'OrderQty': qty_nav,
            'OrderID': '*',
            'TransactTime': '*',
            'Side': side,
            'AvgPx': '0',
            'OrdStatus': 'A',
            'TimeInForce': tif_day,
            'ExecType': "A",
            'LeavesQty': qty_nav,
            'CumQty': '0',
            'OrdType': order_type,
            'ClOrdID': '*',
            'Text': text_pn,
            'Price': price_nav,
            'ExDestination': ex_destination_1

        }
        fix_verifier_bs.CheckExecutionReport(er_6, response_new_order_single, direction=SECOND, case=case_id_3,   message_name='FIXQUODSELL7 sent 35=8 Nav slice Pending New', key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

        # Check that FIXQUODSELL5 sent 35=8 new
        er_7 = dict(
            er_6,
            ExecType="0",
            OrdStatus='0',
            Text= text_n
        )
        fix_verifier_bs.CheckExecutionReport(er_7, response_new_order_single, direction=SECOND, case=case_id_3, message_name='FIXQUODSELL7 sent 35=8 Nav slice New', key_parameters=['OrdStatus', 'ExecType', 'OrderQty', 'Price'])

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
            'CumQty': '0',
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


    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rule_list)
