from test_cases.fx.fx_mm_esp import QAP_1560, QAP_1599, QAP_2034, QAP_2035, QAP_2037, \
    QAP_2038, QAP_2039, QAP_2117, QAP_2523, QAP_2555, \
    QAP_3563, QAP_1559, \
    QAP_3841, QAP_3390, QAP_2750, QAP_2823, QAP_2874, QAP_2876, \
    QAP_2880, QAP_2879, QAP_2873, QAP_2966, QAP_3848, QAP_2012, QAP_4094, \
    QAP_4016, QAP_3661, QAP_1644, QAP_2990, QAP_2844, QAP_2050, QAP_2051, QAP_6148, QAP_6151, QAP_1558
from test_cases.fx.fx_mm_esp.QAP_1418 import QAP_1418
from test_cases.fx.fx_mm_esp.QAP_1511 import QAP_1511
from test_cases.fx.fx_mm_esp.QAP_1518 import QAP_1518
from test_cases.fx.fx_mm_esp.QAP_1536 import QAP_1536
from test_cases.fx.fx_mm_esp.QAP_1554 import QAP_1554
from test_cases.fx.fx_mm_esp.QAP_1589 import QAP_1589
from test_cases.fx.fx_mm_esp.QAP_1597 import QAP_1597
from test_cases.fx.fx_mm_esp.QAP_1601 import QAP_1601
from test_cases.fx.fx_mm_esp.QAP_2069 import QAP_2069
from test_cases.fx.fx_mm_esp.QAP_2072 import QAP_2072
from test_cases.fx.fx_mm_esp.QAP_2075 import QAP_2075
from test_cases.fx.fx_mm_esp.QAP_2078 import QAP_2078
from test_cases.fx.fx_mm_esp.QAP_2079 import QAP_2079
from test_cases.fx.fx_mm_esp.QAP_2082 import QAP_2082
from test_cases.fx.fx_mm_esp.QAP_2084 import QAP_2084
from test_cases.fx.fx_mm_esp.QAP_2085 import QAP_2085
from test_cases.fx.fx_mm_esp.QAP_2086 import QAP_2086
from test_cases.fx.fx_mm_esp.QAP_2556 import QAP_2556
from test_cases.fx.fx_mm_esp.QAP_2587 import QAP_2587
from test_cases.fx.fx_mm_esp.QAP_2796 import QAP_2796
from test_cases.fx.fx_mm_esp.QAP_2797 import QAP_2797
from test_cases.fx.fx_mm_esp.QAP_2825 import QAP_2825
from test_cases.fx.fx_mm_esp.QAP_2855 import QAP_2855
from test_cases.fx.fx_mm_esp.QAP_2872 import QAP_2872
from test_cases.fx.fx_mm_esp.QAP_2957 import QAP_2957
from test_cases.fx.fx_mm_esp.QAP_3045 import QAP_3045
from test_cases.fx.fx_mm_esp.QAP_3537 import QAP_3537
from test_cases.fx.fx_mm_esp.QAP_5389 import QAP_5389
from test_cases.fx.fx_mm_esp.QAP_6145 import QAP_6145
from test_cases.fx.fx_mm_esp.QAP_6149 import QAP_6149
from test_cases.fx.fx_mm_esp.QAP_6153 import QAP_6153
from test_cases.fx.fx_mm_esp.QAP_6289 import QAP_6289
from test_cases.fx.fx_mm_esp.QAP_6931 import QAP_6931
from test_cases.fx.fx_mm_esp.QAP_6932 import QAP_6932
from test_cases.fx.fx_mm_esp.QAP_6933 import QAP_6933
from test_cases.fx.fx_mm_esp.QAP_7160 import QAP_7160
from test_cases.fx.fx_mm_esp.QAP_7167 import QAP_7167
from test_cases.fx.fx_mm_esp.QAP_8010 import QAP_8010
from test_cases.fx.fx_mm_esp.QAP_8224 import QAP_8224
from test_cases.fx.fx_mm_esp.QAP_T2479 import QAP_T2479
from test_cases.fx.fx_mm_esp.QAP_T2602 import QAP_T2602
from test_cases.fx.fx_mm_esp.QAP_T2957 import QAP_T2957
from test_cases.fx.fx_mm_synthetic import QAP_2646
from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.fx.fx_taker_esp import QAP_3140, QAP_3141
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet

from win_gui_modules.utils import set_session_id, prepare_fe_2, get_opened_fe

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()


def test_run(parent_id=None):
    report_id = bca.create_event('ESP MM regression', parent_id)
    session_id = set_session_id()
    Stubs.custom_config['qf_trading_fe_main_win_name'] = "Quod Financial - Quod site 314"
    data_set = FxDataSet()
    configuration = ComponentConfiguration("ESP_MM")

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(report_id, session_id)
        else:
            get_opened_fe(report_id, session_id)
        QAP_1418(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1536(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1560.execute(report_id, session_id)
        QAP_1599.execute(report_id, session_id)
        QAP_1601(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2034.execute(report_id, session_id)
        QAP_2035.execute(report_id, session_id)
        QAP_2037.execute(report_id, session_id)
        QAP_2038.execute(report_id, session_id)
        QAP_2039.execute(report_id, session_id)
        QAP_2050.execute(report_id, session_id)
        QAP_2051.execute(report_id, session_id)
        QAP_2069(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2072(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2075(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2117.execute(report_id, session_id)
        QAP_2523.execute(report_id, session_id)
        QAP_2555.execute(report_id, session_id)
        QAP_2556(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2587(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2646.execute(report_id, session_id)
        QAP_2796(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2825(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2844.execute(report_id, session_id)
        QAP_2855(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3045(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3563.execute(report_id, session_id)
        QAP_1511(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1589(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_4016.execute(report_id, session_id)
        QAP_3661.execute(report_id, session_id)
        QAP_3140.execute(report_id, session_id)
        QAP_6148.execute(report_id, session_id)
        QAP_1518(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1554(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_1558.execute(report_id)
        QAP_1559.execute(report_id)
        QAP_1597(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2012.execute(report_id)
        QAP_2078(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2079(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2082(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2084(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2085(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2086(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2750.execute(report_id)
        QAP_2797(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2823.execute(report_id)
        QAP_2872(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2873.execute(report_id)
        QAP_2874.execute(report_id)
        QAP_2876.execute(report_id)
        QAP_2879.execute(report_id)
        QAP_2880.execute(report_id)
        QAP_2957(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_2966.execute(report_id)
        ##### QAP_2990.execute(report_id)  // NOT READY
        QAP_3141.execute(report_id)
        QAP_3390.execute(report_id)
        QAP_3841.execute(report_id)
        QAP_3848.execute(report_id)
        QAP_4094.execute(report_id)
        QAP_5389().execute(report_id)
        QAP_6145(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_6151.execute(report_id)
        QAP_6153(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_6149(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3537(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_6289(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_6931(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_6932(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_6933(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_7160(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_7167(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_8010(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_8224(report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T2479(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2602(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()
        QAP_T2957(report_id=report_id, session_id=session_id, data_set=configuration.data_set,
                  environment=configuration.environment).execute()



    except Exception:
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
