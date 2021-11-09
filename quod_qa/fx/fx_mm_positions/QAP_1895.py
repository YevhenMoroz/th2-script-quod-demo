import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.win_gui_wrappers.data_set import Side
from quod_qa.win_gui_wrappers.forex.rfq_tile import RFQTile
from stubs import Stubs
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    PositionsInfo, ExtractionPositionsAction

from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


def get_dealing_positions_details(del_act, base_request, symbol, account):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", "Position")
    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return float(response["dealingpositions.position"].replace(",", ""))


def compare_position(case_id, pos_before, position, pos_after):
    expected_pos = pos_before + position

    verifier = Verifier(case_id)
    verifier.set_event_name("Compare position")
    verifier.compare_values("Quote position", str(round(expected_pos, 2)), str(pos_after))

    verifier.verify()


def execute(report_id, session_id):
    pos_service = Stubs.act_fx_dealing_positions

    case_name = Path(__file__).name[:-3]

    # Preconditions
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    client = "ASPECT_DB"
    ccy1 = "EUR"
    ccy2 = "USD"
    venue = "CITI"
    tenor = "Spot"
    symbol = "EUR/USD"
    order_qty = "1000000"
    buy_side = Side.buy.value

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    try:
        # Step 1
        rfq_tile = RFQTile(case_id, case_base_request)
        rfq_tile.crete_tile().modify_rfq_tile(from_cur=ccy1, to_cur=ccy2,
                                              near_qty=order_qty, near_tenor=tenor,
                                              client=client, single_venue=venue)
        rfq_tile.send_rfq()
        pos_before = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        rfq_tile.place_order(side=buy_side)
        # Step 2
        position = float(order_qty)
        position_after = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        compare_position(case_id, pos_before, position, position_after)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            rfq_tile.close_tile()
        except Exception:
            logging.error("Error execution", exc_info=True)
