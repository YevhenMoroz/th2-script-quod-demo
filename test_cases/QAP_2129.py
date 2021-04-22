import logging
from datetime import datetime
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

# from win_gui_modules.aggregated_rates_wrappers import PlaceRFQRequest, RFQTileOrderSide, ModifyRFQTileRequest
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.client_pricing_wrappers import BaseTileDetails
from win_gui_modules.quote_wrappers import QuoteDetailsRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = Stubs.fix_act
    ar_service = Stubs.win_act_aggregated_rates_service
    common_act = Stubs.win_act
    event_store = Stubs.event_store
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event('QAP-2129', report_id)
    # session_id = set_session_id()
    # set_base(session_id, case_id)
    # base_request = get_base_request(session_id, case_id)
    # base_details = BaseTileDetails(base=base_request)
    #
    # work_dir = Stubs.custom_config['qf_trading_fe_folder_303']
    # password = Stubs.custom_config['qf_trading_fe_password_303']
    # user = Stubs.custom_config['qf_trading_fe_user_303']
    # prepare_fe(case_id, session_id, work_dir, user, password)
    #
    # execution_id = bca.client_orderid(4)
    # qrb = QuoteDetailsRequest(base=base_request)
    # qrb.set_extraction_id(execution_id)
    # qrb.request()

    reusable_params = {
        'Account': case_params['Account'],
        'Side': 1,
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
            },
        'SettlDate': tsd.spo(),
        'SettlType': '0'
        }

    rfq_params_new = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': 0,
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
        }

    rfq_params_expired = {
        'QuoteReqID': bca.client_orderid(9),
        'NoRelatedSymbols': [{
            **reusable_params,
            'Currency': 'EUR',
            'QuoteType': '1',
            'OrderQty': 1000000,
            'OrdType': 'D',
            'ExpireTime': reusable_params['SettlDate'] + '-23:59:00.000',
            'TransactTime': (datetime.utcnow().isoformat())}]
        }

    # execution_id = bca.client_orderid(4)
    # qrb = QuoteDetailsRequest(base=base_request)
    # qrb.set_extraction_id(execution_id)
    # qrb_quote_req_id = ExtractionDetail('quoteRequestBook.id', 'Id')
    # qrb_user = ExtractionDetail('quoteRequestBook.id', 'User')
    # qrb_status = ExtractionDetail('quoteRequestBook.status', 'Status')
    # qrb_quote_status = ExtractionDetail('quoteRequestBook.quotestatus', 'QuoteStatus')
    # qrb.add_extraction_details([qrb_quote_req_id, qrb_user, qrb_status, qrb_quote_status])
    #
    act.placeQuoteFIX(
            bca.convert_to_request(
                    'Send RFQ',
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params_new, case_params['TraderConnectivity'])
                    ))

    act.placeQuoteFIX(
            bca.convert_to_request(
                    'Send RFQ',
                    case_params['TraderConnectivity'],
                    case_id,
                    bca.message_to_grpc('QuoteRequest', rfq_params_expired, case_params['TraderConnectivity'])
                    ))
    #
    # call(ar_service.getQuoteRequestBookDetails, qrb.request())
    # call(common_act.verifyEntities, verification(execution_id, 'checking QRB', [
    #     verify_ent('QRB Id', qrb_quote_req_id.name, rfq_params['QuoteReqID']),
    #     verify_ent('QRB User', qrb_user.name, case_params['TraderConnectivity']),
    #     verify_ent('QRB Status', qrb_status.name, "New"),
    #     # verify_ent('QRB QuoteStatus', qrb_quote_status.name, "")
    # ]))

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
