import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4158 import QAP_T4158
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4360 import QAP_T4360
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4738 import QAP_T4738
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4872 import QAP_T4872
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4871 import QAP_T4871
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4870 import QAP_T4870
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4869 import QAP_T4869
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4868 import QAP_T4868
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4867 import QAP_T4867
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4866 import QAP_T4866
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4821 import QAP_T4821
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4811 import QAP_T4811
from test_cases.algo.Algo_Kepler.Algo_Iceberg.QAP_T4810 import QAP_T4810

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Iceberg" if version is None else f"Iceberg for th2 integration (cloned) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        configuration = ComponentConfiguration("Lit_dark_iceberg")
        QAP_T4872(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4871(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4870(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4869(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4868(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4867(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4866(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4821(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4811(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4810(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        QAP_T4738(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4158(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4360(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()



    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()