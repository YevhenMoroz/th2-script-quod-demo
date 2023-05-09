import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_PercentageVolume.QAP_T4648 import QAP_T4648
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4225 import QAP_T4225
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4350 import QAP_T4350
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T4351 import QAP_T4351
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8791 import QAP_T8791
from test_cases.algo.Algo_Redburn.Algo_POV.QAP_T8845 import QAP_T8845
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4464 import QAP_T4464
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4470 import QAP_T4470
from test_cases.algo.Algo_Redburn.Algo_POV_Scaling.QAP_T4478 import QAP_T4478
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T11233 import QAP_T11233
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T11234 import QAP_T11234
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T4386 import QAP_T4386
from test_cases.algo.Algo_Redburn.POV_Auction.QAP_T8719 import QAP_T8719
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"POV (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        configuration = ComponentConfigurationAlgo("Participation")

        # region Basic
        QAP_T8791(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4351(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4350(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4470(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4225(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region MinParticipation
        # endregion

        # region MaxParticipation
        # dublicate QAP_T8791(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Would
        QAP_T4648(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region UnderParticipation
        QAP_T8845(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region OverParticipation
        # endregion

        # region Navigator
        # endregion

        # region Auction
        QAP_T4386(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T8719(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11233(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11234(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region POV Scaling
        QAP_T4478(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4464(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()