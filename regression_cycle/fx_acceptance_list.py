from test_cases.fx.fx_mm_autohedging import QAP_T2697, QAP_T2821, QAP_T2682, QAP_T2681, import_AH_layout
from test_cases.fx.fx_mm_esp import QAP_T2986, QAP_T2902, QAP_T2980, QAP_T2759, QAP_T2983, QAP_T2965, QAP_T2966, QAP_T2749, \
    QAP_T2758, QAP_T2897, QAP_2075, QAP_T2893
from test_cases.fx.fx_mm_positions import QAP_T2932, import_position_layout, QAP_T2933, QAP_T2935, QAP_T2934
from test_cases.fx.fx_mm_rfq import QAP_T2940, QAP_T2906, QAP_T2969, QAP_T2714, QAP_T2716
from test_cases.fx.fx_mm_rfq.QAP_T2677 import QAP_T2677
from test_cases.fx.fx_mm_rfq.interpolation import QAP_T2596, QAP_T2575, QAP_T2580
from test_cases.fx.fx_mm_synthetic import QAP_T2782
from test_cases.fx.fx_taker_esp import QAP_T2685
from test_cases.fx.fx_taker_rfq import QAP_T3071, QAP_T3070, QAP_T3065, QAP_T2748, QAP_T2747, QAP_T2744, QAP_T2746, QAP_T2717, \
    import_rfq_taker_layout
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe, close_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event('Acceptance list', parent_id)
    session_id = set_session_id()
    main_window_name = "Quod Financial - Quod site 314"

    configuration = ComponentConfiguration("FX_Acceptance_list")
    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id, main_window_name)

            # region RFQ taker
            import_rfq_taker_layout.execute(report_id, session_id)
            QAP_T3071.execute(report_id, session_id)
            QAP_T3070.execute(report_id, session_id)
            QAP_T3065.execute(report_id, session_id)
            QAP_T2748.execute(report_id, session_id)
            QAP_T2747.execute(report_id, session_id)
            QAP_T2744.execute(report_id, session_id)
            QAP_T2746.execute(report_id, session_id)
            QAP_T2717.execute(report_id, session_id)
            # endregion

            # region ESP taker

            # endregion

            # region ESP maker
            QAP_T2986.execute(report_id, session_id)
            QAP_T2983.execute(report_id)
            QAP_T2980.execute(report_id, session_id)
            QAP_T2966.execute(report_id)
            QAP_T2965.execute(report_id)
            QAP_T2902.execute(report_id, session_id)
            QAP_2075.execute(report_id, report_id)
            QAP_T2897.execute(report_id)
            QAP_T2893.execute(report_id)
            QAP_T2782.execute(report_id, session_id)
            QAP_T2758.execute(report_id)
            QAP_T2759.execute(report_id, session_id)
            QAP_T2749.execute(report_id, session_id)
            QAP_T2685.execute(report_id, session_id)
            # endregion

            # region RFQ maker
            QAP_T2969.execute(report_id)
            QAP_T2940.execute(report_id)
            QAP_T2906.execute(report_id, report_id)
            QAP_T2716.execute(report_id)
            QAP_T2714.execute(report_id, report_id)
            QAP_T2677(report_id, session_id, configuration.data_set, configuration.environment).execute()
            QAP_T2596.execute(report_id, report_id)
            QAP_T2580.execute(report_id)
            QAP_T2575.execute(report_id)
            # endregion

            # region AutoHedger
            QAP_T2697.execute(report_id, session_id)
            QAP_T2821.execute(report_id, session_id)
            # endregion

            # region Position
            import_position_layout.execute(report_id, session_id)
            QAP_T2932.execute(report_id, session_id)
            # endregion
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        # close_fe(report_id, session_id)
        Stubs.win_act.unregister(session_id)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
