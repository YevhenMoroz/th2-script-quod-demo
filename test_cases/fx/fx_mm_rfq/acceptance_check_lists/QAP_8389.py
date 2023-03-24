from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2560 import QAP_T2560
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2579 import QAP_T2579
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2594 import QAP_T2594
from test_cases.fx.fx_mm_rfq.interpolation.QAP_T2596 import QAP_T2596
from test_cases.fx.fx_mm_rfq.manual_intervention.QAP_T2592 import QAP_T2592
from test_cases.fx.fx_mm_rfq.rejection.QAP_T2593 import QAP_T2593
from test_cases.fx.fx_mm_rfq.update_quod_settings import update_settings_and_restart_qs

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def test_run(parent_id=None, version=None):
    version = "5.1.167.184"
    configuration = ComponentConfiguration("RFQ_MM")
    report_id = bca.create_event(f"FX_MM_RFQ" if version is None else f"FX_MM_RFQ | {version}", parent_id)

    try:
        # Region Manual Intervention
        update_settings_and_restart_qs("Manual Intervention")
        QAP_T2592(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion
        # region Rejection
        update_settings_and_restart_qs("Rejection")
        QAP_T2593(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion
        # Region Interpolation
        update_settings_and_restart_qs("Interpolation")
        QAP_T2560(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2579(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2594(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2596(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion
    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        pass


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
