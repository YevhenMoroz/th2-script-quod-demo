import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_POV import QAP_T4333, QAP_T4330
from test_cases.algo.Algo_PercentageVolume import QAP_T4573, QAP_T4574, QAP_T4580, QAP_T4599, QAP_T4604, QAP_T4629, QAP_T4631, QAP_T4648, QAP_T4659, QAP_T4660, QAP_T4556, QAP_T4661, QAP_T4565, QAP_T4662, QAP_T4566, QAP_T4567, QAP_T4568, QAP_T4569
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8716 import QAP_T8716
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8718 import QAP_T8718
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8728 import QAP_T8728
from test_framework.configurations.component_configuration import ComponentConfiguration


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"POV - Additional Features | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        # configuration = ComponentConfiguration("Participation")
        configuration = ComponentConfiguration("Scaling")

        QAP_T8716(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8718(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8728(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        # QAP_T4333.execute(report_id)
        # QAP_T4330.execute(report_id)

        # region Needs Refactoring
        # QAP_T4569.execute(report_id)
        # QAP_T4573.execute(report_id)
        # QAP_T4574.execute(report_id)
        # QAP_T4580.execute(report_id)
        # QAP_T4599.execute(report_id)
        # QAP_T4604.execute(report_id)
        # QAP_T4629.execute(report_id)
        # QAP_T4631.execute(report_id)
        # QAP_T4648.execute(report_id)
        # QAP_T4659.execute(report_id)
        # QAP_T4660.execute(report_id)
        # QAP_T4556.execute(report_id)
        # QAP_T4661.execute(report_id)
        # QAP_T4565.execute(report_id)
        # QAP_T4662.execute(report_id)
        # QAP_T4566.execute(report_id)
        # QAP_T4567.execute(report_id)
        # QAP_T4568.execute(report_id)
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()