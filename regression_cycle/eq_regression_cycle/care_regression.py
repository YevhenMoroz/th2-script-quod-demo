from custom.basic_custom_actions import timestamps
from test_cases.eq.Care import QAP_T7698, QAP_T7697, QAP_T7689, QAP_T7688, QAP_T7685, QAP_T7686, QAP_T7684, QAP_T7682, \
    QAP_T7683, QAP_T7681, QAP_T7680, QAP_T7677, QAP_T7676, QAP_T7674, QAP_T7673, QAP_T7672, QAP_T7671, QAP_T7670, QAP_T7669, \
    QAP_T7668, QAP_T7667, QAP_T7666, QAP_T7665, QAP_T7664, QAP_T7663, QAP_T7423, QAP_T7662, QAP_T7661, QAP_T7660, QAP_T7659, \
    QAP_T7658, QAP_T7657, QAP_T7656, QAP_T7655, QAP_T7654, QAP_T7633, QAP_T7632, QAP_T7629, QAP_T7628, QAP_T7626, QAP_T7623, \
    QAP_T7622, QAP_T7621, QAP_T7553, QAP_T7524, QAP_T7523, QAP_T7519, QAP_T7515, QAP_T7509, QAP_T7502, QAP_T7479, QAP_T7432, \
    QAP_T7419, QAP_T7418, QAP_T7403
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

def test_run(parent_id= None):
    report_id = bca.create_event('Care ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'), parent_id)
    session_id = set_session_id()
    seconds, nanos = timestamps()  # Store case start time
    try:
        QAP_T7698.execute(report_id, session_id)
        QAP_T7697.execute(report_id, session_id)
        QAP_T7689.execute(report_id, session_id)
        QAP_T7688.execute(report_id, session_id)
        # QAP_T7687.execute(report_id, session_id)
        QAP_T7686.execute(report_id, session_id)
        QAP_T7685.execute(report_id, session_id)
        QAP_T7684.execute(report_id, session_id)
        QAP_T7683.execute(report_id, session_id)
        QAP_T7682.execute(report_id, session_id)
        QAP_T7681.execute(report_id, session_id)
        QAP_T7680.execute(report_id, session_id)
        QAP_T7677.execute(report_id, session_id)
        QAP_T7676.execute(report_id, session_id)
        QAP_T7674.execute(report_id, session_id)
        QAP_T7673.execute(report_id, session_id)
        QAP_T7672.execute(report_id, session_id)
        QAP_T7671.execute(report_id, session_id)
        QAP_T7670.execute(report_id, session_id)
        QAP_T7669.execute(report_id, session_id)
        QAP_T7668.execute(report_id, session_id)
        QAP_T7667.execute(report_id, session_id)
        QAP_T7666.execute(report_id, session_id)
        QAP_T7665.execute(report_id, session_id)
        QAP_T7664.execute(report_id, session_id)
        QAP_T7663.execute(report_id, session_id)
        QAP_T7662.execute(report_id, session_id)
        QAP_T7661.execute(report_id, session_id)
        QAP_T7660.execute(report_id, session_id)
        QAP_T7659.execute(report_id, session_id)
        QAP_T7658.execute(report_id, session_id)
        QAP_T7657.execute(report_id, session_id)
        QAP_T7656.execute(report_id, session_id)
        QAP_T7655.execute(report_id, session_id)
        QAP_T7654.execute(report_id, session_id)
        QAP_T7633.execute(report_id, session_id)
        QAP_T7632.execute(report_id, session_id)
        QAP_T7629.execute(report_id, session_id)
        QAP_T7628.execute(report_id, session_id)
        QAP_T7626.execute(report_id, session_id)
        QAP_T7623.execute(report_id, session_id)
        QAP_T7622.execute(report_id, session_id)
        QAP_T7621.execute(report_id, session_id)
        QAP_T7553.execute(report_id, session_id)
        QAP_T7524.execute(report_id, session_id)
        QAP_T7523.execute(report_id, session_id)
        QAP_T7519.execute(report_id, session_id)
        QAP_T7515.execute(report_id, session_id)
        QAP_T7509.execute(report_id, session_id)
        QAP_T7502.execute(report_id, session_id)
        QAP_T7479.execute(report_id, session_id)
        QAP_T7432.execute(report_id, session_id)
        QAP_T7423.execute(report_id, session_id)
        QAP_T7419.execute(report_id, session_id)
        QAP_T7418.execute(report_id, session_id)
        QAP_T7403.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        logger.info(f"Care regression was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
