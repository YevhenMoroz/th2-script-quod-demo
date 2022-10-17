import os
import logging
import time
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers import DataSet
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from datetime import datetime
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

#order param
qty = 1000
qty_bid = 123
qty_ask = 543
price = 1
price_bid = 1
price_ask = 50
price_nav = 700
side = 1
tif_day = 0
order_type = 2
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
status_fill = DataSet.Status.Fill

#venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '555'

#connectivity
case_name = os.path.basename(__file__)
instrument = DataSet.Instrument.BUI.value
FromQuod = DataSet.DirectionEnum.FromQuod
ToQuod = DataSet.DirectionEnum.ToQuod
connectivity_buy_side = DataSet.Connectivity.Ganymede_316_Buy_Side.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Redburn.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value

def rules_creation():
    rule_manager = RuleManager(Simulators.algo)
    nos_pov = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side, account, ex_destination_1, price)
    ocrr = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(connectivity_buy_side, False)
    ocr_rule = rule_manager.add_OrderCancelRequest(connectivity_buy_side, account, ex_destination_1, True)

    return [ocrr, nos_pov, ocr_rule]

def execute(report_id):
    try:
        rules_list = rules_creation()
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
        
        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)

        # Send_MarkerData
        # if faced an issue with MDReqID (MDReqID doesn't change in FXFH_TH2 logs) in method update_MDReqID change md_req_id for the static MDReqID from the FXFH_TH2 logs
        market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=price_bid, MDEntrySize=123)
        market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=50000, TradingSessionSubID=3, SecurityTradingStatus=3)
        fix_manager_fh.send_message(market_data_snap_shot)

        time.sleep(3)

        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Algo Order", case_id)
        fix_verifier_ss.set_case_id(case_id_1)

        # Before set order params, check that, for example, set_POV_params() doesn't refer to the data set (will be change when this script will use a class instead of method execute)
        pov_order = FixMessageNewOrderSingleAlgo().set_POV_params()
        pov_order.add_ClordId((os.path.basename(__file__)[:-3]))
        pov_order.change_parameters(dict(Account=client, OrderQty=qty, Side=side, Price=price, Instrument=instrument))
        pov_order.update_fields_in_component('QuodFlatParameters', dict(ParticipateInOpeningAuctions='Y'))
        fix_manager.send_message_and_receive_response(pov_order, case_id_1)
        # endregion

        time.sleep(1)

        market_data_snap_shot_2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        market_data_snap_shot_2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=price_bid, MDEntrySize=543)
        market_data_snap_shot_2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=50000, TradingSessionSubID=3, SecurityTradingStatus=3)
        fix_manager_fh.send_message(market_data_snap_shot_2)

        # add time delay to change trading phase
        time.sleep(10)

        # Commend MDReqID if faced an issue with MDReqID (MDReqID doesn't change in FXFH_TH2 logs)
        MDRefID_1 = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol="555",
            connection_id=ConnectionID(session_alias="fix-feed-handler-316-ganymede")
        )).MDRefID

        # Set message to change Trading Phase
        mdir_params_trade = {
            'MDReqID': MDRefID_1,     #MDRefID_1 - add, if the MDReqID issues is gone
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '20',
                    'MDEntrySize': '100',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    'TradingSessionSubID': '2',
                    'SecurityTradingStatus': '3'
                }
            ]
        }

        # Send New Trading Phase
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', "fix-feed-handler-316-ganymede", report_id,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, "fix-feed-handler-316-ganymede")
        ))

    except:
        logging.error("Error execution", exc_info=True)
    finally:
        RuleManager.remove_rules(rules_list)