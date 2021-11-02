from quod_qa.fx.fx_mm_autohedging import QAP_3082, QAP_2470
from quod_qa.fx.fx_mm_esp import QAP_1418, QAP_2069, QAP_1536, QAP_2796, QAP_1518, QAP_1559, QAP_1558, QAP_2825, \
    QAP_2797, QAP_2078, QAP_2075, QAP_2082
from quod_qa.fx.fx_mm_positions import QAP_1898, import_position_layout
from quod_qa.fx.fx_mm_rfq import QAP_1746, QAP_2062, QAP_1552, QAP_3005, QAP_3003
from quod_qa.fx.fx_mm_rfq.interpolation import QAP_3734, QAP_3805, QAP_3766
from quod_qa.fx.fx_mm_synthetic import QAP_2646
from quod_qa.fx.fx_taker_esp import QAP_3140
from quod_qa.fx.fx_taker_rfq import QAP_568, QAP_569, QAP_574, QAP_2826, QAP_2835, QAP_2847, QAP_2836, QAP_3002, \
    import_rfq_taker_layout
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('Acceptance list', parent_id)
    session_id = set_session_id()
    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)

            # region RFQ taker
            import_rfq_taker_layout.execute(report_id, session_id)
            QAP_568.execute(report_id, session_id)
            QAP_569.execute(report_id, session_id)
            QAP_574.execute(report_id, session_id)
            QAP_2826.execute(report_id, session_id)
            QAP_2835.execute(report_id, session_id)
            QAP_2847.execute(report_id, session_id)
            QAP_2836.execute(report_id, session_id)
            QAP_3002.execute(report_id, session_id)
            # endregion

            # region ESP taker

            # endregion

            # region ESP maker
            QAP_1418.execute(report_id, session_id)
            QAP_1518.execute(report_id)
            QAP_1536.execute(report_id, session_id)
            QAP_1558.execute(report_id)
            QAP_1559.execute(report_id)
            QAP_2069.execute(report_id, session_id)
            QAP_2075.execute(report_id, report_id)
            QAP_2078.execute(report_id)
            QAP_2082.execute(report_id)
            QAP_2646.execute(report_id, session_id)
            QAP_2797.execute(report_id)
            QAP_2796.execute(report_id, session_id)
            QAP_2825.execute(report_id, session_id)
            QAP_3140.execute(report_id, session_id)
            # endregion

            # region RFQ maker
            QAP_1552.execute(report_id)
            QAP_1746.execute(report_id)
            QAP_2062.execute(report_id, report_id)
            QAP_3003.execute(report_id)
            QAP_3005.execute(report_id, report_id)
            QAP_3734.execute(report_id, report_id)
            QAP_3766.execute(report_id)
            QAP_3805.execute(report_id)
            # endregion

            # region AutoHedger
            QAP_3082.execute(report_id, session_id)
            QAP_2470.execute(report_id, session_id)
            # endregion

            # region Position
            import_position_layout.execute(report_id, session_id)
            QAP_1898.execute(report_id, session_id)
            # endregion
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        close_fe(report_id, session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
