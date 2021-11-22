from custom.basic_custom_actions import timestamps
from test_cases.eq.PostTrade import QAP_2614, QAP_2615, QAP_2697, QAP_2700, QAP_3338, QAP_3342, QAP_3343, QAP_3349, \
    QAP_3770, QAP_3333, QAP_3344, QAP_3784, QAP_2780, QAP_2849, QAP_2850, QAP_2973, QAP_3000, QAP_3217, QAP_3220, \
    QAP_3259, QAP_3303, QAP_3310, QAP_3315, QAP_3332, QAP_3334, QAP_3337, QAP_3352, QAP_3388, QAP_3413, QAP_3491, \
    QAP_3936, QAP_4349, QAP_4458, QAP_4471
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
        QAP_2614.execute(report_id, session_id)
        QAP_2615.execute(report_id, session_id)
        QAP_2697.execute(report_id, session_id)
        QAP_2700.execute(report_id, session_id)
        QAP_2780.execute(report_id, session_id)
        QAP_2849.execute(report_id, session_id)
        QAP_2850.execute(report_id, session_id)
        QAP_2973.execute(report_id, session_id)
        QAP_3000.execute(report_id, session_id)
        QAP_3217.execute(report_id, session_id)
        QAP_3220.execute(report_id, session_id)
        QAP_3259.execute(report_id, session_id)
        QAP_3303.execute(report_id, session_id)
        QAP_3310.execute(report_id, session_id)
        QAP_3315.execute(report_id, session_id)
        QAP_3332.execute(report_id, session_id)
        QAP_3333.execute(report_id, session_id)
        QAP_3334.execute(report_id, session_id)
        QAP_3337.execute(report_id, session_id)
        QAP_3338.execute(report_id, session_id)
        QAP_3342.execute(report_id, session_id)
        QAP_3343.execute(report_id, session_id)
        QAP_3344.execute(report_id, session_id)
        QAP_3349.execute(report_id, session_id)
        QAP_3352.execute(report_id, session_id)
        QAP_3388.execute(report_id, session_id)
        QAP_3413.execute(report_id, session_id)
        QAP_3491.execute(report_id, session_id)
        QAP_3770.execute(report_id, session_id)
        QAP_3770.execute(report_id, session_id)
        QAP_3784.execute(report_id, session_id)
        QAP_3936.execute(report_id, session_id)
        QAP_4349.execute(report_id, session_id)
        QAP_4458.execute(report_id, session_id)
        QAP_4471.execute(report_id, session_id)













    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"post trade regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
