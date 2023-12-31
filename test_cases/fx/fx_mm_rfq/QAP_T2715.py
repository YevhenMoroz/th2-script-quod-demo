from custom import tenor_settlement_date as tsd
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
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
    expected_pos = pos_before - position

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
    client = "Iridium1"
    account = "Iridium1_1"
    settle_type = "0"
    symbol = "GBP/USD"
    currency = "GBP"
    security_type = "FXSPOT"
    side = "2"
    order_qty = "1000000"
    settle_date = spo()

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    try:
        rfq = FixClientSellRfq(
            CaseParamsSellRfq(client, case_id, side=side, orderqty=order_qty, symbol=symbol, securitytype=security_type,
                              settldate=settle_date,
                              settltype=settle_type, currency=currency, account=account)). \
            send_request_for_quote(). \
            verify_quote_pending()
        price = rfq.extract_filed("BidPx")
        rfq.send_new_order_single(price). \
            verify_order_pending(). \
            verify_order_filled_fwd()
        # Step 1
        pos_before = get_dealing_positions_details(pos_service, case_base_request, symbol, client)

        # Step 2
        rfq = FixClientSellRfq(
            CaseParamsSellRfq(client, case_id, side=side, orderqty=order_qty, symbol=symbol, securitytype=security_type,
                              settldate=settle_date,
                              settltype=settle_type, currency=currency, account=account)). \
            send_request_for_quote(). \
            verify_quote_pending()
        price = rfq.extract_filed("BidPx")
        rfq.send_new_order_single(price). \
            verify_order_pending(). \
            verify_order_filled_fwd()

        position = float(order_qty)
        position_after = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        compare_position(case_id, pos_before, position, position_after)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
