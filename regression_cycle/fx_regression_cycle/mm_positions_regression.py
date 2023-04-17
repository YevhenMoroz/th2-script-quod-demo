from test_cases.fx.fx_mm_positions.QAP_T10457 import QAP_T10457
from test_cases.fx.fx_mm_positions.QAP_T10760 import QAP_T10760
from test_cases.fx.fx_mm_positions.QAP_T10840 import QAP_T10840
from test_cases.fx.fx_mm_positions.QAP_T11053 import QAP_T11053
from test_cases.fx.fx_mm_positions.QAP_T11080 import QAP_T11080
from test_cases.fx.fx_mm_positions.QAP_T2932 import QAP_T2932
from test_cases.fx.fx_mm_positions.QAP_T2933 import QAP_T2933
from test_cases.fx.fx_mm_positions.QAP_T2934 import QAP_T2934
from test_cases.fx.fx_mm_positions.QAP_T2935 import QAP_T2935
from test_cases.fx.fx_mm_positions.QAP_T9408 import QAP_T9408
from test_cases.fx.fx_mm_positions.prepare_position import prepare_position
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"FX_MM_Positions" if version is None else f"FX_MM_Positions | {version}", parent_id)
    configuration = ComponentConfiguration("Position")
    try:
        prepare_position()
        QAP_T2932(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2933(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2934(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2935(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        QAP_T9408(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10457(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10760(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10840(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11053(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11080(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
