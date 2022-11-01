from stubs import Stubs
import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_TimeInForce.QAP_T4208 import QAP_T4208
from test_cases.algo.Algo_TimeInForce.QAP_T4207 import QAP_T4207
from test_cases.algo.Algo_TimeInForce.QAP_T4224 import QAP_T4224
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

    report_id = bca.create_event(f"Algo_TimeInForce" if version is None else f"Algo_TimeInForce | {version}", parent_id)
    try:
        # session_id = set_session_id()
        # if not Stubs.frontend_is_open:
        #     prepare_fe(report_id, session_id, work_dir, username, password)
        # else:
        #     get_opened_fe(report_id, session_id, work_dir)
        configuration = ComponentConfiguration("TimeInForce")
        QAP_T4208(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4224(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4207(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
    except Exception:
        logging.error("Error execution", exc_info=True)



if __name__ == '__main__':
    test_run()
    Stubs.factory.close()
