from custom import tenor_settlement_date as tsd

import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    PositionsInfo, ExtractionPositionsAction

from win_gui_modules.utils import prepare_fe_2, get_base_request, call, get_opened_fe
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
    client = "Silver1"
    account = "Silver1_1"
    settle_type = "W1"
    symbol = "EUR/USD"
    currency = "EUR"
    security_type = "FXFWD"
    side = "1"
    order_qty = "1000000"
    settle_date = tsd.wk1()

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    try:
        # Step 1
        pos_before = get_dealing_positions_details(pos_service, case_base_request, symbol, client)

        # Step 2
        rfq = FixClientSellRfq(
            CaseParamsSellRfq(client, case_id, side=side, orderqty=order_qty, symbol=symbol, securitytype=security_type,
                              settldate=settle_date,
                              settltype=settle_type, currency=currency, account=account)). \
            send_request_for_quote(). \
            verify_quote_pending()
        price = rfq.extruct_filed("OfferPx")
        rfq.send_new_order_single(price). \
            verify_order_pending(). \
            verify_order_filled_fwd()

        position = float(order_qty)
        position_after = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        compare_position(case_id, pos_before, position, position_after)

    except Exception:
        logging.error("Error execution", exc_info=True)
