import os
import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# text
text_pn = 'Pending New status'
text_n = 'New status'
text_f = 'Fill'
text_c = 'order canceled'

# order param
avt = 10000     # average volume traded per minute
ast = avt * 5   # 5 average traded
qty = 300000
qty_nav_trade = 250000
qty_twap = 30000
last_nav_qty = qty - qty_nav_trade
waves = 10
qty_twap_1 = int(qty / waves)
first_reserve = max(ast, int(last_nav_qty * (1 - 1)))
reserve = max(first_reserve, int(qty_twap_1))
qty_nav_first = qty - reserve
qty_nav_second = qty - qty_nav_trade
price = 29.995  # Primary - 1 tick
price_nav = 30
nav_rebalance = 10

#Key parameters
key_params_cl = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price']
key_params=['OrdStatus', 'ExecType', 'OrderQty', 'Price']

#Gateway Side
gateway_side_buy = DataSet.GatewaySide.RBBuy
gateway_side_sell = DataSet.GatewaySide.Sell

#Status
status_pending = DataSet.Status.Pending
status_new = DataSet.Status.New
status_fill = DataSet.Status.Fill
status_cancel = DataSet.Status.Cancel

# venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

# connectivity
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
    nos_ioc = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, True)
    nos_trade_rule1 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price_nav, price_nav, qty_nav_trade, qty_nav_trade, 0)
    nos_trade_rule2 = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side, account, ex_destination_1, price_nav, price_nav, qty_nav_second, qty_nav_second, 0)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)

    return [nos_rule, nos_rule1, nos_ioc, nos_trade_rule1, nos_trade_rule2, ocr_rule]

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
        twap_nav_order.update_fields_in_component('QuodFlatParameters', dict(NavigatorLimitPrice = price_nav, Waves = waves, NavigatorRebalanceTime = nav_rebalance))
        fix_manager.send_message_and_receive_response(twap_nav_order, case_id_1)
        # endregion

        time.sleep(1)

        # region Check Sell side
        fix_verifier_ss.check_fix_message(twap_nav_order, direction=ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_pending)
        fix_verifier_ss.check_fix_message(pending_twap_nav_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_new)
        fix_verifier_ss.check_fix_message(new_twap_nav_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check Buy side
        # Check First TWAP child
        fix_verifier_bs.set_case_id(bca.create_event("First TWAP slise", case_id))

        twap_child_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        twap_child_1.change_parameters(dict(OrderQty=qty_twap_1, Price=price))
        fix_verifier_bs.check_fix_message(twap_child_1, key_parameters=key_params, message_name='Buy side NewOrderSingle TWAP child')

        pending_twap_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_child_1, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_twap_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew TWAP child')

        new_twap_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_child_1, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_twap_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New TWAP child')

        # Check First Navigator child
        nav_child_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        nav_child_1.change_parameters(dict(OrderQty=qty_nav_second, Price=price_nav))
        fix_verifier_bs.check_fix_message(nav_child_1, key_parameters=key_params, message_name='Buy side NewOrderSingle First Navigator')

        pending_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_1, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_nav_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew First Navigator')

        new_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_1, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_nav_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side New ExecReport First Navigator')

        time.sleep(1)

        cancel_twap_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_child_1, gateway_side_buy, status_cancel)
        fix_verifier_bs.check_fix_message(cancel_twap_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport Cancel First TWAP child')

        fill_nav_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_1, gateway_side_buy, status_fill)
        fix_verifier_bs.check_fix_message(fill_nav_child_1_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport Fill First Navigator')
        # endregion

        time.sleep(3)

        #region Rebalance
        fix_verifier_bs.set_case_id(bca.create_event("Rebalance", case_id))

        # Check Second Navigator child
        nav_child_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        nav_child_2.change_parameters(dict(OrderQty=qty_nav_second, Price=price_nav))
        fix_verifier_bs.check_fix_message(nav_child_2, key_parameters=key_params, message_name='Buy side NewOrderSingle Second Navigator')

        pending_nav_child_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_2, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_nav_child_2_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew Second Navigator')

        new_nav_child_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_2, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_nav_child_2_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New Second Navigator')

        time.sleep(10)

        fill_nav_child_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(nav_child_2, gateway_side_buy, status_fill)
        fix_verifier_bs.check_fix_message(fill_nav_child_2_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport Fill Second Navigator')
        #endregion

        #region Check Parent order fill
        fix_verifier_ss.set_case_id(bca.create_event("Check parent order Fill", case_id))

        fill_twap_nav_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_nav_order, gateway_side_sell, status_fill)
        fill_twap_nav_order_params.change_parameter('LastQty', qty_nav_second)
        fix_verifier_ss.check_fix_message(fill_twap_nav_order_params, key_parameters=key_params, message_name='Sell side ExecReport Fill')
        #endregion

    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(rules_list)
