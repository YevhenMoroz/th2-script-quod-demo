import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper_test.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
act = Stubs.fix_act
alias = "fix-fh-314-luna"
alias_gtw = "fix-sell-esp-t-314-stand"

def send_md(md_params, case_id):
    print(md_params)
    act.sendMessage(
        bca.convert_to_request(
            'Send Market Data SPOT',
            alias,
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', md_params, alias)
    ))

def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        simulator = Stubs.simulator
        # simulator = Stubs.test_sim



        mdu_params_spo = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="EUR/USD:SPO:REG:BARX",
                    connection_id=ConnectionID(session_alias=alias))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18066,
                    "MDEntrySize": 5000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18146,
                    "MDEntrySize": 5000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        send_md(mdu_params_spo, case_id)

        mdu_params_spo2 = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="EUR/USD:SPO:REG:CITI",
                    connection_id=ConnectionID(session_alias=alias))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18075,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18141,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
               ]
        }
        send_md(mdu_params_spo2, case_id)

        new_order_sor = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters({'OrderQty': '2000000'})
        FixManager(alias_gtw, case_id).Send_NewOrderSingle_FixMessage(fix_message=new_order_sor,
                                                                      message_name='New Order Single SOR')







    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        # md.send_md_unsubscribe()
        pass
