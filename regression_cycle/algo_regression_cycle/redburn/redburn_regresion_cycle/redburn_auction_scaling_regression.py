import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10278 import QAP_T10278
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10273 import QAP_T10273
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10976 import QAP_T10976
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10977 import QAP_T10977
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10978 import QAP_T10978
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T11107 import QAP_T11107
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T11113 import QAP_T11113
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T11114 import QAP_T11114
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4149 import QAP_T4149
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4348 import QAP_T4348
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4364 import QAP_T4364
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4390 import QAP_T4390
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4447 import QAP_T4447
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4450 import QAP_T4450
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4451 import QAP_T4451
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4460 import QAP_T4460
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4389 import QAP_T4389
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10476 import QAP_T10476
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4463 import QAP_T4463
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4506 import QAP_T4506
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4507 import QAP_T4507
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4459 import QAP_T4459
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4504 import QAP_T4504
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4505 import QAP_T4505
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4495 import QAP_T4495
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4508 import QAP_T4508
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4509 import QAP_T4509
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10488 import QAP_T10488
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T10489 import QAP_T10489
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4494 import QAP_T4494
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4510 import QAP_T4510
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4511 import QAP_T4511
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4512 import QAP_T4512
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4513 import QAP_T4513
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4514 import QAP_T4514
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4498 import QAP_T4498
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4501 import QAP_T4501
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4388 import QAP_T4388
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4302 import QAP_T4302
from test_cases.algo.Algo_Redburn.Algo_Auction_Scaling.QAP_T4517 import QAP_T4517
from test_framework.configurations.component_configuration import ComponentConfigurationAlgo


logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"Auction - Scaling (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:

        configuration = ComponentConfigurationAlgo("Scaling")
        # region Check Reject
        QAP_T4506(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4507(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4495(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4508(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4509(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4494(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4512(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4513(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4514(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        QAP_T10976(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10977(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10978(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4149(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10278(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10273(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10488(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10489(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4460(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4389(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T10476(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4459(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4504(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4505(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4498(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4501(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4388(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4302(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4511(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4510(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4348(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4463(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4450(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4451(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4390(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4447(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4364(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4517(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11107(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11114(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T11113(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()


    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()