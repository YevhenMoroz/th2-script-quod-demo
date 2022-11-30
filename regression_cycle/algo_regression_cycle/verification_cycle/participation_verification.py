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
    report_id = bca.create_event(f"POV" if version is None else f"POV (verification) | {version}", parent_id)
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
        # QAP_T5039(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute() need change config to test
        QAP_T5064(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5088(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T5089(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
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
