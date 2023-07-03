from test_cases.fx.fx_mm_positions.QAP_T10342 import QAP_T10342
from test_cases.fx.fx_mm_positions.QAP_T10400 import QAP_T10400
from test_cases.fx.fx_mm_positions.QAP_T10411 import QAP_T10411
from test_cases.fx.fx_mm_positions.QAP_T10457 import QAP_T10457
from test_cases.fx.fx_mm_positions.QAP_T10460 import QAP_T10460
from test_cases.fx.fx_mm_positions.QAP_T10461 import QAP_T10461
from test_cases.fx.fx_mm_positions.QAP_T10612 import QAP_T10612
from test_cases.fx.fx_mm_positions.QAP_T10613 import QAP_T10613
from test_cases.fx.fx_mm_positions.QAP_T10614 import QAP_T10614
from test_cases.fx.fx_mm_positions.QAP_T10635 import QAP_T10635
from test_cases.fx.fx_mm_positions.QAP_T10636 import QAP_T10636
from test_cases.fx.fx_mm_positions.QAP_T10649 import QAP_T10649
from test_cases.fx.fx_mm_positions.QAP_T10760 import QAP_T10760
from test_cases.fx.fx_mm_positions.QAP_T10840 import QAP_T10840
from test_cases.fx.fx_mm_positions.QAP_T10842 import QAP_T10842
from test_cases.fx.fx_mm_positions.QAP_T10845 import QAP_T10845
from test_cases.fx.fx_mm_positions.QAP_T11053 import QAP_T11053
from test_cases.fx.fx_mm_positions.QAP_T11080 import QAP_T11080
from test_cases.fx.fx_mm_positions.QAP_T11216 import QAP_T11216
from test_cases.fx.fx_mm_positions.QAP_T11217 import QAP_T11217
from test_cases.fx.fx_mm_positions.QAP_T11218 import QAP_T11218
from test_cases.fx.fx_mm_positions.QAP_T11222 import QAP_T11222
from test_cases.fx.fx_mm_positions.QAP_T11224 import QAP_T11224
from test_cases.fx.fx_mm_positions.QAP_T11502 import QAP_T11502
from test_cases.fx.fx_mm_positions.QAP_T2804 import QAP_T2804
from test_cases.fx.fx_mm_positions.QAP_T2805 import QAP_T2805
from test_cases.fx.fx_mm_positions.QAP_T2808 import QAP_T2808
from test_cases.fx.fx_mm_positions.QAP_T2809 import QAP_T2809
from test_cases.fx.fx_mm_positions.QAP_T2810 import QAP_T2810
from test_cases.fx.fx_mm_positions.QAP_T2811 import QAP_T2811
from test_cases.fx.fx_mm_positions.QAP_T2812 import QAP_T2812
from test_cases.fx.fx_mm_positions.QAP_T2813 import QAP_T2813
from test_cases.fx.fx_mm_positions.QAP_T2932 import QAP_T2932
from test_cases.fx.fx_mm_positions.QAP_T2933 import QAP_T2933
from test_cases.fx.fx_mm_positions.QAP_T2934 import QAP_T2934
from test_cases.fx.fx_mm_positions.QAP_T2935 import QAP_T2935
from test_cases.fx.fx_mm_positions.QAP_T8424 import QAP_T8424
from test_cases.fx.fx_mm_positions.QAP_T9408 import QAP_T9408
from test_cases.fx.fx_mm_positions.prepare_position import prepare_position
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_framework.configurations.component_configuration import ComponentConfiguration, ComponentConfigurationFX

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None, version="5.1.178.194"):
    # report_id = bca.create_event(f"FX_MM_Positions" if version is None else f"FX_MM_Positions | {version}", parent_id)
    report_id = bca.create_event(f"FX_MM_Positions | {version}", parent_id)
    configuration = ComponentConfiguration("Position")
    try:
        # prepare_position()
        # QAP_T11053(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        QAP_T2804(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2805(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2808(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2809(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2810(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2811(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2812(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2813(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2932(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2933(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2934(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2935(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8424(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9408(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10342(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10400(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10411(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10457(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10460(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10461(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10612(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10613(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10614(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10635(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10636(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10649(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10760(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10840(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10842(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10842(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10845(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11080(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11216(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11217(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11218(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11222(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11224(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11502(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()


    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
