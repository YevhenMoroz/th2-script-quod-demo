import logging
import os
from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs

from test_cases.QAP_2864 import simulator
from win_gui_modules.order_book_wrappers import OrdersDetails

from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-2002"
    seconds, nanos = timestamps()  # Store case start time

    # region Declaration
    seconds, nanos = timestamps()  # Store case start time
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = 900
    symbol = "1624"
    client = "CLIENT1"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # endregion

    # region TradeRule
    trade_rule_1 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="CLIENT1", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=qty,
        mask_as_connectivity="fix-bs-eq-paris",
        md_entry_size={0: 1000},
        md_entry_px={40: 30},
        symbol={"XPAR": symbol}))
    # endregion

    # region Create order via FIX
    connectivity = 'gtwquod5'
    fix_manager_qtwquod5 = FixManager(connectivity, case_id)

    fix_params = {
        'Account': client,
        'HandlInst': "1",
        'Side': "1",
        'OrderQty': qty,
        'TimeInForce': 4,
        'OrdType': 1,
        'TransactTime': datetime.utcnow().isoformat(),
        'ExDestination': 'CHIX',
        'Instrument': {
            'Symbol': 'FR0000125007_EUR',
            'SecurityID': 'FR0000125007',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR',

        },
        'Currency': 'EUR',
        'SecurityExchange': 'TRERROR',
    }

    fix_message = FixMessage(fix_params)
    fix_message.add_random_ClOrdID()
    fix_manager_qtwquod5.Send_NewOrderSingle_FixMessage(fix_message)
    Stubs.core.removeRule(trade_rule_1)
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"

    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_tif = ExtractionDetail("order_tif", "TIF")
    order_execSts = ExtractionDetail("oder_execSts", "ExecSts")
    order_ordType = ExtractionDetail("oder_ordType", "OrdType")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_tif,
                                                                                            order_execSts,
                                                                                            order_ordType
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Terminated"),
                                                  verify_ent("Qty", order_qty.name, qty),
                                                  verify_ent("TIF", order_tif.name, "FillOrKill"),
                                                  verify_ent("ExecSts", order_execSts.name, "Filled"),
                                                  verify_ent("OrdType", order_ordType.name, "Market")
                                                  ]))
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
