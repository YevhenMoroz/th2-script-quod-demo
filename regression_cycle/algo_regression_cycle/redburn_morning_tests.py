import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_Redburn.Algo_MOE import EXP_WW_02, EXP_FPC_01, EXP_SCO_01, EXP_LIM_01, EXP_WW_01, EXP_VO_01
from test_cases.algo.Algo_Redburn.Algo_TWAP import QA_TWAP_NAV_WW_01_sell, TWAP_MinP_01, QA_TWAP_NAV_WW_03_buy, TWAP_WW_01, QA_TWAP_NAV_WW_03_sell, QA_TWAP_NAV_WW_REF_01_sell, TWAP_AUC_01, \
    QA_TWAP_NAV_WW_MAXPercentage, QA_TWAP_NAV_WW_01_buy, TWAP_MaxP_01, TWAP_BA_01, QA_TWAP_NAV_WW_02_sell, QA_TWAP_NAV_WW_MAXShares, TWAP_NAV_01, TWAP_NAV_02, QA_TWAP_NAV_WW_REF_01_buy, \
    QA_TWAP_NAV_WW_02_buy
from test_cases.algo.Algo_Redburn.Algo_VWAP import VWAP_MinP_01, VWAP_BA_01, VWAP_AUC_01, VWAP_WW_01, VWAP_MaxP_01, VWAP_NAV_01, VWAP_NAV_02
from test_cases.algo.Algo_Redburn.Algo_POV import POV_AUC_01, POV_BA_01, POV_WW_01, POV_MinMax_01, POV_NAV_02, POV_SCAP_01, POV_NAV_01
from test_cases.algo.Algo_Redburn.Algo_MOO import OPN_SCA_01, QA_OPN_AuctionWouldCapMaxWouldPerc, QA_OPN_Market, QA_OPN_WouldRef, OPN_VO_01, QA_OPN_WouldPercentage, \
    QA_OPN_AuctionWouldCapMaxWouldShares, QA_OPN_InitialSlice_01, QA_OPN_AuctionWouldCap100, OPN_FPC_01, QA_OPN_LIM_PRM, QA_OPN_AuctionWouldCap, QA_OPN_LIM_MKT, OPN_LIM_01, OPN_WW_01, \
    QA_OPN_InitialSlice_02, QA_OPN_LIM_MID, QA_OPN_WouldShares, QA_OPN_InitialSlice_03
from test_cases.algo.Algo_Redburn.Algo_MOC import QA_CLO_InitialSlice_01, CLO_WW_01, QA_CLO_WouldAtLast, CLO_VO_01, QA_CLO_Perc_for_Close90, QA_CLO_Market, CLO_SCO_MKT, QA_CLO_WouldPercentage, \
    CLO_FPC_01, QA_CLO_WouldAtLast2, QA_CLO_WouldShares, QA_CLO_AuctionWouldCap100, CLO_SCO_PRM, QA_CLO_WouldRef_Unavaliable, CLO_LIM_01, QA_CLO_WouldRef, QA_CLO_AuctionWouldCapMaxWouldShares, \
    QA_CLO_AuctionWouldCap, QA_CLO_AuctionWouldCapMaxWouldPerc, CLO_SCO_MID, QA_CLO_InitialSlice_02, QA_CLO_AuctionWouldCap0, QA_CLO_Perc_for_Close100, QA_CLO_AtLast, CLO_SCO_01, \
    QA_CLO_InitialSlice_03, QA_CLO_WouldShares0
from stubs import Stubs

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

timeouts = False
work_dir = Stubs.custom_config['qf_trading_fe_folder']
username = Stubs.custom_config['qf_trading_fe_user']
password = Stubs.custom_config['qf_trading_fe_password']

channels = dict()


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event('Redburn morning tests')
    logger.info(f"Root event was created (id = {report_id.id})")
    try:

        # region TWAP NAV WW
        QA_TWAP_NAV_WW_MAXPercentage.execute(report_id)
        QA_TWAP_NAV_WW_MAXShares.execute(report_id)
        QA_TWAP_NAV_WW_01_sell.execute(report_id)
        QA_TWAP_NAV_WW_02_sell.execute(report_id)
        QA_TWAP_NAV_WW_03_sell.execute(report_id)
        QA_TWAP_NAV_WW_01_buy.execute(report_id)
        QA_TWAP_NAV_WW_02_buy.execute(report_id)
        QA_TWAP_NAV_WW_03_buy.execute(report_id)
        QA_TWAP_NAV_WW_REF_01_buy.execute(report_id)
        QA_TWAP_NAV_WW_REF_01_sell.execute(report_id)
        # endregion

        # region OPN Additional
        QA_OPN_AuctionWouldCap.execute(report_id)
        QA_OPN_AuctionWouldCap100.execute(report_id)
        QA_OPN_AuctionWouldCapMaxWouldPerc.execute(report_id)
        QA_OPN_AuctionWouldCapMaxWouldShares.execute(report_id)
        QA_OPN_InitialSlice_01.execute(report_id)
        QA_OPN_InitialSlice_02.execute(report_id)
        QA_OPN_InitialSlice_03.execute(report_id)
        QA_OPN_WouldPercentage.execute(report_id)
        QA_OPN_WouldRef.execute(report_id)
        QA_OPN_WouldShares.execute(report_id)
        QA_OPN_LIM_MID.execute(report_id)
        QA_OPN_LIM_MKT.execute(report_id)
        QA_OPN_LIM_PRM.execute(report_id)
        QA_OPN_Market.execute(report_id)
        # endregion

        # region CLO Additional
        CLO_SCO_MID.execute(report_id)
        CLO_SCO_MKT.execute(report_id)
        CLO_SCO_PRM.execute(report_id)
        QA_CLO_InitialSlice_01.execute(report_id)
        QA_CLO_InitialSlice_02.execute(report_id)
        QA_CLO_InitialSlice_03.execute(report_id)
        QA_CLO_WouldShares.execute(report_id)
        QA_CLO_WouldPercentage.execute(report_id)
        QA_CLO_WouldRef.execute(report_id)
        QA_CLO_WouldRef_Unavaliable.execute(report_id)
        QA_CLO_Perc_for_Close90.execute(report_id)
        QA_CLO_Perc_for_Close100.execute(report_id)
        QA_CLO_AuctionWouldCap.execute(report_id)
        QA_CLO_AuctionWouldCap100.execute(report_id)
        QA_CLO_AuctionWouldCap0.execute(report_id)
        QA_CLO_AuctionWouldCapMaxWouldPerc.execute(report_id)
        QA_CLO_AuctionWouldCapMaxWouldShares.execute(report_id)
        QA_CLO_WouldAtLast.execute(report_id)
        QA_CLO_WouldAtLast2.execute(report_id)
        QA_CLO_AtLast.execute(report_id)
        QA_CLO_Market.execute(report_id)
        QA_CLO_WouldShares0.execute(report_id)
        # endregion

        # region Expiry Client requirement
        EXP_LIM_01.execute(report_id)
        EXP_VO_01.execute(report_id)
        EXP_WW_01.execute(report_id)
        EXP_WW_02.execute(report_id)
        EXP_FPC_01.execute(report_id)
        EXP_SCO_01.execute(report_id)
        # endregion

        # region TWAP Client requirement
        TWAP_BA_01.execute(report_id)
        TWAP_WW_01.execute(report_id)
        TWAP_NAV_01.execute(report_id)
        TWAP_NAV_02.execute(report_id)
        TWAP_AUC_01.execute(report_id)
        TWAP_MinP_01.execute(report_id)
        TWAP_MaxP_01.execute(report_id)
        # endregion

        # region VWAP Client requirement
        VWAP_BA_01.execute(report_id)
        VWAP_WW_01.execute(report_id)
        VWAP_NAV_01.execute(report_id)
        VWAP_NAV_02.execute(report_id)
        VWAP_AUC_01.execute(report_id)
        VWAP_MinP_01.execute(report_id)
        VWAP_MaxP_01.execute(report_id)
        # endregion

        # region Pov Client requirement
        POV_BA_01.execute(report_id)
        POV_WW_01.execute(report_id)
        POV_NAV_01.execute(report_id)
        POV_NAV_02.execute(report_id)
        POV_AUC_01.execute(report_id)
        POV_MinMax_01.execute(report_id)
        POV_SCAP_01.execute(report_id)
        # endregion

        # region OPN Client
        OPN_FPC_01.execute(report_id)
        OPN_LIM_01.execute(report_id)
        OPN_SCA_01.execute(report_id)
        OPN_VO_01.execute(report_id)
        OPN_WW_01.execute(report_id)
        # endregion

        # region CLO Client
        CLO_FPC_01.execute(report_id)
        CLO_LIM_01.execute(report_id)
        CLO_SCO_01.execute(report_id)
        CLO_VO_01.execute(report_id)
        CLO_WW_01.execute(report_id)
        # endregion

        # region benchmark with Auction
        TWAP_AUC_01.execute(report_id)
        VWAP_AUC_01.execute(report_id)
        POV_AUC_01.execute(report_id)
        # endregion

        # region TWAP NAV WW
        QA_TWAP_NAV_WW_MAXPercentage.execute(report_id)
        QA_TWAP_NAV_WW_MAXShares.execute(report_id)
        QA_TWAP_NAV_WW_01_sell.execute(report_id)
        QA_TWAP_NAV_WW_02_sell.execute(report_id)
        QA_TWAP_NAV_WW_03_sell.execute(report_id)
        QA_TWAP_NAV_WW_01_buy.execute(report_id)
        QA_TWAP_NAV_WW_02_buy.execute(report_id)
        QA_TWAP_NAV_WW_03_buy.execute(report_id)
        QA_TWAP_NAV_WW_REF_01_buy.execute(report_id)
        QA_TWAP_NAV_WW_REF_01_sell.execute(report_id)
        # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
