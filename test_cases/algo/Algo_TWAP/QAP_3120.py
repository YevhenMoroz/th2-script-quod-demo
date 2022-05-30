import os
import logging
import time
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.algo_formulas_manager import AlgoFormulasManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# order param
tick = 0.005
qty = 2000
price = 10
tif_day = DataSet.TimeInForce.Day.value
tif_ioc = DataSet.TimeInForce.ImmediateOrCancel.value
waves = 2
aggressivity = 1
qty_twap_1 = AlgoFormulasManager.get_next_twap_slice(qty, waves)
qty_twap_2 = AlgoFormulasManager.get_next_twap_slice(qty - qty_twap_1, waves - 1)

# Key parameters
key_params_cl = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price']
key_params = ['OrdStatus', 'ExecType', 'OrderQty', 'Price']

# Gateway Side
gateway_side_buy = DataSet.GatewaySide.Buy
gateway_side_sell = DataSet.GatewaySide.Sell

# Status
status_pending = DataSet.Status.Pending
status_new = DataSet.Status.New
status_eliminate = DataSet.Status.Eliminate
status_cancel = DataSet.Status.Cancel

# venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '1015'

# connectivity
case_name = os.path.basename(__file__)
instrument = DataSet.Instrument.RF.value
FromQuod = DataSet.DirectionEnum.FromQuod
ToQuod = DataSet.DirectionEnum.ToQuod
connectivity_buy_side = "fix-bs-310-columbia"
connectivity_sell_side = "fix-ss-310-columbia-standart"
connectivity_fh = 'fix-fh-310-columbia'


def rules_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side, account, ex_destination_1, True, qty, price)
    ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, False)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)
    return [nos_rule, nos_ioc_rule, ocrr_rule, ocr_rule]


def execute(report_id):
    try:
        rules_list = rules_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        now = datetime.today() - timedelta(hours=2)

        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_verifier_bs = FixVerifier(connectivity_buy_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)

        # Send_MarkerData
        # fix_manager_fh.set_case_id(bca.create_event("Send Market Data", case_id))
        # market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        # market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=price_bid, MDEntrySize=qty)
        # market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=qty)
        # fix_manager_fh.send_message(market_data_snap_shot)

        # time.sleep(3)

        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)

        twap_order = FixMessageNewOrderSingleAlgo().set_TWAP_params()
        twap_order.add_ClordId((os.path.basename(__file__)[:-3]))
        twap_order.change_parameters(dict(Account=client, OrderQty=qty, Price=price))
        twap_order.update_fields_in_component('QuodFlatParameters', dict(StartDate2=now.strftime("%Y%m%d-%H:%M:%S"), EndDate2=(now + timedelta(minutes=2)).strftime( "%Y%m%d-%H:%M:%S"), Waves=waves, Aggressivity=aggressivity))

        fix_manager.send_message_and_receive_response(twap_order, case_id_1)

        time.sleep(3)

        # region Check Sell side
        fix_verifier_ss.check_fix_message(twap_order, direction=ToQuod, message_name='Sell side NewOrderSingle')

        pending_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_order, gateway_side_sell, status_pending)
        fix_verifier_ss.check_fix_message(pending_twap_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_order, gateway_side_sell, status_new)
        fix_verifier_ss.check_fix_message(new_twap_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # Check First TWAP child
        fix_verifier_bs.set_case_id(bca.create_event("First TWAP slice", case_id))

        twap_1_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        twap_1_child.change_parameters(dict(OrderQty=qty_twap_1, Price=price, TimeInForce=tif_day, Instrument=instrument))
        fix_verifier_bs.check_fix_message(twap_1_child, key_parameters=key_params, message_name='Buy side NewOrderSingle First TWAP child')

        pending_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_twap_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew First TWAP child')

        new_twap_1_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_1_child, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_twap_1_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New First TWAP child')

        #endregion
        time.sleep(65)

        # Check Second TWAP child
        fix_verifier_bs.set_case_id(bca.create_event("Second TWAP slice", case_id))

        twap_2_child = FixMessageNewOrderSingleAlgo().set_DMA_params()
        twap_2_child.change_parameters( dict(OrderQty=qty_twap_2, Price=price, TimeInForce=tif_day, Instrument=instrument))
        fix_verifier_bs.check_fix_message(twap_2_child, key_parameters=key_params, message_name='Buy side NewOrderSingle Second TWAP child')

        pending_twap_2_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_2_child, gateway_side_buy, status_pending)
        fix_verifier_bs.check_fix_message(pending_twap_2_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport PendingNew Second TWAP child')

        new_twap_2_child_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_2_child, gateway_side_buy, status_new)
        fix_verifier_bs.check_fix_message(new_twap_2_child_params, key_parameters=key_params, direction=ToQuod, message_name='Buy side ExecReport New Second TWAP child')

        #endregion

        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_4)
        # Cancel Order
        cancel_request_twap_order = FixMessageOrderCancelRequest(twap_order)
        fix_manager.send_message_and_receive_response(cancel_request_twap_order, case_id_4)
        fix_verifier_ss.check_fix_message(cancel_request_twap_order, direction=ToQuod, message_name='Buy side Cancel Request')

        cancel_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(twap_order, gateway_side_buy, status_cancel)
        fix_verifier_ss.check_fix_message(cancel_twap_order_params, key_parameters=key_params, message_name='Buy side ExecReport Cancel')
        # endregion

    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rules_list)

