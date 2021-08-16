import logging
from datetime import datetime

from th2_grpc_sim_quod.sim_pb2 import NoMDEntries

from custom import basic_custom_actions as bca
from examples import example_java_api
from quod_qa.eq.Algo_PercentageVolume import QAP_1324
from quod_qa.eq.Test import read_log_example
from rule_management import RuleManager
from stubs import Stubs
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, close_fe, get_opened_fe, \
    prepare_fe_2

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('Ziuban tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    # session_id = set_session_id()
    try:
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)

        # example_java_api.TestCase(report_id).execute()
        # QAP_1324.execute(report_id, session_id)


        read_log_example.execute(report_id)


        # rm = RuleManager()
        # nos_ioc_md_rule = rm.add_NewOrdSingle_IOC_MarketData(
        #     "fix-buy-side-316-ganymede",
        #     "XPAR_CLIENT1",
        #     "XPAR",
        #     20,
        #     100,
        #     True,
        #     "fix-feed-handler-316-ganymede",
        #     "756",
        #     20,
        #     350,
        #         [NoMDEntries(MDEntryType="0", MDEntryPx="0", MDEntrySize="0", MDEntryPositionNo="1"),NoMDEntries(MDEntryType="1", MDEntryPx="20", MDEntrySize="500", MDEntryPositionNo="1")],
        #         [NoMDEntries(MDUpdateAction='0', MDEntryType='2', MDEntryPx='40', MDEntrySize='1000', MDEntryDate=datetime.utcnow().date().strftime("%Y%m%d"),
        #                  MDEntryTime=datetime.utcnow().time().strftime("%H:%M:%S"))])
        # rm.print_active_rules()
        # rm.remove_rule_by_id(10)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        pass
        # Stubs.win_act.unregister(session_id)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()