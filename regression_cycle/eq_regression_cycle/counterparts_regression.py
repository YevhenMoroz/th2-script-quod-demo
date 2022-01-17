import logging
import traceback

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.eq.Counterpart.QAP_3503 import QAP_3503
from test_cases.eq.Counterpart.QAP_3509 import QAP_3509
from test_cases.eq.Counterpart.QAP_3510 import QAP_3510
from test_cases.eq.Counterpart.QAP_3743 import QAP_3743
from test_cases.eq.Counterpart.QAP_4111 import QAP_4111
from test_cases.eq.Counterpart.QAP_4421 import QAP_4421
from test_cases.eq.Counterpart.QAP_4903 import QAP_4903
from test_cases.eq.Counterpart.QAP_5860 import QAP_5860
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
    report_id = bca.create_event('Counterparts', parent_id)
    session_id = set_session_id()
    QAP_3503(report_id, session_id).execute()
    QAP_3509(report_id, session_id).execute()
    QAP_3510(report_id, session_id).execute()
    # QAP_3536(report_id, session_id).execute() need to rewrite
    QAP_3743(report_id, session_id).execute()
    QAP_4111(report_id, session_id).execute()
    QAP_4421(report_id, session_id).execute()
    QAP_4903(report_id, session_id).execute()
    QAP_5860(report_id, session_id).execute()


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
