import logging
import traceback
from datetime import datetime

from custom import basic_custom_actions as bca
from test_cases.eq.DMA import QAP_2001, QAP_2002, QAP_2003, QAP_2005, QAP_2551, QAP_4393, QAP_4375, QAP_2006, QAP_2007, \
    QAP_2008, QAP_2522, QAP_3723, QAP_2000, QAP_2546, QAP_2547
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
    QAP_2000.execute(report_id, session_id)

    QAP_2001.execute(report_id, session_id)
    QAP_2002.execute(report_id, session_id)
    QAP_2003.execute(report_id, session_id)
    QAP_2005.execute(report_id, session_id)
    QAP_2006.execute(report_id, session_id)
    QAP_2007.execute(report_id, session_id)
    QAP_2008.execute(report_id, session_id)
    QAP_2551.execute(report_id, session_id)
    QAP_4393.execute(report_id, session_id)
    QAP_4375.execute(report_id, session_id)
    QAP_2522.execute(report_id, session_id)
    QAP_2546.execute(report_id, session_id)
    QAP_2547.execute(report_id,session_id)
    QAP_3723.execute(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
