from grpc_modules import win_act_pb2


class BaseParams:
    session_id = None
    event_id = None


def set_base(session_id, event_id):
    BaseParams.session_id = session_id
    BaseParams.event_id = event_id


def fields_request(extraction_id, data):
    request = win_act_pb2.GetOrderFieldsRequest(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
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
    request = win_act_pb2.CheckChildOrderRequest(directOrderDetails=direct)
    request.id = extraction_id

    length = len(data)
    i = 0
    while i < length:
        var = request.child.add()
        var.name = data[i]
        var.colName = data[i + 1]
        i += 2

    return request


def order_analysis_algo_parameters_request(extraction_id, data):
    request = win_act_pb2.GetOrderAnalysisAlgoParametersRequest(sessionID=BaseParams.session_id,
                                                                parentEventId=BaseParams.event_id)
    request.id = extraction_id

    length = len(data)
    i = 0
    while i < length:
        var = request.details.add()
        var.name = data[i]
        var.paramName = data[i + 1]
        i += 2

    return request


def verify_ent(report_name:str, saved_path:str, actual_value:str):
    return [report_name, saved_path, actual_value]


def verification(extraction_id, verification_name, data):
    request = win_act_pb2.VerificationDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.extractionId = extraction_id
    request.verificationName = verification_name
    for arr in data:
        var = request.fields.add()
        var.printedName = arr[0]
        var.actualPath = arr[1]
        var.expectedValue = arr[2]

    return request


def accept_order_request(instr: str, qty: str, limit: str):
    request = win_act_pb2.NewCareOrderDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.instrLookupSymbol = instr
    request.limitPrice = limit
    request.quantity = qty

    return request


def direct_order_request(instr: str, qty: str, limit: str, qty_percent: str):
    request = win_act_pb2.DirectOrderDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.orderDetails.instrLookupSymbol = instr
    request.orderDetails.limitPrice = limit
    request.orderDetails.quantity = qty
    request.qtyPercentage = qty_percent

    return request

