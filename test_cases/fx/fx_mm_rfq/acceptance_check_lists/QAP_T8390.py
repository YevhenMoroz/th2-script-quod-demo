from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2603 import QAP_T2603
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2580 import QAP_T2580
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2575 import QAP_T2575
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2574 import QAP_T2574
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2573 import QAP_T2573
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2559 import QAP_T2559
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2558 import QAP_T2558
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2537 import QAP_T2537
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_T2550 import QAP_T2550
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_T2597 import QAP_T2597
from test_cases.fx.fx_mm_rfq.rejection.QAP_T2598 import QAP_T2598
from test_cases.fx.fx_mm_rfq.rejection.QAP_T2595 import QAP_T2595
from test_cases.fx.fx_mm_rfq.update_quod_settings import update_settings_and_restart_qs

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def test_run(parent_id=None, version=None):
    version = "5.1.167.184"
    configuration = ComponentConfiguration("RFQ_MM")
    report_id = bca.create_event(f"FX_MM_RFQ" if version is None else f"FX_MM_RFQ | {version}", parent_id)
    session_id = set_session_id(target_server_win="ostronov")
    main_window_name = "Quod Financial - Quod site 314"
    try:
        # Region Manual Intervention
        update_settings_and_restart_qs("Manual Intervention")
        QAP_T2550(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2597(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Rejection
        update_settings_and_restart_qs("Rejection")
        QAP_T2595(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2598(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # Region Interpolation
        update_settings_and_restart_qs("Interpolation")
        QAP_T2537(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2558(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2559(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2573(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2574(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2575(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2580(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T2589(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2603(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # endregion

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        pass


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
