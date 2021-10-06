from quod_qa.fx.fx_mm_autohedging import QAP_2159, QAP_2255, \
    QAP_3939, QAP_3039, QAP_2470, QAP_3354, QAP_3067, QAP_1762, QAP_2326, import_AH_layout, AH_Precondition
from quod_qa.fx.fx_mm_autohedging import QAP_2252, QAP_2113, QAP_2228, QAP_2250, QAP_2251, QAP_2290, QAP_2291, QAP_2292, \
    QAP_3902
from quod_qa.fx.fx_mm_positions.prepare_position import prepare_position
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('ESP MM AH regression', parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"

    try:
        prepare_position()
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

        import_AH_layout.execute(report_id, session_id)
        AH_Precondition.execute(report_id)

        QAP_2113.execute(report_id, session_id)
        QAP_2228.execute(report_id, session_id)
        QAP_2250.execute(report_id, session_id)
        QAP_2251.execute(report_id, session_id)
        QAP_2252.execute(report_id, session_id)
        QAP_2290.execute(report_id, session_id)
        QAP_2291.execute(report_id, session_id)
        QAP_2292.execute(report_id, session_id)
        QAP_3902.execute(report_id, session_id)
        QAP_2159.execute(report_id, session_id)
        QAP_2255.execute(report_id, session_id)
        QAP_3939.execute(report_id, session_id)
        QAP_3039.execute(report_id, session_id)
        QAP_3354.execute(report_id, session_id)
        QAP_3067.execute(report_id, session_id)
        QAP_1762.execute(report_id, session_id)
        QAP_2326.execute(report_id, session_id)
        QAP_2470.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
