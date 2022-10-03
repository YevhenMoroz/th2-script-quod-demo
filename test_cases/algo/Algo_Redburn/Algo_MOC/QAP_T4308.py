import os
import logging
import time
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#order param
qty = 100000
price = 30
would_price_offset = 5
text_reject_would_price_reference = DataSet.FreeNotesReject.MissWouldPriceReference.value
tif_atc = DataSet.TimeInForce.AtTheClose.value

#Key parameters
key_params_cl = ['ClOrdID', 'OrdStatus', 'ExecType', 'OrderQty', 'Price']
key_params=['OrdStatus', 'ExecType', 'OrderQty', 'Price']

#Gateway Side
gateway_side_buy = DataSet.GatewaySide.Buy
gateway_side_sell = DataSet.GatewaySide.Sell

#Status
status_pending = DataSet.Status.Pending
status_new = DataSet.Status.New
status_reject = DataSet.Status.Reject

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '1015'

#connectivity
case_name = os.path.basename(__file__)
instrument = DataSet.Instrument.PAR
FromQuod = DataSet.DirectionEnum.FromQuod
ToQuod = DataSet.DirectionEnum.ToQuod
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value

def rules_creation():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    return [nos_rule]

def execute(report_id):
    try:
        rules_list = rules_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        # Send_MarkerData
        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)

        # Send_MarkerData
        fix_manager_fh.set_case_id(bca.create_event("Send Market Data", case_id))
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        fix_manager_fh.send_message(market_data_snap_shot)

        time.sleep(3)

        #region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)

        moc_order = FixMessageNewOrderSingleAlgo().set_MOC_params()
        moc_order.add_ClordId((os.path.basename(__file__)[:-3]))
        moc_order.change_parameters(dict(Account= client, OrderQty = qty))
        moc_order.update_fields_in_component('QuodFlatParameters', dict(WouldPriceOffset=would_price_offset))

        fix_manager.send_message_and_receive_response(moc_order, case_id_1)

        time.sleep(3)

        #region Check Sell side
        fix_verifier_ss.check_fix_message(moc_order, direction=ToQuod, message_name='Sell side NewOrderSingle')

        pending_moc_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(moc_order, gateway_side_sell, status_pending)
        pending_moc_order_params.change_parameter('TimeInForce', tif_atc)
        pending_moc_order_params.remove_parameter('TargetStrategy')
        fix_verifier_ss.check_fix_message(pending_moc_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport PendingNew')

        reject_moc_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(moc_order, gateway_side_sell, status_reject)
        reject_moc_order_params.change_parameters(dict(Text=text_reject_would_price_reference, TimeInForce=tif_atc))
        reject_moc_order_params.remove_parameter('TargetStrategy')
        fix_verifier_ss.check_fix_message(reject_moc_order_params, key_parameters=key_params_cl, message_name='Sell side ExecReport Reject')
        #endregion

    except:
        logging.error("Error execution", exc_info=True)
    finally:
        rule_manager = RuleManager()
        rule_manager.remove_rules(rules_list)
