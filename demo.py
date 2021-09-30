import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from quod_qa.eq.Care import QAP_1045
from stubs import Stubs
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('Yehor tests ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'))
    logger.info(f"Root event was created (id = {report_id.id})")

    session_id = set_session_id()

    try:
        # example_java_api.TestCase(report_id).execute()

        QAP_3361.execute(report_id, session_id)
        # rm = RuleManager()
        # rm.print_active_rules()
        # rm.remove_rules_by_id_list([2078, 2079, 2729, 2733])
        # rm.print_active_rules()

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    try:
        logging.basicConfig()
        test_run()
    finally:
        Stubs.factory.close()
