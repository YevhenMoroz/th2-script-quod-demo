from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.win_act_pb2_grpc import HandWinActStub
from grpc_modules.order_book_pb2_grpc import OrderBookServiceStub
from custom.basic_custom_actions import create_event_id
from custom.basic_custom_actions import create_store_event_request
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionInfo
from channels import Channels
from win_gui_modules.wrappers import *


def execute(report_id, session_id):
    event_store = EventStoreServiceStub(Channels.event_store_channel)
    case_name = "QAP-2740 [SORPING] Send SORPING algo order to check PriceCost criteria in Aggressive phase"
    case_id = create_event_id()
    event_store.StoreEvent(request=create_store_event_request(case_name, case_id, report_id))

    set_base(session_id, case_id)

    common_act = HandWinActStub(Channels.ui_act_channel)

    act2 = OrderBookServiceStub(Channels.ui_act_channel)

    order_info_extraction = "getOrderInfo"

    call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.ExecPcy", "ExecPcy"]))
    call(common_act.verifyEntities, verification(
        order_info_extraction, "checking order", [
            verify_ent("Order ExecPcy", "order.ExecPcy", "Synth (Quod LitDark)")
        ])
    )

    # step 2

    call(common_act.getOrderFields, fields_request(order_info_extraction, ["order.status", "Sts"]))
    call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                 [verify_ent("Order Status", "order.status", "Filled")]))

    sub_order1 = ExtractionInfo.from_data(["subOrder1.ExecPcy", "ExecPcy"])
    sub_order2 = ExtractionInfo.from_data(["subOrder2.ExecPcy", "ExecPcy"])
    main_order = ExtractionInfo.from_sub_order_details(OrdersDetails.from_info([sub_order1, sub_order2]))

    sub_order_details = OrdersDetails()
    sub_order_details.set_default_params(get_base_request(session_id, case_id))
    sub_order_details.set_extraction_id("order.subOrder")
    sub_order_details.set_one_extraction_info(main_order)

    call(act2.getOrdersDetails, sub_order_details.request())

    call(common_act.verifyEntities,
         verification("order.subOrder", "checking order",
                      [verify_ent("Order ExecPcy", "subOrder1.ExecPcy", "Synth (Quod MultiListing)")]))

    call(common_act.verifyEntities,
         verification("order.subOrder", "checking order",
                      [verify_ent("Order ExecPcy", "subOrder2.ExecPcy", "Synth (Quod DarkPool)")]))
