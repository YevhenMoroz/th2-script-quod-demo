import logging
from custom import basic_custom_actions as bca
from test_cases.algo.Algo_Redburn.Algo_MOC import CLO_SCO_MID, CLO_SCO_MKT, CLO_SCO_PRM, QA_CLO_InitialSlice_01, QA_CLO_InitialSlice_02, QA_CLO_InitialSlice_03, QA_CLO_WouldShares, QA_CLO_WouldPercentage, QA_CLO_WouldRef, QA_CLO_WouldRef_Unavaliable, QA_CLO_Perc_for_Close90, QA_CLO_Perc_for_Close100, QA_CLO_AuctionWouldCap, QA_CLO_AuctionWouldCap100, QA_CLO_AuctionWouldCap0, QA_CLO_AuctionWouldCapMaxWouldPerc, QA_CLO_AuctionWouldCapMaxWouldShares, QA_CLO_WouldAtLast, QA_CLO_WouldAtLast2, QA_CLO_AtLast, QA_CLO_Market, QA_CLO_WouldShares0, CLO_FPC_01, CLO_LIM_01, CLO_SCO_01, CLO_VO_01, CLO_WW_01
from test_cases.algo.Algo_Redburn.Algo_MOE import EXP_DMA_01, EXP_LIM_01, EXP_LIM_02_NEX, EXP_LIM_03_NEX, EXP_LIM_04_NEX, EXP_LIM_05_NEX, EXP_LIM_06_NEX, EXP_VO_01, EXP_WW_01, EXP_WW_02, EXP_FPC_01, EXP_SCO_01, EXP_TWAP_01, EXP_VWAP_01, EXP_POV_01
from test_cases.algo.Algo_Redburn.Algo_MOO import QA_OPN_AuctionWouldCap, QA_OPN_AuctionWouldCap100, QA_OPN_AuctionWouldCapMaxWouldPerc, QA_OPN_AuctionWouldCapMaxWouldShares, QA_OPN_InitialSlice_01, QA_OPN_InitialSlice_02, QA_OPN_InitialSlice_03, QA_OPN_WouldPercentage, QA_OPN_WouldRef, QA_OPN_WouldShares, QA_OPN_LIM_MID, QA_OPN_LIM_MKT, QA_OPN_LIM_PRM, QA_OPN_Market, OPN_FPC_01, OPN_LIM_01, OPN_SCA_01, OPN_VO_01, OPN_WW_01
from test_cases.algo.Algo_Redburn.Algo_MOO.Reference import MOO_Reference_CLO, MOO_Reference_DHI, MOO_Reference_DLO, MOO_Reference_LMT, MOO_Reference_LTP, MOO_Reference_MID, MOO_Reference_MKT_Buy, MOO_Reference_MKT_Sell, MOO_Reference_OPN, MOO_Reference_PRM_Buy, MOO_Reference_PRM_Sell
from test_cases.algo.Algo_Redburn.Algo_POV import POV_BA_01, POV_WW_01, POV_NAV_01, POV_NAV_02, POV_AUC_01, POV_MinMax_01, POV_SCAP_01, MULT_POV_BA_01
from test_cases.algo.Algo_Redburn.Algo_TWAP import TWAP_BA_01, TWAP_WW_01, TWAP_NAV_01, TWAP_NAV_02, TWAP_AUC_01, TWAP_MinP_01, TWAP_MaxP_01, MULT_TWAP_BA_01, TWAP_BA_LSE, TWAP_BA_COPENHAGEN, TWAP_BA_DUBLIN, TWAP_BA_HELSINKI, TWAP_BA_LISBON, TWAP_BA_SIX, TWAP_BA_XETRA
from test_cases.algo.Algo_Redburn.Algo_VWAP import VWAP_BA_01, VWAP_WW_01, VWAP_NAV_01, VWAP_NAV_02, VWAP_AUC_01, VWAP_MinP_01, VWAP_MaxP_01, MULT_VWAP_BA_01, VWAP_BA_LSE, VWAP_BA_COPENHAGEN, VWAP_BA_DUBLIN, VWAP_BA_HELSINKI, VWAP_BA_LISBON, VWAP_BA_SIX, VWAP_BA_XETRA, VWAP_STO
from test_cases.algo.Algo_Redburn.MMT_Flags.Amsterdam_XAMS import MMT_TWAP_AUC_LMT_XAMS, MMT_VWAP_AUC_LMT_XAMS, MMT_POV_AUC_LMT_XAMS
from test_cases.algo.Algo_Redburn.MMT_Flags.Athens_XATH import MMT_TWAP_AUC_LMT_XATH, MMT_VWAP_AUC_LMT_XATH, MMT_POV_AUC_LMT_XATH
from test_cases.algo.Algo_Redburn.MMT_Flags.Brussels_XBRU import MMT_TWAP_AUC_LMT_XBRU, MMT_VWAP_AUC_LMT_XBRU, MMT_POV_AUC_LMT_XBRU
from test_cases.algo.Algo_Redburn.MMT_Flags.Budapest_XBUD import MMT_POV_AUC_LMT_XBUD, MMT_TWAP_AUC_LMT_XBUD, MMT_VWAP_AUC_LMT_XBUD
from test_cases.algo.Algo_Redburn.MMT_Flags.Copenhagen_XCSE import MMT_TWAP_AUC_LMT_XCSE, MMT_VWAP_AUC_LMT_XCSE, MMT_POV_AUC_LMT_XCSE
from test_cases.algo.Algo_Redburn.MMT_Flags.Dublin_XDUB import MMT_TWAP_AUC_LMT_XDUB, MMT_VWAP_AUC_LMT_XDUB, MMT_POV_AUC_LMT_XDUB
from test_cases.algo.Algo_Redburn.MMT_Flags.Helsinki_XHEL import MMT_TWAP_AUC_LMT_XHEL, MMT_VWAP_AUC_LMT_XHEL, MMT_POV_AUC_LMT_XHEL
from test_cases.algo.Algo_Redburn.MMT_Flags.Lisbon_XLIS import MMT_TWAP_AUC_LMT_XLIS, MMT_VWAP_AUC_LMT_XLIS, MMT_POV_AUC_LMT_XLIS
from test_cases.algo.Algo_Redburn.MMT_Flags.Oslo_XOSL import MMT_TWAP_AUC_LMT_XOSL, MMT_VWAP_AUC_LMT_XOSL, MMT_POV_AUC_LMT_XOSL
from test_cases.algo.Algo_Redburn.MMT_Flags.Paris_XPAR import MMT_TWAP_AUC_LMT_XPAR, MMT_VWAP_AUC_LMT_XPAR, MMT_POV_AUC_LMT_XPAR
from test_cases.algo.Algo_Redburn.MMT_Flags.Prag_XPRA import MMT_POV_AUC_LMT_XPRA, MMT_TWAP_AUC_LMT_XPRA, MMT_VWAP_AUC_LMT_XPRA
from test_cases.algo.Algo_Redburn.MMT_Flags.Stockholm_XSTO import MMT_TWAP_AUC_LMT_XSTO, MMT_VWAP_AUC_LMT_XSTO, MMT_POV_AUC_LMT_XSTO
from test_cases.algo.Algo_Redburn.MMT_Flags.Wiener_Boerse_XWBO import MMT_VWAP_AUC_LMT_XWBO, MMT_POV_AUC_LMT_XWBO, MMT_TWAP_AUC_LMT_XWBO
from stubs import Stubs
from test_cases.algo.Algo_Redburn.Many_Venues import MULT_BA_01
from test_cases.algo.Algo_Redburn.Many_Venues.MOC import MOC_AMS, MOC_ATH, MOC_BRU, MOC_COP, MOC_DUB, MOC_HEL, MOC_LIS, MOC_LSE, MOC_MIL, MOC_OSL, MOC_XET, MOC_WIE, MOC_STO, MOC_SIX, MOC_PAR
from test_cases.algo.Algo_Redburn.Many_Venues.MOO import MOO_AMS, MOO_ATH, MOO_BRU, MOO_COP, MOO_DUB, MOO_HEL, MOO_LIS, MOO_LSE, MOO_MIL, MOO_OSL, MOO_XET, MOO_WIE, MOO_STO, MOO_SIX, MOO_PAR
from test_cases.algo.Algo_Redburn.Market_Orders import MOO_MKT_LSE, MOC_MKT_LSE, MOC_MKT_MIL, MOO_MKT_SIX, MOO_MKT_MIL, \
    MOC_MKT_SIX, TWAP_AUC_MKT_LSE, TWAP_AUC_MKT_SIX, TWAP_AUC_MKT_XETRA, VWAP_AUC_MKT_LSE, VWAP_AUC_MKT_SIX, \
    VWAP_AUC_MKT_XETRA, POV_AUC_MKT_LSE, POV_AUC_MKT_SIX, POV_AUC_MKT_XETRA
from test_cases.algo.Algo_Redburn.AuctionVolumeCheck import VOL_POV_AUC_LMT_LSE, VOL_POV_AUC_LMT_MILAN, VOL_POV_AUC_LMT_XETRA, VOL_POV_AUC_MKT_LSE, VOL_POV_AUC_MKT_MILAN, VOL_POV_AUC_MKT_XETRA, VOL_TWAP_AUC_LMT_LSE, VOL_TWAP_AUC_LMT_MILAN, VOL_TWAP_AUC_LMT_XETRA, VOL_TWAP_AUC_MKT_LSE, VOL_TWAP_AUC_MKT_MILAN, VOL_TWAP_AUC_MKT_XETRA, VOL_VWAP_AUC_LMT_LSE, VOL_VWAP_AUC_LMT_MILAN, VOL_VWAP_AUC_LMT_XETRA, VOL_VWAP_AUC_MKT_LSE, VOL_VWAP_AUC_MKT_MILAN, VOL_VWAP_AUC_MKT_XETRA

logging.basicConfig(format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.WARN)

channels = dict()


def test_run():
    # Generation id and time for test run
    logging.getLogger().setLevel(logging.WARN)
    report_id = bca.create_event('Redburn morning tests')
    logger.info(f"Root event was created (id = {report_id.id})")
    try:
        # region Calums venues

        # #AMSTERDAM
        # MOO_AMS.execute(report_id)
        # MOC_AMS.execute(report_id)
        # #ATHENS
        # MOO_ATH.execute(report_id)
        # MOC_ATH.execute(report_id)
        # #BRUSSELS
        # MOO_BRU.execute(report_id)
        # MOC_BRU.execute(report_id)
        # #COPENHAGEN
        # MOO_COP.execute(report_id)
        # MOC_COP.execute(report_id)
        # #DUBLIN
        # MOO_DUB.execute(report_id)
        # MOC_DUB.execute(report_id)
        # #HELSINKI
        # MOO_HEL.execute(report_id)
        # MOC_HEL.execute(report_id)
        # #LISBON
        # MOO_LIS.execute(report_id)
        # MOC_LIS.execute(report_id)
        # #LSE
        # MOO_LSE.execute(report_id)
        # MOC_LSE.execute(report_id)
        # # #MADRID
        # # MOO_MAD.execute(report_id)
        # # MOC_MAD.execute(report_id)
        # #MILAN
        # MOO_MIL.execute(report_id)
        # MOC_MIL.execute(report_id)
        # #OSLO
        # MOO_OSL.execute(report_id)
        # MOC_OSL.execute(report_id)
        # #PARIS
        # MOO_PAR.execute(report_id)
        # MOC_PAR.execute(report_id)
        # #SIX
        # MOO_SIX.execute(report_id)
        # MOC_SIX.execute(report_id)
        # #STOCKHOLM
        # MOO_STO.execute(report_id)
        # MOC_STO.execute(report_id)
        # #WIENER
        # MOO_WIE.execute(report_id)
        # MOC_WIE.execute(report_id)
        # #XETRA
        # MOO_XET.execute(report_id)
        # MOC_XET.execute(report_id)
        # #endregion
        #
        # # region Reference
        # MOO_Reference_CLO.execute(report_id)
        # MOO_Reference_DHI.execute(report_id)
        # MOO_Reference_DLO.execute(report_id)
        # MOO_Reference_LMT.execute(report_id)
        # MOO_Reference_LTP.execute(report_id)
        # MOO_Reference_MID.execute(report_id)
        # MOO_Reference_MKT_Buy.execute(report_id)
        # MOO_Reference_MKT_Sell.execute(report_id)
        # MOO_Reference_OPN.execute(report_id)
        # MOO_Reference_PRM_Buy.execute(report_id)
        # MOO_Reference_PRM_Sell.execute(report_id)
        # # end region
        #
        # # region OPN Additional
        # QA_OPN_AuctionWouldCap.execute(report_id)
        # QA_OPN_AuctionWouldCap100.execute(report_id)
        # QA_OPN_AuctionWouldCapMaxWouldPerc.execute(report_id)
        # QA_OPN_AuctionWouldCapMaxWouldShares.execute(report_id)
        # QA_OPN_InitialSlice_01.execute(report_id)
        # QA_OPN_InitialSlice_02.execute(report_id)
        # QA_OPN_InitialSlice_03.execute(report_id)
        # QA_OPN_WouldPercentage.execute(report_id)
        # QA_OPN_WouldRef.execute(report_id)
        # QA_OPN_WouldShares.execute(report_id)
        # QA_OPN_LIM_MID.execute(report_id)
        # QA_OPN_LIM_MKT.execute(report_id)
        # QA_OPN_LIM_PRM.execute(report_id)
        # QA_OPN_Market.execute(report_id)
        # # endregion
        #
        # # region CLO Additional
        # CLO_SCO_MID.execute(report_id)
        # CLO_SCO_MKT.execute(report_id)
        # CLO_SCO_PRM.execute(report_id)
        # QA_CLO_InitialSlice_01.execute(report_id)
        # QA_CLO_InitialSlice_02.execute(report_id)
        # QA_CLO_InitialSlice_03.execute(report_id)
        # QA_CLO_WouldShares.execute(report_id)
        # QA_CLO_WouldPercentage.execute(report_id)
        # QA_CLO_WouldRef.execute(report_id)
        # QA_CLO_WouldRef_Unavaliable.execute(report_id)
        # QA_CLO_Perc_for_Close90.execute(report_id)
        # QA_CLO_Perc_for_Close100.execute(report_id)
        # QA_CLO_AuctionWouldCap.execute(report_id)
        # QA_CLO_AuctionWouldCap100.execute(report_id)
        # QA_CLO_AuctionWouldCap0.execute(report_id)
        # QA_CLO_AuctionWouldCapMaxWouldPerc.execute(report_id)
        # QA_CLO_AuctionWouldCapMaxWouldShares.execute(report_id)
        # QA_CLO_WouldAtLast.execute(report_id)
        # QA_CLO_WouldAtLast2.execute(report_id)
        # QA_CLO_AtLast.execute(report_id)
        # QA_CLO_Market.execute(report_id)
        # QA_CLO_WouldShares0.execute(report_id)
        # # endregion
        #
        # # region Expiry Client ralgouirement
        # EXP_DMA_01.execute(report_id)
        # EXP_LIM_01.execute(report_id)
        # EXP_LIM_02_NEX.execute(report_id)
        # EXP_LIM_03_NEX.execute(report_id)
        # EXP_LIM_04_NEX.execute(report_id)
        # EXP_LIM_05_NEX.execute(report_id)
        # EXP_LIM_06_NEX.execute(report_id)
        # EXP_VO_01.execute(report_id)
        # EXP_WW_01.execute(report_id)
        # EXP_WW_02.execute(report_id)
        # EXP_FPC_01.execute(report_id)
        # EXP_SCO_01.execute(report_id)
        # EXP_TWAP_01.execute(report_id)
        # EXP_VWAP_01.execute(report_id)
        # EXP_POV_01.execute(report_id)
        # # endregion

        # region TWAP Client ralgouirement
        TWAP_BA_01.execute(report_id)
        TWAP_WW_01.execute(report_id)
        TWAP_NAV_01.execute(report_id)
        TWAP_NAV_02.execute(report_id)
        TWAP_AUC_01.execute(report_id)
        TWAP_MinP_01.execute(report_id)
        TWAP_MaxP_01.execute(report_id)
        # endregion

        # region VWAP Client ralgouirement
        VWAP_BA_01.execute(report_id)
        VWAP_WW_01.execute(report_id)
        VWAP_NAV_01.execute(report_id)
        VWAP_NAV_02.execute(report_id)
        VWAP_AUC_01.execute(report_id)
        VWAP_MinP_01.execute(report_id)
        VWAP_MaxP_01.execute(report_id)
        # endregion

        # region Pov Client ralgouirement
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

        # region Multilisting Benchmark orders
        MULT_TWAP_BA_01.execute(report_id)
        MULT_VWAP_BA_01.execute(report_id)
        MULT_POV_BA_01.execute(report_id)
        MULT_BA_01.execute(report_id)
        # endregion

        # # region Calum's orders with Forbidden venues
        # TWAP_BA_LSE.execute(report_id)
        # VWAP_BA_LSE.execute(report_id)
        # TWAP_BA_COPENHAGEN.execute(report_id)
        # VWAP_BA_COPENHAGEN.execute(report_id)
        # TWAP_BA_DUBLIN.execute(report_id)
        # VWAP_BA_DUBLIN.execute(report_id)
        # TWAP_BA_HELSINKI.execute(report_id)
        # VWAP_BA_HELSINKI.execute(report_id)
        # TWAP_BA_LISBON.execute(report_id)
        # VWAP_BA_LISBON.execute(report_id)
        # TWAP_BA_SIX.execute(report_id)
        # VWAP_BA_SIX.execute(report_id)
        # TWAP_BA_XETRA.execute(report_id)
        # VWAP_BA_XETRA.execute(report_id)
        # VWAP_STO.execute(report_id)
        # # endregion

        # # region Market price checks PDAT-1875QA
        # # Auctions
        # MOO_MKT_LSE.execute(report_id)
        # MOO_MKT_SIX.execute(report_id)
        # MOO_MKT_MIL.execute(report_id)
        #
        # MOC_MKT_LSE.execute(report_id)
        # MOC_MKT_SIX.execute(report_id)
        # MOC_MKT_MIL.execute(report_id)
        #
        # # Benchmarks + Auc + Forbidden venues
        # TWAP_AUC_MKT_LSE.execute(report_id)
        # TWAP_AUC_MKT_SIX.execute(report_id)
        # TWAP_AUC_MKT_XETRA.execute(report_id)
        #
        # VWAP_AUC_MKT_LSE.execute(report_id)
        # VWAP_AUC_MKT_SIX.execute(report_id)
        # VWAP_AUC_MKT_XETRA.execute(report_id)
        #
        # POV_AUC_MKT_LSE.execute(report_id)
        # POV_AUC_MKT_SIX.execute(report_id)
        # POV_AUC_MKT_XETRA.execute(report_id)
        # # endregion

        # # region Auction market volume check
        # VOL_POV_AUC_LMT_LSE.execute(report_id)
        # VOL_POV_AUC_LMT_MILAN.execute(report_id)
        # VOL_POV_AUC_LMT_XETRA.execute(report_id)
        # VOL_POV_AUC_MKT_LSE.execute(report_id)
        # VOL_POV_AUC_MKT_MILAN.execute(report_id)
        # VOL_POV_AUC_MKT_XETRA.execute(report_id)
        # VOL_TWAP_AUC_LMT_LSE.execute(report_id)
        # VOL_TWAP_AUC_LMT_MILAN.execute(report_id)
        # VOL_TWAP_AUC_LMT_XETRA.execute(report_id)
        # VOL_TWAP_AUC_MKT_LSE.execute(report_id)
        # VOL_TWAP_AUC_MKT_MILAN.execute(report_id)
        # VOL_TWAP_AUC_MKT_XETRA.execute(report_id)
        # VOL_VWAP_AUC_LMT_LSE.execute(report_id)
        # VOL_VWAP_AUC_LMT_MILAN.execute(report_id)
        # VOL_VWAP_AUC_LMT_XETRA.execute(report_id)
        # VOL_VWAP_AUC_MKT_LSE.execute(report_id)
        # VOL_VWAP_AUC_MKT_MILAN.execute(report_id)
        # VOL_VWAP_AUC_MKT_XETRA.execute(report_id)
        # # endregion

        # # region MMT flags
        #
        # # region Wiener Boerse
        # MMT_TWAP_AUC_LMT_XWBO.execute(report_id)
        # MMT_VWAP_AUC_LMT_XWBO.execute(report_id)
        # MMT_POV_AUC_LMT_XWBO.execute(report_id)
        # # endregion
        #
        # # region Budapest
        # MMT_TWAP_AUC_LMT_XBUD.execute(report_id)
        # MMT_VWAP_AUC_LMT_XBUD.execute(report_id)
        # MMT_POV_AUC_LMT_XBUD.execute(report_id)
        # # endregion
        #
        # # region Prag
        # MMT_TWAP_AUC_LMT_XPRA.execute(report_id)
        # MMT_VWAP_AUC_LMT_XPRA.execute(report_id)
        # MMT_POV_AUC_LMT_XPRA.execute(report_id)
        # # endregion
        #
        # # region Paris
        # MMT_TWAP_AUC_LMT_XPAR.execute(report_id)
        # MMT_VWAP_AUC_LMT_XPAR.execute(report_id)
        # MMT_POV_AUC_LMT_XPAR.execute(report_id)
        # # endregion
        #
        # # region Amsterdam
        # MMT_TWAP_AUC_LMT_XAMS.execute(report_id)
        # MMT_VWAP_AUC_LMT_XAMS.execute(report_id)
        # MMT_POV_AUC_LMT_XAMS.execute(report_id)
        # # endregion
        #
        # # region Lisbon
        # MMT_TWAP_AUC_LMT_XLIS.execute(report_id)
        # MMT_VWAP_AUC_LMT_XLIS.execute(report_id)
        # MMT_POV_AUC_LMT_XLIS.execute(report_id)
        # # endregion
        #
        # # region Brussels
        # MMT_TWAP_AUC_LMT_XBRU.execute(report_id)
        # MMT_VWAP_AUC_LMT_XBRU.execute(report_id)
        # MMT_POV_AUC_LMT_XBRU.execute(report_id)
        # # endregion
        #
        # # region Dublin
        # MMT_TWAP_AUC_LMT_XDUB.execute(report_id)
        # MMT_VWAP_AUC_LMT_XDUB.execute(report_id)
        # MMT_POV_AUC_LMT_XDUB.execute(report_id)
        # # endregion
        #
        # # region Oslo
        # MMT_TWAP_AUC_LMT_XOSL.execute(report_id)
        # MMT_VWAP_AUC_LMT_XOSL.execute(report_id)
        # MMT_POV_AUC_LMT_XOSL.execute(report_id)
        # # endregion
        #
        # # region Copenhagen
        # MMT_TWAP_AUC_LMT_XCSE.execute(report_id)
        # MMT_VWAP_AUC_LMT_XCSE.execute(report_id)
        # MMT_POV_AUC_LMT_XCSE.execute(report_id)
        # # endregion
        #
        # region Helsinki
        MMT_TWAP_AUC_LMT_XHEL.execute(report_id)
        MMT_VWAP_AUC_LMT_XHEL.execute(report_id)
        MMT_POV_AUC_LMT_XHEL.execute(report_id)
        # endregion
        #
        # # region Stockholm
        # MMT_TWAP_AUC_LMT_XSTO.execute(report_id)
        # MMT_VWAP_AUC_LMT_XSTO.execute(report_id)
        # MMT_POV_AUC_LMT_XSTO.execute(report_id)
        # # endregion
        #
        # # region Athens
        # MMT_TWAP_AUC_LMT_XATH.execute(report_id)
        # MMT_VWAP_AUC_LMT_XATH.execute(report_id)
        # MMT_POV_AUC_LMT_XATH.execute(report_id)
        # # endregion
        #
        # # endregion


        # # region TWAP NAV WW
        # QA_TWAP_NAV_WW_MAXPercentage.execute(report_id)
        # QA_TWAP_NAV_WW_MAXShares.execute(report_id)
        # QA_TWAP_NAV_WW_01_sell.execute(report_id)
        # QA_TWAP_NAV_WW_02_sell.execute(report_id)
        # QA_TWAP_NAV_WW_03_sell.execute(report_id)
        # QA_TWAP_NAV_WW_01_buy.execute(report_id)
        # QA_TWAP_NAV_WW_02_buy.execute(report_id)
        # QA_TWAP_NAV_WW_03_buy.execute(report_id)
        # QA_TWAP_NAV_WW_REF_01_buy.execute(report_id)
        # QA_TWAP_NAV_WW_REF_01_sell.execute(report_id)
        # # endregion

    except Exception:
        # bca.create_event('Fail test event', status='FAILED', parent_id=parent_id)
        logging.error("Error execution", exc_info=True)


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
    Stubs.factory.close()
