import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.wrapper_test.DataSet import DirectionEnum
from quod_qa.wrapper_test.FixManager import FixManager
from quod_qa.wrapper_test.FixVerifier import FixVerifier
from quod_qa.wrapper_test.forex.FixMessageExecutionReportAlgoFX import FixMessageExecutionReportAlgoFX
from quod_qa.wrapper_test.forex.FixMessageNewOrderSingleAlgoFX import FixMessageNewOrderSingleAlgoFX


alias_fh = "fix-fh-314-luna"
alias_gtw = "fix-sell-esp-t-314-stand"
symbol = 'EUR/USD'
securitytype = 'FXSPOT'
defaultmdsymbol_spo_barx = 'EUR/USD:SPO:REG:BARX'
defaultmdsymbol_spo_citi = 'EUR/USD:SPO:REG:CITI'
no_md_entries_spo_barx = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.18066,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.18146,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]
no_md_entries_spo_citi = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.18075,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDQuoteType": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.18141,
        "MDEntrySize": 1000000,
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
        fix_manager = FixManager(alias_gtw, case_id)
        fix_verifier = FixVerifier(alias_gtw, case_id)

        # Send market data to the BARX venue EUR/USD spot
        # FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_barx, symbol, securitytype,
        #                            connectivity=alias_fh).prepare_custom_md_spot(
        #     no_md_entries_spo_barx)).send_market_data_spot(even_name_custom='Send Market Data SPOT BARX')
        #
        # # Send market data to the CITI venue EUR/USD spot
        # FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo_citi, symbol, securitytype,
        #                            connectivity=alias_fh).prepare_custom_md_spot(
        #     no_md_entries_spo_citi)). \
        #     send_market_data_spot(even_name_custom='Send Market Data SPOT CITI')

        new_order_sor = FixMessageNewOrderSingleAlgoFX().set_default_SOR().change_parameters({'TimeInForce': '3'})
        new_order_sor.add_fields_into_repeating_group('NoStrategyParameters', [
            {'StrategyParameterName': 'LonePassive', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}])

        fix_manager.send_message_and_receive_response(new_order_sor)

        execution_report = FixMessageExecutionReportAlgoFX(new_order_single=new_order_sor)
        fix_verifier.check_fix_message(execution_report)




    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        # md.send_md_unsubscribe()
        pass
