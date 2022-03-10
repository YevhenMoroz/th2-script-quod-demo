import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
instrument_gbp_nok = "GBP/NOK"
instrument_eur_usd = "EUR/USD"
instrument_usd_rub = "USD/RUB"
instrument_gbp_usd = "GBP/USD"
instrument_usd_cad = "USD/CAD"
instrument_usd_sgd = "USD/SGD"
instrument_usd = "USD"

sec_type_fw = "FXFWD"
sec_type_sp = "FXSPOT"

instr_type_fwd="FXF"
instr_type_spo="SPO"
instr_type_sn="SN"

tenor_spo="REG"
tenor_sn="FXN"
tenor_fwd="WK1"

venue_ms= "MS"
venue_hsbc= "HSBC"
venue_citi= "CITI"
venue_gs= "GS"

instrument = instrument_eur_usd
venue=venue_citi
sec_type=sec_type_sp
tenor=tenor_spo
instr_type=instr_type_spo
symbol = instrument+':'+instr_type+':'+tenor+':'+venue


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        simulator = Stubs.simulator
        # simulator = Stubs.test_sim
        act = Stubs.fix_act
        # alias = "fix-fh-q-314-luna"
        alias = "fix-fh-314-luna"

        mdu_params_spo = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol=symbol,
                    connection_id=ConnectionID(session_alias=alias))).MDRefID,
            'Instrument': {
                'Symbol': instrument,
                'SecurityType': sec_type
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18599,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18810,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                # {
                #     "MDEntryType": "0",
                #     "MDEntryPx": 1.18397,
                #     "MDEntrySize": 5000000,
                #     "MDEntryPositionNo": 2,
                #     "MDQuoteType": 1,
                #     'SettlDate': tsd.spo(),
                #     "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                # },
                # {
                #     "MDEntryType": "1",
                #     "MDEntryPx": 1.18909,
                #     "MDEntrySize": 5000000,
                #     "MDEntryPositionNo": 2,
                #     "MDQuoteType": 1,
                #     'SettlDate': tsd.spo(),
                #     "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                # },
                # {
                #     "MDEntryType": "0",
                #     "MDEntryPx": 1.18251,
                #     "MDEntrySize": 12000000,
                #     "MDEntryPositionNo": 3,
                #     "MDQuoteType": 1,
                #     'SettlDate': tsd.spo(),
                #     "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                # },
                # {
                #     "MDEntryType": "1",
                #     "MDEntryPx": 1.18999,
                #     "MDEntrySize": 12000000,
                #     "MDEntryPositionNo": 3,
                #     "MDQuoteType": 1,
                #     'SettlDate': tsd.spo(),
                #     "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                # }
            ]
        }
        print(mdu_params_spo)
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                alias,
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, alias)
            ))

        # mdu_params_spo1 = {
        #     "MDReqID": simulator.getMDRefIDForConnection314(
        #         request=RequestMDRefID(
        #             symbol="EUR/USD:SPO:REG:HSBC",
        #             connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
        #     'Instrument': {
        #         'Symbol': 'EUR/USD',
        #         'SecurityType': 'FXSPOT'
        #     },
        #     "NoMDEntries": [
        #         {
        #             "MDEntryType": "0",
        #             "MDEntryPx": 1.19640,
        #             "MDEntrySize": 1000000,
        #             "MDEntryPositionNo": 1,
        #             'SettlDate': tsd.spo(),
        #             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        #         },
        #         {
        #             "MDEntryType": "1",
        #             "MDEntryPx": 1.19222,
        #             "MDEntrySize": 1000000,
        #             "MDEntryPositionNo": 1,
        #             'SettlDate': tsd.spo(),
        #             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        #         },
        #     ]
        # }
        #
        # act.sendMessage(
        #     bca.convert_to_request(
        #         'Send Market Data SPOT',
        #         'fix-fh-314-luna',
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo1, 'fix-fh-314-luna')
        #     ))

        # mdu_params_spo = {
        #     "MDReqID": simulator.getMDRefIDForConnection314(
        #         request=RequestMDRefID(
        #             symbol="EUR/USD:SPO:REG:BARX",
        #             connection_id=ConnectionID(session_alias=alias))).MDRefID,
        #     'Instrument': {
        #         'Symbol': 'EUR/USD',
        #         'SecurityType': 'FXSPOT'
        #     },
        #     "NoMDEntries": [
        #         {
        #             "MDEntryType": "0",
        #             "MDEntryPx": 1.18066,
        #             "MDEntrySize": 5000000,
        #             "MDEntryPositionNo": 1,
        #             "MDQuoteType": 1,
        #             'SettlDate': tsd.spo(),
        #             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        #         },
        #         {
        #             "MDEntryType": "1",
        #             "MDEntryPx": 1.18146,
        #             "MDEntrySize": 5000000,
        #             "MDEntryPositionNo": 1,
        #             "MDQuoteType": 1,
        #             'SettlDate': tsd.spo(),
        #             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        #         },
        #     ]
        # }
        # act.sendMessage(
        #     bca.convert_to_request(
        #         'Send Market Data SPOT',
        #         alias,
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, alias)
        #     ))
        #
        # mdu_params_spo2 = {
        #     "MDReqID": simulator.getMDRefIDForConnection314(
        #         request=RequestMDRefID(
        #             symbol="EUR/USD:SPO:REG:CITI",
        #             connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
        #     'Instrument': {
        #         'Symbol': 'EUR/USD',
        #         'SecurityType': 'FXSPOT'
        #     },
        #     "NoMDEntries": [
        #         {
        #             "MDEntryType": "0",
        #             "MDEntryPx": 1.18075,
        #             "MDEntrySize": 1000000,
        #             "MDEntryPositionNo": 1,
        #             'SettlDate': tsd.spo(),
        #             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        #         },
        #         {
        #             "MDEntryType": "1",
        #             "MDEntryPx": 1.18141,
        #             "MDEntrySize": 1000000,
        #             "MDEntryPositionNo": 1,
        #             'SettlDate': tsd.spo(),
        #             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        #         },
        #     ]
        # }
        # act.sendMessage(
        #     bca.convert_to_request(
        #         'Send Market Data SPOT',
        #         'fix-fh-314-luna',
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo2, 'fix-fh-314-luna')
        #     ))


        # id = simulator.getMDRefIDForConnection314(
        #         request=RequestMDRefID(
        #             symbol="EUR/USD:SPO:REG:DB",
        #             connection_id=ConnectionID(session_alias="fix-fh-q-314-luna"))).MDRefID
        # mdu_params_spo2 = {
        #     "MDReqID": simulator.getMDRefIDForConnection314(
        #         request=RequestMDRefID(
        #             symbol="EUR/USD:SPO:REG:DB",
        #             connection_id=ConnectionID(session_alias="fix-fh-q-314-luna"))).MDRefID,
        #     'Instrument': {
        #         'Symbol': 'EUR/USD',
        #         'SecurityType': 'FXSPOT'
        #     },
        #     "NoMDEntries": [
        #         {
        #             "MDEntryType": "0",
        #             "MDEntryPx": 1.16079,
        #             "MDEntrySize": 5000000,
        #             "MDEntryPositionNo": 1,
        #             "MDQuoteType": 1,
        #             'SettlDate': tsd.spo(),
        #             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        #         },
        #         {
        #             "MDEntryType": "1",
        #             "MDEntryPx": 1.16140,
        #             "MDEntrySize": 5000000,
        #             "MDEntryPositionNo": 1,
        #             "MDQuoteType": 1,
        #             'SettlDate': tsd.spo(),
        #             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
        #         },
        #     ]
        # }
        # simulator.updateStorage(mdu_params_spo3)
        # print(bca.convert_to_request(
        #         'Send Market Data SPOT',
        #         'fix-fh-q-314-luna',
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo2, 'fix-fh-q-314-luna')
        #     ))
        # act.sendMessage(
        #     bca.convert_to_request(
        #         'Send Market Data SPOT',
        #         'fix-fh-q-314-luna',
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo2, 'fix-fh-q-314-luna')
        #     ))


        # id = simulator.getMDRefIDForConnection314(
        #         request=RequestMDRefID(
        #             symbol=symbol,
        #             connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID



        mdu_params_FWD = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol=symbol,
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': instrument,
                'SecurityType': sec_type
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18039,
                    "MDEntrySize": 1000000,
                    "MDEntrySpotRate": 1.18038,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.wk1(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18051,
                    "MDEntrySize": 1000000,
                    "MDEntrySpotRate": 1.18052,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.wk1(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        # print(mdu_params_FWD)
        # act.sendMessage(
        #     bca.convert_to_request(
        #         'Send Market Data SPOT',
        #         'fix-fh-314-luna',
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_FWD, 'fix-fh-314-luna')
        #     ))






    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        # md.send_md_unsubscribe()
        pass
