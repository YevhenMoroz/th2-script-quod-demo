from quod_qa.fx.fx_mm_autohedging import QAP_2252, QAP_2113, QAP_2228, QAP_2250, QAP_2251, QAP_2290, QAP_2159, QAP_2255, \
    QAP_3939, QAP_3039, QAP_3354, QAP_3067, QAP_1762, QAP_2326, QAP_5551, QAP_2322, QAP_2291, QAP_2292, QAP_3147, \
    QAP_3146, QAP_2265, QAP_3082, QAP_3819, QAP_4122, QAP_2293
from quod_qa.fx.fx_mm_autohedging import QAP_2159, QAP_2255, \
    QAP_3939, QAP_3039, QAP_2470, QAP_3354, QAP_3067, QAP_1762, QAP_2326, import_AH_layout, AH_Precondition
from quod_qa.fx.fx_mm_autohedging import QAP_2252, QAP_2113, QAP_2228, QAP_2250, QAP_2251, QAP_2290, QAP_2291, QAP_2292, \
    QAP_3902
from quod_qa.fx.fx_mm_positions.prepare_position import prepare_position
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe, prepare_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('ESP MM AH regression', parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    fe_dir = Stubs.custom_config['qf_trading_fe_folder']
    fe_user = Stubs.custom_config['qf_trading_fe_user']
    fe_password = Stubs.custom_config['qf_trading_fe_password']

    try:
        prepare_position()
        Stubs.frontend_is_open = True
        if not Stubs.frontend_is_open:
            prepare_fe(report_id, session_id, fe_dir, fe_user, fe_password)
        else:
            get_opened_fe(report_id, session_id)

        import_AH_layout.execute(report_id, session_id)
        AH_Precondition.execute(report_id)
        QAP_1762.execute(report_id, session_id)
        QAP_2113.execute(report_id, session_id)
        QAP_2159.execute(report_id, session_id)
        QAP_2228.execute(report_id, session_id)
        QAP_2255.execute(report_id, session_id)
        QAP_2322.execute(report_id, session_id)
        QAP_3939.execute(report_id, session_id)
        QAP_3039.execute(report_id, session_id)
        QAP_3354.execute(report_id, session_id)
        QAP_3067.execute(report_id, session_id)
        QAP_2326.execute(report_id, session_id)
        QAP_5551.execute(report_id, session_id)
        QAP_2470.execute(report_id, session_id)
        QAP_3147.execute(report_id, session_id)
        QAP_3146.execute(report_id, session_id)
        QAP_3082.execute(report_id, session_id)
        QAP_3819.execute(report_id, session_id)
        QAP_4122.execute(report_id, session_id)
        # Rest API
        QAP_3902.execute(report_id, session_id)
        QAP_2292.execute(report_id, session_id)
        QAP_2291.execute(report_id, session_id)
        QAP_2290.execute(report_id, session_id)
        QAP_2252.execute(report_id, session_id)
        QAP_2251.execute(report_id, session_id)
        QAP_2250.execute(report_id, session_id)
        QAP_2265.execute(report_id, session_id)
        QAP_2293.execute(report_id, session_id)
    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
