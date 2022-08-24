import logging
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4586 import QAP_T4586
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4589 import QAP_T4589
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4614 import QAP_T4614
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4741 import QAP_T4741
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4742 import QAP_T4742
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4743 import QAP_T4743
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4744 import QAP_T4744
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4745 import QAP_T4745
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4779 import QAP_T4779
from test_cases.algo.Algo_Kepler.Algo_MPDark.QAP_T4780 import QAP_T4780
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


def test_run(parent_id=None):
    # Generation id and time for test run
    report_id = bca.create_event('MPDark', parent_id)
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region MP Dark (Dark Phase Only)
        configuration = ComponentConfiguration("mp_dark")
        QAP_T4777(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4776(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4775(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4774(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4773(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4772(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4770(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4767(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4765(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4764(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4762(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4759(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4735(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4733(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4732(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4731(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4730(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4156(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

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

        # region MP Dark (other)
        QAP_T4724(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4718(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        QAP_T4358(report_id=report_id, data_set=configuration.data_set, environment=configuration.environment).execute()
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()