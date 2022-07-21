import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3150 import QAP_3150
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3151 import QAP_3151
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3153 import QAP_3153
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3154 import QAP_3154
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3155 import QAP_3155
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3156 import QAP_3156
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3158 import QAP_3158
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3203 import QAP_3203
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3218 import QAP_3218
from test_cases.algo.Algo_Kepler.Algo_Iceberg_Route_Venue.QAP_3221 import QAP_3221

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None):
    # Generation id and time for test run
    report_id = bca.create_event('Iceberg', parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        configuration = ComponentConfiguration("lit_dark_iceberg")
        QAP_3150(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3151(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3153(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3154(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3155(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3156(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3158(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3203(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3218(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_3221(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()