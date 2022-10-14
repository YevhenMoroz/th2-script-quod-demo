import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_TWAP import QAP_T4378, QAP_T4449, QAP_T4281, QAP_T4379, QAP_T4282, QAP_T4424, QAP_T4425, QAP_T4426, QAP_T4427, QAP_T4430, QAP_T4436, QAP_T4437, QAP_T4320, QAP_T4438, QAP_T4439, QAP_T4441, QAP_T4442, QAP_T4443, QAP_T4370, QAP_T4444, QAP_T4372, QAP_T4448, QAP_T4361, QAP_T4380, QAP_T4385, QAP_T4292, QAP_T4303
from test_framework.configurations.component_configuration import ComponentConfiguration
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4297 import QAP_T4297
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4304 import QAP_T4304
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4315 import QAP_T4315
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4319 import QAP_T4319
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4323 import QAP_T4323
from test_cases.algo.Algo_Redburn.Algo_TWAP.QAP_T4324 import QAP_T4324


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"TWAP - Navigator | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Iceberg: Route/Venue
        # configuration = ComponentConfiguration("Twap")
        configuration = ComponentConfiguration("Scaling")
        # QAP_T4872(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        QAP_T4297(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4304(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4315(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4319(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4323(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4324(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()

        QAP_T4303.execute(report_id)

        # region Needs Refactoring
        # QAP_T4378.execute(report_id)
        # QAP_T4449.execute(report_id)
        # QAP_T4281.execute(report_id)
        # QAP_T4379.execute(report_id)
        # QAP_T4282.execute(report_id)
        # QAP_T4424.execute(report_id)
        # QAP_T4425.execute(report_id)
        # QAP_T4426.execute(report_id)
        # QAP_T4427.execute(report_id)
        # QAP_T4430.execute(report_id)
        # QAP_T4436.execute(report_id)
        # QAP_T4437.execute(report_id)
        # QAP_T4320.execute(report_id)
        # QAP_T4438.execute(report_id)
        # QAP_T4439.execute(report_id)
        # QAP_T4441.execute(report_id)
        # QAP_T4442.execute(report_id)
        # QAP_T4443.execute(report_id)
        # QAP_T4370.execute(report_id)
        # QAP_T4444.execute(report_id)
        # QAP_T4372.execute(report_id)
        # QAP_T4448.execute(report_id)
        # QAP_T4361.execute(report_id)
        # QAP_T4380.execute(report_id)
        # QAP_T4385.execute(report_id)
        # QAP_T4292.execute(report_id)
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()