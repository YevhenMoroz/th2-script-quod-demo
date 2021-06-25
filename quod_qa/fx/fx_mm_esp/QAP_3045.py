import logging
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileTableValuesRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instrument)
    call(service.modifyRatesTile, modify_request.build())


def check_margins(base_request, service, case_id, row, base):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askBase", "Base"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidBase", "Base"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check base margins")
    verifier.compare_values("Base", base, response["rateTile.askBase"])
    verifier.verify()


no_md_entries = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19597,
        "MDEntrySize": 200000,
        "MDEntryPositionNo": 1,
        "SettlDate": spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19609,
        "MDEntrySize": 200000,
        "MDEntryPositionNo": 1,
        "SettlDate": spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19594,
        "MDEntrySize": 6000000,
        "MDEntryPositionNo": 2,
        "SettlDate": spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19612,
        "MDEntrySize": 6000000,
        "MDEntryPositionNo": 2,
        "SettlDate": spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19591,
        "MDEntrySize": 1200000000,
        "MDEntryPositionNo": 3,
        "SettlDate": spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19615,
        "MDEntrySize": 1200000000,
        "MDEntryPositionNo": 3,
        "SettlDate": spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    instrument = "EUR/GBP-SPOT"
    client_tier = "Silver"

    default_md_symbol_spo = "EUR/GBP:SPO:REG:HSBC"
    symbol = "EUR/GBP"
    security_type_spo = "FXSPOT"

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        params = CaseParamsBuy(case_id, default_md_symbol_spo, symbol, security_type_spo)
        params.prepare_custom_md_spot(no_md_entries)
        FixClientBuy(params).send_market_data_spot()
        check_margins(base_details, cp_service, case_id, 1, "0.1")
        check_margins(base_details, cp_service, case_id, 2, "0")


    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
