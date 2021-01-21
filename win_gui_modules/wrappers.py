from th2_grpc_act_gui_quod.act_ui_win_pb2 import GetOrderFieldsRequest, CheckChildOrderRequest, \
    GetOrderAnalysisAlgoParametersRequest, GetOrderAnalysisEventsRequest, \
    VerificationDetails, NewCareOrderDetails, DirectOrderDetails


class BaseParams:
    session_id = None
    event_id = None


def set_base(session_id, event_id):
    BaseParams.session_id = session_id
    BaseParams.event_id = event_id


def fields_request(extraction_id, data):
    request = GetOrderFieldsRequest(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.id = extraction_id

    length = len(data)
    i = 0
    while i < length:
        var = request.details.add()
        var.name = data[i]
        var.colName = data[i + 1]
        i += 2

    return request


def child_fields_request(extraction_id, data, direct):
    request = CheckChildOrderRequest(directOrderDetails=direct)
    request.id = extraction_id

    length = len(data)
    i = 0
    while i < length:
        var = request.child.add()
        var.name = data[i]
        var.colName = data[i + 1]
        i += 2

    return request


def order_analysis_algo_parameters_request(extraction_id, data, filter):
    request = GetOrderAnalysisAlgoParametersRequest(sessionID=BaseParams.session_id,
                                                                parentEventId=BaseParams.event_id)
    request.id = extraction_id

    length = len(data)
    i = 0
    while i < length:
        var = request.details.add()
        var.name = data[i]
        var.paramName = data[i + 1]
        i += 2

    length = len(filter)
    i = 0
    while i < length:
        request.filter[filter[i]] = filter[i + 1]
        i += 2

    return request


def create_order_analysis_events_request(extraction_id: str, filters: dict):
    request = GetOrderAnalysisEventsRequest(sessionID=BaseParams.session_id,
                                                        parentEventId=BaseParams.event_id)
    request.id = extraction_id

    for key, value in filters.items():
        request.filter[key] = value

    return request


def verify_ent(report_name:str, saved_path:str, actual_value:str):
    return [report_name, saved_path, actual_value]


def verification(extraction_id, verification_name, data):
    request = VerificationDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.actualExtractionId = extraction_id
    request.verificationName = verification_name
    for arr in data:
        var = request.fields.add()
        var.printedName = arr[0]
        var.actualPath = arr[1]
        var.expectedValue = arr[2]

    return request


def accept_order_request(instr: str, qty: str, limit: str):
    request = NewCareOrderDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.instrLookupSymbol = instr
    request.limitPrice = limit
    request.quantity = qty

    return request


def direct_order_request(instr: str, qty: str, limit: str, qty_percent: str):
    request = DirectOrderDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.orderDetails.instrLookupSymbol = instr
    request.orderDetails.limitPrice = limit
    request.orderDetails.quantity = qty
    request.qtyPercentage = qty_percent

    return request

