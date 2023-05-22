from test_cases.fx.fx_mm_autohedging.QAP_T10301 import QAP_T10301
from test_cases.fx.fx_mm_autohedging.QAP_T10439 import QAP_T10439
from test_cases.fx.fx_mm_autohedging.QAP_T10440 import QAP_T10440
from test_cases.fx.fx_mm_autohedging.QAP_T10443 import QAP_T10443
from test_cases.fx.fx_mm_autohedging.QAP_T10444 import QAP_T10444
from test_cases.fx.fx_mm_autohedging.QAP_T10711 import QAP_T10711
from test_cases.fx.fx_mm_autohedging.QAP_T10750 import QAP_T10750
from test_cases.fx.fx_mm_autohedging.QAP_T10775 import QAP_T10775
from test_cases.fx.fx_mm_autohedging.QAP_T10780 import QAP_T10780
from test_cases.fx.fx_mm_autohedging.QAP_T2681 import QAP_T2681
from test_cases.fx.fx_mm_autohedging.QAP_T2682 import QAP_T2682
from test_cases.fx.fx_mm_autohedging.QAP_T2862 import QAP_T2862
from test_cases.fx.fx_mm_autohedging.QAP_T9220 import QAP_T9220
from test_cases.fx.fx_mm_autohedging.QAP_T9228 import QAP_T9228
from test_cases.fx.fx_mm_autohedging.QAP_T9412 import QAP_T9412
from test_cases.fx.fx_mm_autohedging.QAP_T9464 import QAP_T9464
from test_cases.fx.fx_mm_autohedging.QAP_T9468 import QAP_T9468
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_mm_positions.prepare_position import prepare_position
from test_framework.configurations.component_configuration import ComponentConfiguration, ComponentConfigurationFX

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event("FX_MM_Autohedger_automation" if version is None
                                 else f"FX_MM_Autohedger_automation | {version}", parent_id)
    # configuration = ComponentConfigurationFX("ESP_MM_309")
    configuration = ComponentConfiguration("AutoHedger")
    try:
        # prepare_position()
        QAP_T10301(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10444(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2681(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2862(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9220(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9228(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9412(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9464(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9468(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10439(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10440(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10443(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10711(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # QAP_T10750(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10775(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10780(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
