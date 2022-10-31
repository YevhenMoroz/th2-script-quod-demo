import os
import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#order param
avt = 10000     # average volume traded per minute
ast = avt * 5   # 5 average traded
qty = 300000
qty_nav_trade = 200000
last_nav_qty = qty - qty_nav_trade
waves = 10
qty_twap_1 = int(last_nav_qty / waves)
first_reserve = max(ast, int(last_nav_qty * (1 - 1)))
reserve = max(first_reserve, int(qty_twap_1))
qty_nav = last_nav_qty - reserve
price = 29.995
price_nav = 30
nav_init_sweep = 10

#Key parameters
key_params_cl = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price']
key_params=['OrdStatus', 'ExecType', 'OrderQty', 'Price']

#Gateway Side
gateway_side_buy = DataSet.GatewaySide.Buy
gateway_side_sell = DataSet.GatewaySide.Sell

#Status
status_pending = DataSet.Status.Pending
status_new = DataSet.Status.New
status_partial_fill = DataSet.Status.PartialFill
status_cancel = DataSet.Status.Cancel

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
s_par = '555'

#connectivi
case_name = os.path.basename(__file__)
instrument = DataSet.Instrument.BUI
FromQuod = DataSet.DirectionEnum.FromQuod
ToQuod = DataSet.DirectionEnum.ToQuod
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value

def rules_creation():
    rule_manager = RuleManager(Simulators.algo)
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    nos_rule1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price_nav)
    nos_trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price_nav, price_nav, qty, qty_nav_trade, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)

    return [nos_rule, nos_rule1, nos_trade_rule1, ocr_rule]

def execute(report_id):
    try:
        rules_list = rules_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)

        # Send_MarkerData
        fix_manager_fh.set_case_id(bca.create_event("Send Market Data", case_id))
        market_data_snapshot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        fix_manager_fh.send_message(market_data_snapshot)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)

        twap_nav_order = FixMessageNewOrderSingleAlgo().set_TWAP_Navigator_params()
        twap_nav_order.add_ClordId((os.path.basename(__file__)[:-3]))
        twap_nav_order.change_parameters(dict(Account= client, OrderQty = qty))
        twap_nav_order.update_fields_in_component('QuodFlatParameters', dict(NavigatorLimitPrice= price_nav, NavigatorInitialSweepTime= nav_init_sweep, Waves = waves))
        fix_manager.send_message_and_receive_response(twap_nav_order, case_id_1)
        # endregion

        time.sleep(3)

        #region Check Sell side
        fix_verifier_ss.check_fix_message(twap_nav_order, direction=ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_pending)
        fix_verifier_ss.check_fix_message(pending_twap_nav_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_new)
        fix_verifier_ss.check_fix_message(new_twap_nav_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport New')
        #endregion

        # region Check Buy side
        fix_verifier_bs.set_case_id(bca.create_event("First Navigator child", case_id))

        #Check First Navigator child
        nav_child_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        nav_child_1.change_parameters(dict(OrderQty=qty, Price=price_nav))
        fix_verifier_bs.check_fix_message(nav_child_1, key_parameters=key_params, message_name='Buy side NewOrderSingle First Navigator')

        pending_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_1, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_nav_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew First Navigator')

        fill_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_1, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(fill_nav_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New First Navigator')

        time.sleep(15)

        #Check Fill First Navigator
        new_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_1, gateway_side_buy, status_partial_fill)
        new_nav_child_1_params.change_parameters(dict(CumQty=qty_nav_trade, LastQty=qty_nav_trade, LeavesQty=last_nav_qty))
        fix_verifier_bs.check_fix_message(new_nav_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PartialFill First Navigator')

        #Check First TWAP child
        fix_verifier_bs.set_case_id(bca.create_event("First TWAP slice", case_id))

        twap_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        twap_child.change_parameters(dict(OrderQty=qty_twap_1, Price=price))
        fix_verifier_bs.check_fix_message(twap_child, key_parameters=key_params, message_name='Buy side NewOrderSingle TWAP child')

        pending_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_child, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_twap_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew TWAP child')

        set_new_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_child, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(set_new_twap_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New TWAP child')

        #Check Second Navigator child
        nav_child_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        nav_child_2.change_parameters(dict(OrderQty=qty_nav, Price=price_nav))
        fix_verifier_bs.check_fix_message(nav_child_2, key_parameters=key_params, message_name='Buy side NewOrderSingle Second Navigator')

        pending_nav_child_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_2, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_nav_child_2_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew Second Navigator')

        new_nav_child_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_2, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_nav_child_2_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New Second Navigator')

        cancel_twap_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_child, gateway_side_buy, status_cancel)
        fix_verifier_bs.check_fix_message(cancel_twap_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport Cancel TWAP child')

        cancel_nav_child_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_2, gateway_side_buy, status_cancel)
        fix_verifier_bs.check_fix_message(cancel_nav_child_2_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport Cancel Second Navigator')
        # endregion

        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_4)
        # Cancel Order
        cancel_request_twap_nav_order = FixMessageOrderCancelRequest(twap_nav_order)
        fix_manager.send_message_and_receive_response(cancel_request_twap_nav_order, case_id_4)
        fix_verifier_ss.check_fix_message(cancel_request_twap_nav_order, direction=ToQuod, message_name='Sell side Cancel Request')

        cancel_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_cancel)
        cancel_twap_nav_order_params.change_parameters(dict(CumQty=qty_nav_trade, AvgPx=price_nav))
        fix_verifier_ss.check_fix_message(cancel_twap_nav_order_params, key_parameters=key_params, message_name='Sell side ExecReport Cancel')
        #endregion

    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(rules_list)
