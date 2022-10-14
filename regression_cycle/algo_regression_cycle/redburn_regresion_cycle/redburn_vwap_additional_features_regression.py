import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_VWAP import QAP_T4331, QAP_T4334
from test_cases.algo.Algo_VWAP import QAP_T4563, QAP_T4583, QAP_T4584, QAP_T4601, QAP_T4611, QAP_T4612, QAP_T4613, QAP_T4615, QAP_T4616
from test_framework.configurations.component_configuration import ComponentConfiguration


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"VWAP - Additional Features | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        # configuration = ComponentConfiguration("Vwap")
        configuration = ComponentConfiguration("Scaling")
        # QAP_T4872(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # QAP_T4331.execute(report_id)
        # QAP_T4334.execute(report_id)

        # region Needs Refactoring
        # QAP_T4563.execute(report_id)
        # QAP_T4583.execute(report_id)
        # QAP_T4584.execute(report_id)
        # QAP_T4601.execute(report_id)
        # QAP_T4611.execute(report_id)
        # QAP_T4612.execute(report_id)
        # QAP_T4613.execute(report_id)
        # QAP_T4615.execute(report_id)
        # QAP_T4616.execute(report_id)
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()