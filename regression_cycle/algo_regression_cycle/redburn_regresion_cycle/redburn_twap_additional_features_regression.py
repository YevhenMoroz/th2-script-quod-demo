import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_TWAP import QAP_T4332, QAP_T4286, QAP_T4335
from test_cases.algo.Algo_TWAP import QAP_T4692, QAP_T4693, QAP_T4694, QAP_T4695, QAP_T4557, QAP_T4696, QAP_T4572, QAP_T4697, QAP_T4579, QAP_T4698, QAP_T4600, QAP_T4699, QAP_T4605, QAP_T4700, QAP_T4655, QAP_T4701, QAP_T4664, QAP_T4702, QAP_T4665, QAP_T4666, QAP_T4687, QAP_T4690, QAP_T4691
from test_framework.configurations.component_configuration import ComponentConfiguration


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"TWAP - Additional Features | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        configuration = ComponentConfiguration("Twap")
        # QAP_T4872(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        QAP_T4332.execute(report_id)
        QAP_T4286.execute(report_id)
        QAP_T4335.execute(report_id)

        # region Needs Refactoring
        # QAP_T4692.execute(report_id)
        # QAP_T4693.execute(report_id)
        # QAP_T4694.execute(report_id)
        # QAP_T4695.execute(report_id)
        # QAP_T4557.execute(report_id)
        # QAP_T4696.execute(report_id)
        # QAP_T4572.execute(report_id)
        # QAP_T4697.execute(report_id)
        # QAP_T4579.execute(report_id)
        # QAP_T4698.execute(report_id)
        # QAP_T4600.execute(report_id)
        # QAP_T4699.execute(report_id)
        # QAP_T4605.execute(report_id)
        # QAP_T4700.execute(report_id)
        # QAP_T4655.execute(report_id)
        # QAP_T4701.execute(report_id)
        # QAP_T4664.execute(report_id)
        # QAP_T4702.execute(report_id)
        # QAP_T4665.execute(report_id)
        # QAP_T4666.execute(report_id)
        # QAP_T4687.execute(report_id)
        # QAP_T4690.execute(report_id)
        # QAP_T4691.execute(report_id)
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()