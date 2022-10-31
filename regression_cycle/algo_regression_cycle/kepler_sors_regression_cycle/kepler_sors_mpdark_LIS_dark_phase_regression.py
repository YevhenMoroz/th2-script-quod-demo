import logging
from custom import basic_custom_actions as bca
from stubs import Stubs

from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4522 import QAP_T4522
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4587 import QAP_T4587
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4707 import QAP_T4707
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4708 import QAP_T4708
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4710 import QAP_T4710
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4711 import QAP_T4711
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4712 import QAP_T4712
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4713 import QAP_T4713
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4714 import QAP_T4714
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4715 import QAP_T4715
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4716 import QAP_T4716
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4719 import QAP_T4719
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4720 import QAP_T4720
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4721 import QAP_T4721
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4722 import QAP_T4722
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4723 import QAP_T4723
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4725 import QAP_T4725
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4738 import QAP_T4738
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4739 import QAP_T4739
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4521 import QAP_T4521
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4578 import QAP_T4578
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4586 import QAP_T4586
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4589 import QAP_T4589
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4614 import QAP_T4614
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4674 import QAP_T4674
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4675 import QAP_T4675
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4717 import QAP_T4717
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4729 import QAP_T4729
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4741 import QAP_T4741
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4742 import QAP_T4742
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4743 import QAP_T4743
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4744 import QAP_T4744
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4745 import QAP_T4745
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4779 import QAP_T4779
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4780 import QAP_T4780
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4781 import QAP_T4781
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4782 import QAP_T4782
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4784 import QAP_T4784
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4785 import QAP_T4785
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4786 import QAP_T4786
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4789 import QAP_T4789
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4790 import QAP_T4790
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4791 import QAP_T4791
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4792 import QAP_T4792
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4796 import QAP_T4796
from test_framework.configurations.component_configuration import ComponentConfiguration

from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4795 import QAP_T4795
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4794 import QAP_T4794
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4793 import QAP_T4793
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4788 import QAP_T4788
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4787 import QAP_T4787
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4783 import QAP_T4783
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4778 import QAP_T4778
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4777 import QAP_T4777
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4776 import QAP_T4776
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4775 import QAP_T4775
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4774 import QAP_T4774
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4773 import QAP_T4773
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4772 import QAP_T4772
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4770 import QAP_T4770
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4767 import QAP_T4767
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4765 import QAP_T4765
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4764 import QAP_T4764
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4762 import QAP_T4762
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4759 import QAP_T4759
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4746 import QAP_T4746
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4735 import QAP_T4735
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4733 import QAP_T4733
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4732 import QAP_T4732
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4731 import QAP_T4731
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4730 import QAP_T4730
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4724 import QAP_T4724
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4718 import QAP_T4718
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4358 import QAP_T4358
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4156 import QAP_T4156

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)


def test_run(parent_id=None, version=None):
    # Generation id and time for test run
    report_id = bca.create_event(f"MPDark (LIS + Dark phase)" if version is None else f"MPDark (LIS + Dark phase) (verification) | {version}", parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        configuration = ComponentConfiguration("Mp_dark")
        # LIS + DARK
        # region RFQ
        QAP_T4795(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4746(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Child generation - check tags
        QAP_T4794(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4793(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Full Qty: Restated (qty 700k),   child (qty 1 000k)
        QAP_T4788(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4787(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Algo cancels orders
        QAP_T4783(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4778(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Execution (LIS order)
        QAP_T4796(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Part Execution (Dark order)
        QAP_T4614(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4589(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4586(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4587(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Part Execution (LIS order)
        QAP_T4792(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4791(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4790(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4789(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Modification
        QAP_T4786(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4784(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4785(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4780(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Cancelation
        QAP_T4779(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4745(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4744(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4743(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4742(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4741(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

        # region Cancelation
        QAP_T4781(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4782(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()