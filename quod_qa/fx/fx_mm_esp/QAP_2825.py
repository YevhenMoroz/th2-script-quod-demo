import logging
from pathlib import Path
from custom.verifier import Verifier, VerificationMethod
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, ExtractRatesTileValues, SelectRowsRequest, \
    ExtractRatesTileTableValuesRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from datetime import datetime
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp

# FIX_data
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Silver1'
connectivity = 'fix-ss-esp-314-luna-standard'
settltype = '0'
symbol = 'EUR/USD'
securitytype = 'FXSPOT'
securityidsource = '8'
securityid = 'EUR/USD'
bands = [1000000, 2000000, 3000000]
md = None
settldate = tsd.spo()


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client_tier):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client_tier)
    call(service.modifyRatesTile, modify_request.build())


def modify_spread(base_request, service, pips):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_pips(pips)
    modify_request.widen_spread()
    call(service.modifyRatesTile, modify_request.build())


def select_row(base_request, service, rows):
    modify_request = SelectRowsRequest(details=base_request)
    modify_request.set_row_numbers(rows)
    call(service.selectRows, modify_request.build())


def use_default(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_use_defaults()
    call(service.modifyRatesTile, modify_request.build())


def check_ask(base_request, service):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    ask = float(response["rates_tile.ask_large"] + response["rates_tile.ask_pips"])
    return float(ask)


def check_price_from_row(base_request, service, row):
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    response = call(service.extractRateTileValues, extract_value_request.build())
    ask_large = response["rates_tile.ask_large"]

    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_row_number(row)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askPx", "Px"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidPx", "Px"))
    response_px = call(service.extractRatesTileTableValues, extract_table_request.build())
    ask_px = response_px["rateTile.askPx"]
    return ask_large + ask_px


def compare_prices(case_id, ask_before, ask_after):
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices not equal")
    verifier.compare_values("Price ask", str(ask_before), str(ask_after))
    verifier.verify()


def compare_prices_not_equal(case_id, ask_before, ask_after):
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices not equal")
    verifier.compare_values("Price ask", str(ask_before), str(ask_after), VerificationMethod.NOT_EQUALS)
    verifier.verify()


def compare_prices_from_fix_not_eq(case_id, ask_before, ask_after):
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices not equal Fix ")
    verifier.compare_values("Price", str(ask_before), str(ask_after), VerificationMethod.NOT_EQUALS)
    verifier.verify()


def compare_prices_from_fix_eq(case_id, ask_before, ask_after):
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare prices equal Fix")
    verifier.compare_values("Price", str(ask_before), str(ask_after))
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    simulator = Stubs.simulator
    act = Stubs.fix_act

    cp_service = Stubs.win_act_cp_service

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "EUR/USD-Spot"
    client_tier = "Silver"
    pips = "20"
    mdu_params_spo = {
        "MDReqID": simulator.getMDRefIDForConnection314(
            request=RequestMDRefID(
                symbol="EUR/USD:SPO:REG:HSBC",
                connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
        },
        "NoMDEntries": [
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.19597,
                "MDEntrySize": 22000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.19609,
                "MDEntrySize": 22000000,
                "MDEntryPositionNo": 1,
                'SettlDate': tsd.spo(),
                "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
            },
        ]
    }
    try:
        # Step 1
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, 'fix-fh-314-luna')
            ))
        params = CaseParamsSellEsp(connectivity, client, case_id, settltype=settltype, settldate=settldate,
                                   symbol=symbol, securitytype=securitytype, securityidsource=securityidsource,
                                   securityid=securityid)
        md = FixClientSellEsp(params)
        params.prepare_md_for_verification(bands)
        md.send_md_request()
        md.verify_md_pending()
        price1 = md.extract_filed('price')
        md.send_md_unsubscribe()

        # Step 2
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        ask_before = check_ask(base_details, cp_service)
        line_2_before = check_price_from_row(base_details, cp_service, 2)
        compare_prices_from_fix_eq(case_id, price1, ask_before)
        # Step 3
        select_row(base_details, cp_service, [1])
        modify_spread(base_details, cp_service, pips)
        ask_after = check_ask(base_details, cp_service)
        line_2_after = check_price_from_row(base_details, cp_service, 2)
        compare_prices_not_equal(case_id, ask_before, ask_after)
        compare_prices(case_id, line_2_before, line_2_after)
        # Step 3
        params = CaseParamsSellEsp(connectivity, client, case_id, settltype=settltype, settldate=settldate,
                                   symbol=symbol, securitytype=securitytype, securityidsource=securityidsource,
                                   securityid=securityid)
        md2 = FixClientSellEsp(params)
        bands2 = [2000000, 3000000, 1000000]
        params.prepare_md_for_verification(bands2)
        md2.send_md_request()
        md2.verify_md_pending()
        price2 = md2.extract_filed('price', 5)
        # Step 4
        compare_prices_from_fix_not_eq(case_id, price1, price2)
        compare_prices_from_fix_eq(case_id, ask_after, price2)
        # Step 5
        # Use default
        use_default(base_details, cp_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
            md2.send_md_unsubscribe()
        except Exception:
            logging.error("Error execution", exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)