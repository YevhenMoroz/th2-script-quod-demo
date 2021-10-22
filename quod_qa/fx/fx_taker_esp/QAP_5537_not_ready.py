import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.wrapper_test.FixMessageNewOrderSingle import FixMessageNewOrderSingle
from quod_qa.wrapper_test.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fix_act = Stubs.fix_act

symbol = 'EUR/USD'
securitytype = 'FXSPOT'
defaultmdsymbol_spo_DB = 'EUR/USD:SPO:REG:DB'
defaultmdsymbol_spo_EBS = 'EUR/USD:SPO:REG:EBS-CITI'
no_md_entries_spo_db = [
    {
        "MDEntryType": "0",
        "QuoteEntryID": "2_EUR/USD_2021100176E27F147A3E1310_Bid1",
        "MDEntryPx": 1.18075,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "2_EUR/USD_2021100176E27F147A3E1310_Offer1",
        "MDEntryPx": 1.18141,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "QuoteEntryID": "2_EUR/USD_2021100176E27F147A3E1310_Bid2",
        "MDEntryPx": 1.18071,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "2_EUR/USD_2021100176E27F147A3E1310_Offer2",
        "MDEntryPx": 1.18145,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]
no_md_entries_spo_ebs = [
    {
        "MDEntryType": "0",
        "QuoteEntryID": "1_EUR/USD_2021100176E27F147A3E1310_Bid1",
        "MDEntryPx": 1.18066,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "1_EUR/USD_2021100176E27F147A3E1310_Offer1",
        "MDEntryPx": 1.18146,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "QuoteEntryID": "1_EUR/USD_2021100176E27F147A3E1310_Bid2",
        "MDEntryPx": 1.18061,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "QuoteEntryID": "1_EUR/USD_2021100176E27F147A3E1310_Offer2",
        "MDEntryPx": 1.18149,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        alias = "fix-fh-q-314-luna"

        # # Send market data to the EBS-CITI venue EUR/USD spot
        # FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_EBS, symbol, securitytype,
        #                            connectivity=alias).prepare_custom_md_spot(
        #     no_md_entries_spo_ebs)). \
        #     send_market_data_spot(even_name_custom='Send Market Data SPOT EBS-CITI')
        # # Send market data to the DB venue EUR/USD spot
        # FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_DB, symbol, securitytype,
        #                            connectivity=alias).prepare_custom_md_spot(
        #     no_md_entries_spo_db)). \
        #     send_market_data_spot(even_name_custom='Send Market Data SPOT DB')

        new_order_single = FixMessageNewOrderSingleAlgoFX().set_default_SOR()
        print('New Order Single parameters: ', new_order_single)
        fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                'Send new order ', 'fix-sell-esp-t-314-stand', case_id,
                bca.message_to_grpc('NewOrderSingle', new_order_single,
                                    'fix-sell-esp-t-314-stand')
            ))







    except Exception as e:
        logging.error('Error execution', exc_info=True)

    finally:
        pass
