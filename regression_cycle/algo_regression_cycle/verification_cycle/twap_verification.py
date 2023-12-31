import time

from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_TWAP.QAP_T4988 import QAP_T4988
from test_cases.algo.Algo_TWAP.QAP_T5065 import QAP_T5065
from test_cases.algo.Algo_TWAP.QAP_T4936 import QAP_T4936
from test_cases.algo.Algo_TWAP.QAP_T4935 import QAP_T4935
from test_cases.algo.Algo_TWAP.QAP_T4924 import QAP_T4924
from test_cases.algo.Algo_TWAP.QAP_T4889 import QAP_T4889
from test_cases.algo.Algo_TWAP.QAP_T4887 import QAP_T4887
from test_cases.algo.Algo_TWAP.QAP_T4885 import QAP_T4885
from test_cases.algo.Algo_TWAP.QAP_T4884 import QAP_T4884
from test_cases.algo.Algo_TWAP.QAP_T4883 import QAP_T4883
from test_cases.algo.Algo_TWAP.QAP_T4882 import QAP_T4882
from test_cases.algo.Algo_TWAP.QAP_T4760 import QAP_T4760
from test_cases.algo.Algo_TWAP.QAP_T4886 import QAP_T4886
from test_cases.algo.Algo_TWAP.QAP_T4945 import QAP_T4945
from test_cases.algo.Algo_TWAP.QAP_T4588 import QAP_T4588
from test_cases.algo.Algo_TWAP.QAP_T4987 import QAP_T4987
from test_cases.algo.Algo_TWAP.QAP_T5091 import QAP_T5091
from test_cases.algo.Algo_TWAP.QAP_T5090 import QAP_T5090
from test_cases.algo.Algo_TWAP.QAP_T5087 import QAP_T5087
from test_cases.algo.Algo_TWAP.QAP_T4258 import QAP_T4258
from test_cases.algo.Algo_TWAP.QAP_T4265 import QAP_T4265
from test_cases.algo.Algo_TWAP.QAP_T4271 import QAP_T4271
from test_cases.algo.Algo_TWAP.QAP_T4946 import QAP_T4946
from test_cases.algo.Algo_TWAP.QAP_T4647 import QAP_T4647
from test_cases.algo.Algo_TWAP.QAP_T4276 import QAP_T4276
from test_cases.algo.Algo_TWAP.QAP_T4627 import QAP_T4627
from test_cases.algo.Algo_TWAP.QAP_T4259 import QAP_T4259
from test_cases.algo.Algo_TWAP.QAP_T4268 import QAP_T4268
from test_cases.algo.Algo_TWAP.QAP_T4704 import QAP_T4704
from test_cases.algo.Algo_TWAP.QAP_T8780 import QAP_T8780
from test_cases.algo.Algo_TWAP.QAP_T5013 import QAP_T5013
from test_cases.algo.Algo_TWAP.QAP_T4802 import QAP_T4802

from test_framework.configurations.component_configuration import ComponentConfiguration

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False
channels = dict()

work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

def test_run(parent_id= None, version = None):

    report_id = bca.create_event(f"TWAP" if version is None else f"Algo_TWAP (verification) | {version}", parent_id)
    try:
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)
        configuration = ComponentConfiguration("Twap")
        QAP_T4988(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5065(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4936(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4935(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4924(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4889(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4887(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4886(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4885(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4884(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4883(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4882(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4760(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(5)
        QAP_T4945(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4588(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4987(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5091(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5090(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(5)
        QAP_T5087(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4258(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4265(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4271(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(5)
        QAP_T4946(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4647(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4276(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4627(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4259(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4268(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        time.sleep(5)
        QAP_T4704(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8780(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5013(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4802(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # #FIX/FE
        # QAP_T4946.execute(report_id, session_id)
        # QAP_T4945.execute(report_id, session_id)
        # #end FIX/FE
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
