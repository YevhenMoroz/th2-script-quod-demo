import logging
from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import convert_to_request, message_to_grpc
from quod_qa.eq import MD_test_3
from quod_qa.eq.Algo_Multilisted import QAP_1962
from quod_qa.eq.Sorping import QAP_2408,  QAP_2408_test
from rule_management import RuleManager
from schemas import rfq_tile_example
from stubs import Stubs
from quod_qa.fx import ui_tests
from quod_qa.eq.Care import QAP_1012
logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('Ziuban tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    try:
        # QAP_1012.execute(report_id)
        # QAP_2408.execute(report_id)
        QAP_2408_test.execute(report_id)
        # QAP_1962.execute(report_id)
        # MD_test_3.execute(report_id)
        # rule_manager = RuleManager()
        # rule_manager.remove_all_rules()
        # rule_manager.print_active_rules()

        # MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        #     symbol="734",
        #     connection_id=ConnectionID(session_alias="fix-fh-310-columbia")
        # )).MDRefID
        # mdir_params_bid = {
        #     'MDReqID': MDRefID,
        #     'NoMDEntries': [
        #         {
        #             'MDEntryType': '0',
        #             'MDEntryPx': '30',
        #             'MDEntrySize': '1000',
        #             'MDEntryPositionNo': '1'
        #         },
        #         {
        #             'MDEntryType': '1',
        #             'MDEntryPx': '40',
        #             'MDEntrySize': '1000',
        #             'MDEntryPositionNo': '1'
        #         }
        #     ]
        # }
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send MarketDataSnapshotFullRefresh',
        #     "fix-fh-310-columbia",
        #     report_id,
        #     message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, "fix-fh-310-columbia")
        # ))
        # MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        #     symbol="3416",
        #     connection_id=ConnectionID(session_alias="fix-fh-310-columbia")
        # )).MDRefID
        # mdir_params_bid = {
        #     'MDReqID': MDRefID,
        #     'NoMDEntries': [
        #         {
        #             'MDEntryType': '0',
        #             'MDEntryPx': '30',
        #             'MDEntrySize': '1000',
        #             'MDEntryPositionNo': '1'
        #         },
        #         {
        #             'MDEntryType': '1',
        #             'MDEntryPx': '40',
        #             'MDEntrySize': '1000',
        #             'MDEntryPositionNo': '1'
        #         }
        #     ]
        # }
        #
        # Stubs.fix_act.sendMessage(request=convert_to_request(
        #     'Send MarketDataSnapshotFullRefresh',
        #     "fix-fh-310-columbia",
        #     report_id,
        #     message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, "fix-fh-310-columbia")
        # ))


    except Exception:
        logging.error("Error execution",exc_info=True)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()

