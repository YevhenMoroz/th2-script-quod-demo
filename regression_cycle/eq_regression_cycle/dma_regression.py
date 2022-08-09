import logging
import traceback
from datetime import datetime

from custom import basic_custom_actions as bca
from test_cases.eq.DMA import QAP_T7616, QAP_T7615, QAP_T7614, QAP_T7613, QAP_T7560, QAP_T7370, QAP_T7612, QAP_T7611, \
    QAP_T7610, QAP_T7445, QAP_T7617, QAP_T7564, QAP_T7563
from stubs import Stubs
from win_gui_modules.utils import set_session_id

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

def safe(f):
    def safe_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(
                traceback.format_exc())
        finally:
            pass

    return safe_f

@safe
def test_run(parent_id=None):
    report_id = bca.create_event('DMA ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    session_id = set_session_id()
    QAP_T7617.execute(report_id, session_id)

    QAP_T7616.execute(report_id, session_id)
    QAP_T7615.execute(report_id, session_id)
    QAP_T7614.execute(report_id, session_id)
    QAP_T7613.execute(report_id, session_id)
    QAP_T7612.execute(report_id, session_id)
    QAP_T7611.execute(report_id, session_id)
    QAP_T7610.execute(report_id, session_id)
    QAP_T7560.execute(report_id, session_id)
    QAP_T7370.execute(report_id, session_id)
    # QAP_T7375.execute(report_id, session_id)
    # QAP_T7565.execute(report_id, session_id)
    QAP_T7564.execute(report_id, session_id)
    QAP_T7563.execute(report_id,session_id)
    QAP_T7445.execute(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
