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
from datetime import datetime, time, timezone
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM

from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager

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
# ex_destination_1 = "XPAR"
# account = 'XPAR_CLIENT2'
ex_destination_1 = "XAMS"
account = 'XAMS_CLIENT2'
# ex_destination_1 = "TRQX"
# account = 'TRQX_CLIENT2'
client = "CLIENT2"
currency = 'EUR'
# s_par = '1015'
s_ams = '48'
# s_ams = '555'
# s_par = '555'
# s_par = '734'
# s_trqx = '3416'

#connectivity
case_name = os.path.basename(__file__)
instrument = DataSet.Instrument.AMS.value
# instrument = DataSet.Instrument.RF.value
FromQuod = DataSet.DirectionEnum.FromQuod
ToQuod = DataSet.DirectionEnum.ToQuod
# connectivity_buy_side_rb = DataSet.Connectivity.Columbia_310_Buy_Side.value
# connectivity_sell_side = DataSet.Connectivity.Columbia_310_Sell_Side.value
# connectivity_fh = DataSet.Connectivity.Columbia_310_Feed_Handler.value
connectivity_buy_side_rb = DataSet.Connectivity.Ganymede_316_Buy_Side_Redburn.value
connectivity_sell_side = DataSet.Connectivity.Ganymede_316_Sell_Side.value
connectivity_fh = DataSet.Connectivity.Ganymede_316_Feed_Handler.value

def send_market_data(symbol: str, case_id :str, market_data):
    MDRefID = Stubs.simulator_algo.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntries': market_data,
        #"Instrument": instr
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', md_params, connectivity_fh)
    ))

def rules_creation():
    rule_manager = RuleManager(Simulators.algo)
    # ioc_nos = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side_rb, account, ex_destination_1, False, 10000, 130)
    # nos_trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(connectivity_buy_side_rb, account, ex_destination_1, 30, 30, 41667, 41667, 0)
    # nos_mkt = rule_manager.add_NewOrdSingle_MarketAuction(connectivity_buy_side_rb, account, ex_destination_1)
    # nos = rule_manager.add_OrderCancelReplaceRequest(connectivity_buy_side_rb, account, ex_destination_1, True, 5)
    # nos_pov1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 134)
    # md_rule = rule_manager.add_MarketDataRequestWithTimeout("fix-feed-handler-316-ganymede", [])
    nos_ioc_alla = rule_manager.add_NewOrdSingleExecutionReportAll(connectivity_buy_side_rb, account, ex_destination_1)
    # nos_ioc_all = rule_manager.add_NewOrdSingleExecutionReportTradeOnFullQty(connectivity_buy_side_rb, account, ex_destination_1)
    ocrr = rule_manager.add_OCRR(connectivity_buy_side_rb)
    ocr_rule = rule_manager.add_OCR(connectivity_buy_side_rb)
    return [nos_ioc_alla, ocrr, ocr_rule]

# def rules_creation():
#     rule_manager = RuleManager(Simulators.algo)
#     nos_pov = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, price)
#     nos_pov1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 30)
#     nos_pov2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 130)
#     nos_pov3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 29.995)
#     nos_pov4 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 120)
#     nos_pov5 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 100)
#     nos_pov6 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 131)
#     nos_pov7 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 132)
#     nos_pov8 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 133)
#     nos_pov9 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 134)
#     nos_pov10 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 135)
#     nos_pov11 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 29.99)
#     nos_pov12 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 35)
#     # nos_pov1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 120)
#     # nos_pov2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 119.7)
#     # nos_pov3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 119.4)
#     # nos_pov4 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 119.1)
#     # nos_pov5 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 118.8)
#     # nos_pov6 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 118.5)
#     # nos_pov7 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 118.2)
#     # nos_pov8 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 117.9)
#     # nos_pov9 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 117.6)
#     # nos_pov10 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 117.3)
#     # nos_pov11 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(connectivity_buy_side_rb, account, ex_destination_1, 117)
#     ocrr = rule_manager.add_OCRR(connectivity_buy_side_rb)
#     ocr_rule = rule_manager.add_OCR(connectivity_buy_side_rb)
#     ioc_nos = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side_rb, account, ex_destination_1, False, 0, 135)
#     ioc_nos1 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side_rb, account, ex_destination_1, False, 0, 130)
#     ioc_nos2 = rule_manager.add_NewOrdSingle_IOC(connectivity_buy_side_rb, account, ex_destination_1, False, 0, 40)
#     # nos_trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQtyRBCustom(connectivity_buy_side_rb, account, ex_destination_1, 130, 130, 100, 50, 0)
#     # nos_mkt = rule_manager.add_NewOrdSingle_MarketAuction(connectivity_buy_side_rb, account, ex_destination_1)
#     return [nos_pov1, nos_pov2, nos_pov3, nos_pov4, nos_pov5, nos_pov6, nos_pov7, nos_pov8, nos_pov9, nos_pov10, nos_pov11, nos_pov12, ocrr, ocr_rule, ioc_nos, ioc_nos1, ioc_nos2]

def execute(report_id):
    try:
        print('R_R')
        # rules_list = rules_creation()
        print('R^R')
        case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)

        fix_verifier_ss = FixVerifier(connectivity_sell_side, case_id)
        fix_manager = FixManager(connectivity_sell_side, case_id)
        fix_manager_fh = FixManager(connectivity_fh, case_id)
        case_id_0 = bca.create_event("Send Market Data", case_id)

        # region Snapshot Fullrefresh

        market_data1 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '1155',
                'MDEntryPositionNo': '1',
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '40',
                'MDEntrySize': '1000000',
                'MDEntryPositionNo': '1',
            }
        ]
        instrm = {
                'Symbol': 'FR0000121121_EUR',
                'SecurityID': 'FR0000121121',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR',
                'SecurityType': 'CS',
                'SecurityDesc': 'EURAZEO',
                'SecurityStatus': '2'
        }
        # send_market_data(s_ams, case_id_0, market_data1)
        # send_market_data(s_trqx, case_id_0, market_data1)
        market_data2 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '134',
                'MDEntrySize': '15000',
                'MDEntryPositionNo': '1',
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '135',
                'MDEntrySize': '20000',
                'MDEntryPositionNo': '1',
            }
        ]
        instrm1 = {
                'Symbol': 'FR0000121121_EUR',
                'SecurityID': 'FR0000121121',
                'SecurityIDSource': '4',
                'SecurityExchange': 'XPAR',
                'SecurityType': 'CS',
                'SecurityDesc': 'EURAZEO',
                'SecurityStatus': '1'
        }
        #send_market_data(s_trqx, case_id_0, market_data2)
        market_data2 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '0',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '2'
            },
            {
                'MDEntryType': '0',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '3'
            },
            # {
            #     'MDEntryType': '0',
            #     'MDEntryPx': '30',
            #     'MDEntrySize': '450000',
            #     'MDEntryPositionNo': '1'
            # },
            # {
            #     'MDEntryType': '0',
            #     'MDEntryPx': '29.995',
            #     'MDEntrySize': '8000',
            #     'MDEntryPositionNo': '1'
            # },
        ]
        # send_market_data(s_ams, case_id_0, market_data2)
        # send_market_data(s_trqx, case_id_0, market_data2)

        # region MD
        market_data3 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '134',
                'MDEntrySize': '10000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '0',
                'MDEntryPx': '135',
                'MDEntrySize': '10000',
                'MDEntryPositionNo': '2'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '140',
                'MDEntrySize': '50000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '140',
                'MDEntrySize': '50000',
                'MDEntryPositionNo': '2'
            },
        ]
        # send_market_data(s_ams, case_id_0, market_data3)

        market_data4 = [
            {
                'MDEntryType': '0',
                'MDEntryPx': '103.6',
                'MDEntrySize': '6000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '0',
                'MDEntryPx': '103',
                'MDEntrySize': '6500',
                'MDEntryPositionNo': '2'
            },
            {
                'MDEntryType': '0',
                'MDEntryPx': '102.9',
                'MDEntrySize': '5000',
                'MDEntryPositionNo': '3'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '130',
                'MDEntrySize': '50000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '130',
                'MDEntrySize': '50000',
                'MDEntryPositionNo': '2'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '130',
                'MDEntrySize': '50000',
                'MDEntryPositionNo': '3'
            },
        ]
        # send_market_data(s_trqx, case_id_0, market_data4)

        # endregion

        print('?_?')
        # Commend MDReqID if faced an issue with MDReqID (MDReqID doesn't change in FXFH_TH2 logs)
        MDRefID_1 = Stubs.simulator_algo.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=s_ams,
            # symbol=s_par,
            # symbol=s_trqx,
            connection_id=ConnectionID(session_alias=connectivity_fh)
        )).MDRefID

        # Set message to change Trading Phase
        mdir_params_trade = {
            'MDReqID': MDRefID_1,     #MDRefID_1 - add, if the MDReqID issues is gone
            'NoMDEntriesIR': [
                {
                    'MDUpdateAction': '0',
                    'MDEntryType': '2',
                    'MDEntryPx': '0',
                    'MDEntrySize': '0',
                    'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
                    'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
                    # 'MDEntryDate': '20230122',
                    'TradingSessionSubID': '3',
                    'SecurityTradingStatus': '3',
                    # 'LastTradingSessionSubID': '3'
                    # 'MDOriginType': '0',
                }
            ],
        }
        #
        # Send New Trading Phase
        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send MarketDataIncrementalRefresh', connectivity_fh, report_id,
            message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade, connectivity_fh)
        ))

        # region phases

        phases = [
            {
                "beginTime":  datetime.now().replace(hour=6, minute=50, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=7, minute=0, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "POP",
                "standardTradingPhase": "PRE",
            },
            {
                "beginTime":  datetime.now().replace(hour=7, minute=0, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=7, minute=10, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "OPN",
                "standardTradingPhase": "OPN",
            },
            {
                "beginTime":  datetime.now().replace(hour=7, minute=10, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=10, minute=5, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "PCL",
                "standardTradingPhase": "PCL",
            },
            {
                "beginTime":  datetime.now().replace(hour=10, minute=5, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=20, minute=10, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "TAL",
                "standardTradingPhase": "TAL",
            },
            {
                "beginTime":  datetime.now().replace(hour=20, minute=10, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=22, minute=0, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "CLO",
                "standardTradingPhase": "CLO",
            }
        ]
        # rest_api_algo_manager = RestApiAlgoManager(session_alias="rest_wa316ganymede")
        # rest_api_algo_manager.modify_trading_phase_profile("PreClose Auction Phase (QA)", phases)
        # rest_api_algo_manager.modify_trading_phase_profile("Auction Phase QA2", phases)

        # default phases
        phases = [
            {
                "beginTime":  datetime.now().replace(hour=6, minute=50, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=7, minute=0, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "POP",
                "standardTradingPhase": "PRE",
            },
            {
                "beginTime":  datetime.now().replace(hour=7, minute=0, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=22, minute=0, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "OPN",
                "standardTradingPhase": "OPN",
            },
            {
                "beginTime":  datetime.now().replace(hour=22, minute=0, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=22, minute=5, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "PCL",
                "standardTradingPhase": "PCL",
            },
            {
                "beginTime":  datetime.now().replace(hour=22, minute=5, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=22, minute=10, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "TAL",
                "standardTradingPhase": "TAL",
            },
            {
                "beginTime":  datetime.now().replace(hour=22, minute=10, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=23, minute=0, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "CLO",
                "standardTradingPhase": "CLO",
            },
            {
                "beginTime":  datetime.now().replace(hour=23, minute=0, second=0, tzinfo=timezone.utc),
                "endTime":  datetime.now().replace(hour=23, minute=5, second=0, tzinfo=timezone.utc),
                "submitAllowed": "True",
                "tradingPhase": "EXA",
                "standardTradingPhase": "EXA",
                "expiryCycle": "EVM",
            }
        ]
        # rest_api_algo_manager = RestApiAlgoManager(session_alias="rest_wa316ganymede")
        # rest_api_algo_manager.modify_trading_phase_profile("Auction Phase QA2", phases)
        # rest_api_algo_manager.modify_trading_phase_profile("PreClose Auction Phase (QA)", phases)

        # endregion

        # region Incremental refresh 2

        # Set message to change Trading Phase
        # MDRefID_1 = Stubs.simulator_algo.getMDRefIDForConnection(request=RequestMDRefID(
        #     symbol=s_par,
        #     connection_id=ConnectionID(session_alias=connectivity_fh)
        # )).MDRefID

        # tss = {
        #     #'MDReqID': MDRefID_1,
        #     'TradingSessionID': '1',
        #     'TradSesStatus': '2',
        #     'TradingSessionSubID': '3',
        #     #'SecurityTradingStatus': '3',
        #     # 'MarketID': 'PAR',
        #     #'Instrument': instrument,
        # }
        # #
        # # # Send New Trading Phase
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send TradingSessionStatus', connectivity_fh, report_id,
        #     message_to_grpc('TradingSessionStatus', tss, connectivity_fh)
        # ))

        # MDRefID_2 = Stubs.simulator_algo.getMDRefIDForConnection(request=RequestMDRefID(
        #     symbol=s_trqx,
        #     connection_id=ConnectionID(session_alias=connectivity_fh)
        # )).MDRefID
        #
        # # Set message to change Trading Phase
        # mdir_params_trade2 = {
        #     'MDReqID': MDRefID_2,     #MDRefID_1 - add, if the MDReqID issues is gone
        #     'NoMDEntriesIR': [
        #         {
        #             'MDUpdateAction': '0',
        #             'MDEntryType': '2',
        #             'MDEntryPx': '133',
        #             'MDEntrySize': '10000',
        #             'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
        #             'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
        #             'TradingSessionSubID': '3',
        #             'SecurityTradingStatus': '3',
        #         }
        #     ]
        # }
        #
        # # Send New Trading Phase
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send MarketDataIncrementalRefresh', connectivity_fh, report_id,
        #     message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade2, connectivity_fh)
        # ))

        # md_params = {
        #     'MDReqID': '3416_5',
        #     'SubscriptionRequestType': '1',
        #     'MarketDepth': '0',
        #     'MDUpdateType': '1',
        #     'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
        #     'NoRelatedSymbols': [
        #         {
        #             'Instrument': instrument,
        #         }
        #     ]
        # }
        #
        # def send_md_unsubscribe(md_params):
        #     # Change MarketDataRequest from 'Subscribe' to 'Unsubscribe'
        #     md_params['SubscriptionRequestType'] = '2'
        #     # Send MarketDataRequest via FIX
        #     Stubs.fix_act.sendMessage(
        #         bca.convert_to_request(
        #             'Send MDR (unsubscribe)',
        #             connectivity_fh,
        #             case_id,
        #             bca.message_to_grpc('MarketDataRequest', md_params, connectivity_fh)
        #         ))
        #
        # send_md_unsubscribe(md_params)

        # MDRefID_1 = Stubs.simulator_algo.getMDRefIDForConnection(request=RequestMDRefID(
        #     symbol=s_par,
        #     connection_id=ConnectionID(session_alias=connectivity_fh)
        # )).MDRefID

        #time.sleep(7)

        # Set message to change Trading Phase
        # mdir_params_trade2 = {
        #     'MDReqID': MDRefID_1,     #MDRefID_1 - add, if the MDReqID issues is gone
        #     'NoMDEntriesIR': [
        #         {
        #             'MDUpdateAction': '0',
        #             'MDEntryType': '2',
        #             'MDEntryPx': '50',
        #             'MDEntrySize': '10000',
        #             'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
        #             'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
        #             'TradingSessionSubID': '3',
        #             'SecurityTradingStatus': '3',
        #         }
        #     ]
        # }
        #
        # # Send New Trading Phase
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send MarketDataIncrementalRefresh', connectivity_fh, report_id,
        #     message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade2, connectivity_fh)
        # ))

        # endregion

        print('^_^')

        # region Execution reports

        cl_ord_id_pending_new = "MO1230210113840513001"
        price_pending_new = "29.995"
        tif_pending_new = "0"

        # Execution report Pending New
        exec_report_pending = {
            "Account": account,
            "ClOrdID": cl_ord_id_pending_new,     #need change for each order
            "ExecID": "1234156",
            "OrderID": "1234156",
            "OrdStatus": "A",
            "OrdType": "2",
            "Price": price_pending_new,                           #need change for each order
            "Currency": "EUR",
            "TimeInForce": tif_pending_new,                     #need change for each order
            "LastPx": "0",
            "LastQty": "0",
            "ExecType": "A",
            "LeavesQty": "0",                       #equals the qty of the parent order (child)
            "TransactTime": datetime.utcnow().isoformat(),
            "Side": "1",
            "Instrument": instrument,               #???
            "CumQty": "0"
        }

        # Execution report  New
        exec_report_new = {
            "Account": account,
            "ClOrdID": cl_ord_id_pending_new,     #need change for each order
            "ExecID": "1234156",
            "OrderID": "1234156",
            "OrdStatus": "0",
            "OrdType": "2",
            "Price": price_pending_new,                           #need change for each order
            "Currency": "EUR",
            "TimeInForce": tif_pending_new,                     #need change for each order
            "LastPx": "0",
            "LastQty": "0",
            "ExecType": "0",
            "LeavesQty": "0",                       #equals the qty of the parent order (child)
            "TransactTime": datetime.utcnow().isoformat(),
            "Side": "1",
            "Instrument": instrument,               #???
            "CumQty": "0"
        }

        # Send Exec Report Pending
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send ExecutionReport', connectivity_buy_side_rb, report_id,
        #     message_to_grpc('ExecutionReport', exec_report_pending, connectivity_buy_side_rb)
        # ))
        #
        # # Send Exec Report New
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send ExecutionReport', connectivity_buy_side_rb, report_id,
        #     message_to_grpc('ExecutionReport', exec_report_new, connectivity_buy_side_rb)
        # ))

        #time.sleep(5)
        cum_qty_partial = "1000"
        ord_qty_partial = "2527"
        leaves_qty_partial = int(int(ord_qty_partial) - int(cum_qty_partial))
        price_partial = price_pending_new
        avg_partial = price_partial
        # Execution report Partial Fill
        exec_report_partial = {
            "Account": account,
            "AvgPx": avg_partial,
            "ClOrdID": cl_ord_id_pending_new,
            "CumQty": cum_qty_partial,
            "Currency": "EUR",
            "ExecID": "1234156",
            "LastPx": price_partial,
            "LastQty": cum_qty_partial,
            "OrderID": "1234156",
            "OrderQty": ord_qty_partial,
            "OrdStatus": "1",
            "OrdType": "2",
            "Price": price_partial,
            "Instrument": instrument,   #???
            "Side": "1",
            "Text": "Partial Fill",
            "TimeInForce": tif_pending_new,
            "TransactTime": datetime.utcnow().isoformat(),
            "ExDestination": "XPAR",
            "ExecType": "F",
            "LeavesQty": leaves_qty_partial,
            "OrderCapacity": "A",
        }

        # Send Exec Report Partial Fill
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send ExecutionReport', connectivity_buy_side_rb, report_id,
        #     message_to_grpc('ExecutionReport', exec_report_partial, connectivity_buy_side_rb)
        # ))

        ord_qty_cancel = ord_qty_partial
        cum_qty_cancel = cum_qty_partial
        leaves_qty_cancel = leaves_qty_partial
        avg_cancel = avg_partial

        exec_report_cancel = {
            "ClOrdID": cl_ord_id_pending_new,
            "OrderQty": ord_qty_cancel,
            "CumQty": cum_qty_cancel,
            "ExecID": "1234156",
            "OrderID": "1234156",
            "OrdStatus": "4",
            "AvgPx": avg_cancel,
            "Text": "Cancel",
            "Side": "1",
            "ExecType": "4",
            "Instrument": instrument,
            "LeavesQty": leaves_qty_cancel,
            "TransactTime": datetime.utcnow().isoformat(),
            "OrigClOrdID": cl_ord_id_pending_new
        }

        # # Send Exec Report Cancel
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send ExecutionReport', connectivity_buy_side_rb, report_id,
        #     message_to_grpc('ExecutionReport', exec_report_cancel, connectivity_buy_side_rb)
        # ))

        # endregion

        # mdir_params_trade1 = {
        #     'MDReqID': MDRefID_1,     #MDRefID_1 - add, if the MDReqID issues is gone
        #     'NoMDEntriesIR': [
        #         {
        #             'MDUpdateAction': '0',
        #             'MDEntryType': '2',
        #             'MDEntryPx': '50',
        #             'MDEntrySize': '200000',
        #             'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
        #             'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S"),
        #             'TradingSessionSubID': '3',
        #             'SecurityTradingStatus': '3',
        #             'LastTradingSessionSubID': '3'
        #         }
        #     ]
        # }
        #
        # Send New Trading Phase
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send MarketDataIncrementalRefresh', connectivity_fh, report_id,
        #     message_to_grpc('MarketDataIncrementalRefresh', mdir_params_trade1, connectivity_fh)
        # ))
        # send_market_data(s_par, case_id_0, market_data2)
        # send_market_data(s_trqx, case_id_0, market_data3)

        # market_data_snap_shot = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        # market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=1, MDEntrySize=5555)
        # market_data_snap_shot.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=50000, TradingSessionSubID=3, SecurityTradingStatus=3)
        # fix_manager_fh.send_message(market_data_snap_shot)
        #
        # market_data_snap_shot2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_trqx, connectivity_fh)
        # market_data_snap_shot2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=1, MDEntrySize=5555)
        # market_data_snap_shot2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=50000, TradingSessionSubID=3, SecurityTradingStatus=3)
        # fix_manager_fh.send_message(market_data_snap_shot2)

        # market_data_snap_shot2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(s_par, connectivity_fh)
        # market_data_snap_shot2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=1, MDEntrySize=300)
        # market_data_snap_shot2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=price_ask, MDEntrySize=50000, TradingSessionSubID=3, SecurityTradingStatus=3)
        # fix_manager_fh.send_message(market_data_snap_shot2)

    except:
        logging.error("Error execution", exc_info=True)
    # finally:
    #     rule_manager = RuleManager()
    #     rule_manager.remove_rules(rules_list)