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

    report_id = bca.create_event(f"TWAP" if version is None else f"TWAP (cloned) | {version}", parent_id)
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
        # #FIX/FE
        # QAP_T4946.execute(report_id, session_id)
        # QAP_T4945.execute(report_id, session_id)
        # #end FIX/FE
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
