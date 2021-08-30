import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from examples import example_java_api
from quod_qa.eq.Algo_PercentageVolume import QAP_1324
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
    report_id = bca.create_event(' tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")
    session_id = set_session_id()
    try:
        if not Stubs.frontend_is_open:
            prepare_fe(report_id, session_id, work_dir, username, password)
        else:
            get_opened_fe(report_id, session_id, work_dir)

        # example_java_api.TestCase(report_id).execute()
        QAP_1324.execute(report_id, session_id)


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)

if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()