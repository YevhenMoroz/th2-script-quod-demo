import time

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_PercentageVolume.QAP_T4761 import QAP_T4761
from test_cases.algo.Algo_PercentageVolume.QAP_T4879 import QAP_T4879
from test_cases.algo.Algo_PercentageVolume.QAP_T4890 import QAP_T4890
from test_cases.algo.Algo_PercentageVolume.QAP_T4911 import QAP_T4911
from test_cases.algo.Algo_PercentageVolume.QAP_T4912 import QAP_T4912
from test_cases.algo.Algo_PercentageVolume.QAP_T4913 import QAP_T4913
from test_cases.algo.Algo_PercentageVolume.QAP_T4914 import QAP_T4914
from test_cases.algo.Algo_PercentageVolume.QAP_T4915 import QAP_T4915
from test_cases.algo.Algo_PercentageVolume.QAP_T4933 import QAP_T4933
from test_cases.algo.Algo_PercentageVolume.QAP_T5039 import QAP_T5039
from test_cases.algo.Algo_PercentageVolume.QAP_T5064 import QAP_T5064
from test_cases.algo.Algo_PercentageVolume.QAP_T5088 import QAP_T5088
from test_cases.algo.Algo_PercentageVolume.QAP_T5089 import QAP_T5089
from test_cases.algo.Algo_PercentageVolume.QAP_T4269 import QAP_T4269
from test_cases.algo.Algo_PercentageVolume.QAP_T4274 import QAP_T4274
from test_cases.algo.Algo_PercentageVolume.QAP_T4263 import QAP_T4263
from test_cases.algo.Algo_PercentageVolume.QAP_T4266 import QAP_T4266
from test_cases.algo.Algo_PercentageVolume.QAP_T5050 import QAP_T5050
from test_cases.algo.Algo_PercentageVolume.QAP_T5084 import QAP_T5084
from test_cases.algo.Algo_PercentageVolume.QAP_T5049 import QAP_T5049
from test_cases.algo.Algo_PercentageVolume.QAP_T8739 import QAP_T8739
from test_cases.algo.Algo_PercentageVolume.QAP_T8880 import QAP_T8880
from test_cases.algo.Algo_PercentageVolume.QAP_T9275 import QAP_T9275
from test_cases.algo.Algo_PercentageVolume.QAP_T9158 import QAP_T9158
from test_cases.algo.Algo_PercentageVolume.QAP_T9456 import QAP_T9456
from test_cases.algo.Algo_PercentageVolume.QAP_T9454 import QAP_T9454
from test_cases.algo.Algo_PercentageVolume.QAP_T9453 import QAP_T9453
from test_cases.algo.Algo_PercentageVolume.QAP_T9232 import QAP_T9232
from test_cases.algo.Algo_PercentageVolume.QAP_T9157 import QAP_T9157
from test_cases.algo.Algo_PercentageVolume.QAP_T9156 import QAP_T9156
from test_cases.algo.Algo_PercentageVolume.QAP_T9098 import QAP_T9098
from test_cases.algo.Algo_PercentageVolume.QAP_T9094 import QAP_T9094
from test_cases.algo.Algo_PercentageVolume.QAP_T9093 import QAP_T9093
from test_cases.algo.Algo_PercentageVolume.QAP_T9084 import QAP_T9084
from test_cases.algo.Algo_PercentageVolume.QAP_T4260 import QAP_T4260
from test_cases.algo.Algo_PercentageVolume.QAP_T4261 import QAP_T4261

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']


def test_run(parent_id=None, version=None):
    report_id = bca.create_event(f"POV" if version is None else f"Algo_POV (verification) | {version}", parent_id)
    try:
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)
        configuration = ComponentConfiguration("Participation")
        QAP_T4761(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4879(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4890(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4911(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4912(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4913(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4914(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4915(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4933(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5064(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5088(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5089(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4269(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4274(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(5)
        QAP_T4263(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4266(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5050(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(5)
        QAP_T5084(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(5)
        QAP_T5049(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8739(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8880(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T9275(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        if __name__ == '__main__':
            # tests with config change
            QAP_T9158(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9456(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9454(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9453(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9232(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9157(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9156(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9098(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9094(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9093(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T9084(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T4260(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T4261(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
            QAP_T5039(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # FIX/FE
        # QAP_T5113.execute(report_id, session_id)
        # QAP_T5097.execute(report_id, session_id)
        # QAP_T5096.execute(report_id, session_id)
        # QAP_T5095.execute(report_id, session_id)
        # QAP_T5084.execute(report_id, session_id)
        # QAP_T5050.execute(report_id, session_id)
        # QAP_T5049.execute(report_id, session_id)
        # QAP_T4950.execute(report_id, session_id)
        # end FIX/FE
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
