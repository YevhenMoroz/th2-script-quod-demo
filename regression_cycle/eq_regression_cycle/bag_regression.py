from custom.basic_custom_actions import timestamps
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

from test_cases.eq.Bag.QAP_1082 import QAP_1082
from test_cases.eq.Bag.QAP_1083 import QAP_1083
from test_cases.eq.Bag.QAP_1084 import QAP_1084
from test_cases.eq.Bag.QAP_1085 import QAP_1085
from test_cases.eq.Bag.QAP_1086 import QAP_1086
from test_framework.configurations.component_configuration import ComponentConfiguration
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Bag ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    session_id = set_session_id()
    seconds, nanos = timestamps()  # Store case start time
    configuration = ComponentConfiguration("Bag")
    data_set = configuration.data_set
    try:
        QAP_1082(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_1083(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_1084(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_1085(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
        QAP_1086(report_id=report_id, session_id=session_id, data_set=data_set, environment=configuration.environment) \
            .execute()
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Bag regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
