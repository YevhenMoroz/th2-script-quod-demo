from custom.basic_custom_actions import timestamps
from test_cases.eq.PostTrade import QAP_T7552, QAP_T7551, QAP_T7548, QAP_T7547, QAP_T7503, QAP_T7501, QAP_T7500, QAP_T7498, \
    QAP_T7443, QAP_T7506, QAP_T7499, QAP_T7438, QAP_T7544, QAP_T7538, QAP_T7537, QAP_T7535, QAP_T7533, QAP_T7532, QAP_T7531, \
    QAP_T7530, QAP_T7518, QAP_T7510, QAP_T7507, QAP_T7505, QAP_T7504, QAP_T7495, QAP_T7485, QAP_T7480, QAP_T7476, \
    QAP_3936, QAP_T7383, QAP_T7363, QAP_T7360
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from datetime import datetime

from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('post trade regression', parent_id)
    session_id = set_session_id()
    seconds, nanos = timestamps()  # Store case start time
    try:
        QAP_T7552.execute(report_id, session_id)
        QAP_T7551.execute(report_id, session_id)
        QAP_T7548.execute(report_id, session_id)
        QAP_T7547.execute(report_id, session_id)
        QAP_T7544.execute(report_id, session_id)
        QAP_T7538.execute(report_id, session_id)
        QAP_T7537.execute(report_id, session_id)
        QAP_T7535.execute(report_id, session_id)
        QAP_T7533.execute(report_id, session_id)
        QAP_T7532.execute(report_id, session_id)
        QAP_T7531.execute(report_id, session_id)
        QAP_T7530.execute(report_id, session_id)
        QAP_T7518.execute(report_id, session_id)
        # QAP_T7512.execute(report_id, session_id)
        QAP_T7510.execute(report_id, session_id)
        QAP_T7507.execute(report_id, session_id)
        QAP_T7506.execute(report_id, session_id)
        QAP_T7505.execute(report_id, session_id)
        QAP_T7504.execute(report_id, session_id)
        QAP_T7503.execute(report_id, session_id)
        QAP_T7501.execute(report_id, session_id)
        QAP_T7500.execute(report_id, session_id)
        QAP_T7499.execute(report_id, session_id)
        QAP_T7498.execute(report_id, session_id)
        QAP_T7495.execute(report_id, session_id)
        QAP_T7485.execute(report_id, session_id)
        QAP_T7480.execute(report_id, session_id)
        QAP_T7476.execute(report_id, session_id)
        QAP_T7443.execute(report_id, session_id)
        QAP_T7443.execute(report_id, session_id)
        QAP_T7438.execute(report_id, session_id)
        QAP_3936.execute(report_id, session_id)
        QAP_T7383.execute(report_id, session_id)
        QAP_T7363.execute(report_id, session_id)
        QAP_T7360.execute(report_id, session_id)













    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"post trade regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
