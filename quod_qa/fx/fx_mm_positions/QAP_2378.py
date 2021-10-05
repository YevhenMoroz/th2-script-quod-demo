import logging
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import ndf_spo_front_end, ndf_wk2_front_end
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest

from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    PositionsInfo, ExtractionPositionsAction
from win_gui_modules.utils import prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def place_order_buy(base_request, service, qty, slippage, client):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_quantity(qty)
    place_request.set_slippage(slippage)
    place_request.set_client(client)
    place_request.buy()
    call(service.placeRatesTileOrder, place_request.build())


def get_dealing_positions_details(del_act, base_request, symbol, account, date):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", "Position")

    sub_settle_date = ExtractionPositionsFieldsDetails("sub_positions.settldate", "Settle Date")
    lvl1_info = PositionsInfo.create(
        action=ExtractionPositionsAction.create_extraction_action(
            extraction_details=[sub_settle_date]))
    lvl1_details = GetOrdersDetailsRequest.create(info=lvl1_info)
    lvl1_details.set_filter(["Settle Date", date])

    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position]),
            positions_by_currency=lvl1_details))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return float(response["dealingpositions.position"].replace(",", ""))


def compare_position(case_id, pos_before, qty, pos_after):
    expected_pos = pos_before + float(qty)

    verifier = Verifier(case_id)
    verifier.set_event_name("Compare position")
    verifier.compare_values("Quote position", str(expected_pos), str(pos_after))

    verifier.verify()


def compare_position_quod(case_id, pos_before, qty, pos_after):
    expected_pos = pos_before - float(qty)

    verifier = Verifier(case_id)
    verifier.set_event_name("Compare position")
    verifier.compare_values("Quote position", str(expected_pos), str(pos_after))

    verifier.verify()


def execute(report_id, session_id):
    cp_service = Stubs.win_act_cp_service
    pos_service = Stubs.act_fx_dealing_positions

    case_name = Path(__file__).name[:-3]

    client_tier = "Argentum"
    instrument_spot = "USD/CAD-SPOT"
    instrument_2w = "USD/CAD-2W"
    client = "SILVER1"
    quod_client = "QUOD_1"
    symbol = instrument_spot[:7]
    slippage = "2"
    qty_6m = "6000000"
    date_spo = ndf_spo_front_end()
    date_spo = datetime.strptime(date_spo, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
    date_wk2 = ndf_wk2_front_end()
    date_wk2 = datetime.strptime(date_wk2, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        pos_before = get_dealing_positions_details(pos_service, case_base_request, symbol, client, date_spo)
        pos_before_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, quod_client, date_spo)
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument_spot, client_tier)
        place_order_buy(base_details, cp_service, qty_6m, slippage, client)
        # Step 2
        pos_after_6m = get_dealing_positions_details(pos_service, case_base_request, symbol, client, date_spo)
        pos_after_6m_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, quod_client, date_spo)
        # Step 3
        compare_position(case_id, pos_before, qty_6m, pos_after_6m)
        compare_position_quod(case_id, pos_before_quod, qty_6m, pos_after_6m_quod)
        # Step 4
        modify_rates_tile(base_details, cp_service, instrument_2w, client_tier)
        place_order_buy(base_details, cp_service, qty_6m, slippage, client)

        pos_after_2wk = get_dealing_positions_details(pos_service, case_base_request, symbol, client, date_wk2)
        pos_after_2wk_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, quod_client,
                                                           date_spo)

        compare_position(case_id, pos_after_6m, qty_6m, pos_after_2wk)
        compare_position_quod(case_id, pos_after_6m_quod, qty_6m, pos_after_2wk_quod)


    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
