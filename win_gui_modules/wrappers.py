from th2_grpc_act_gui_quod import act_ui_win_pb2


class BaseParams:
    session_id = None
    event_id = None


def set_base(session_id, event_id):
    BaseParams.session_id = session_id
    BaseParams.event_id = event_id


def fields_request(extraction_id, data):
    request = act_ui_win_pb2.GetOrderFieldsRequest(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
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
    request = act_ui_win_pb2.CheckChildOrderRequest(directOrderDetails=direct)
    request.id = extraction_id

    length = len(data)
    i = 0
    while i < length:
        var = request.child.add()
        var.name = data[i]
        var.colName = data[i + 1]
        i += 2

    return request


def order_analysis_algo_parameters_request(extraction_id: str, param_names: list, filters: dict):
    request = act_ui_win_pb2.GetOrderAnalysisAlgoParametersRequest(sessionID=BaseParams.session_id,
                                                                   parentEventId=BaseParams.event_id)
    request.id = extraction_id
    request.paramNames.extend(param_names)

    for key, value in filters.items():
        request.filter[key] = value

    return request


def create_order_analysis_events_request(extraction_id: str, filters: dict):
    request = act_ui_win_pb2.GetOrderAnalysisEventsRequest(sessionID=BaseParams.session_id,
                                                           parentEventId=BaseParams.event_id)
    request.id = extraction_id

    for key, value in filters.items():
        request.filter[key] = value

    return request


def verify_ent(report_name: str, saved_path: str, actual_value: str):
    return [report_name, saved_path, actual_value]


def verification(actual_extraction_id, verification_name, data):
    request = act_ui_win_pb2.VerificationDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.actualExtractionId = actual_extraction_id
    request.verificationName = verification_name
    for arr in data:
        var = request.fields.add()
        var.printedName = arr[0]
        var.actualPath = arr[1]
        var.expectedValue = arr[2]

    return request


def create_verification_request(verification_name: str, actual_extraction_id: str,
                                expected_extraction_id="") -> act_ui_win_pb2.VerificationDetails:
    request = act_ui_win_pb2.VerificationDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.verificationName = verification_name
    request.actualExtractionId = actual_extraction_id
    request.expectedExtractionId = expected_extraction_id
    return request


def check_value(request: act_ui_win_pb2.VerificationDetails,
                printed_name: str, actual_path: str, expected_value: str,
                method=act_ui_win_pb2.VerificationDetails.VerificationMethod.EQUALS):
    var = request.fields.add()
    var.printedName = printed_name
    var.actualPath = actual_path
    var.expectedValue = expected_value
    var.verificationMethod = method


def compare_values(request: act_ui_win_pb2.VerificationDetails,
                   printed_name: str, actual_path: str, expected_path: str,
                   method=act_ui_win_pb2.VerificationDetails.VerificationMethod.EQUALS):
    var = request.fields.add()
    var.printedName = printed_name
    var.actualPath = actual_path
    var.expectedPath = expected_path
    var.verificationMethod = method

<<<<<<< HEAD
def direct_loc_request(qty_type: str, qty_percentage: str, route: str):
=======

def direct_loc_request(qty_type: str, qty_percentage: str, route: str,
                       direct_values: ExtractDirectsValuesRequest = None):
>>>>>>> ecd4b66ac58b9df6049d87f4cd506ce2c9a3c5ea
    request = act_ui_win_pb2.DirectLocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route

    return request

<<<<<<< HEAD

def direct_moc_request(qty_type: str, qty_percentage: str, route: str):
=======

def direct_child_care(qty_type: str, qty_percentage: str, recipient: str, route: str,
                      direct_values: ExtractDirectsValuesRequest = None):
    request = act_ui_win_pb2.DirectChildCareDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.recipient = recipient
    request.route = route
    request.directsValues.CopyFrom(direct_values)

    return request


def direct_moc_request(qty_type: str, qty_percentage: str, route: str,
                       direct_values: ExtractDirectsValuesRequest = None):
>>>>>>> ecd4b66ac58b9df6049d87f4cd506ce2c9a3c5ea
    request = act_ui_win_pb2.DirectMocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route
<<<<<<< HEAD

    return request


def direct_poc_request(qty_type: str, reference_price: str,  percentage: str, qty_percentage: str, route: str):
    request = act_ui_win_pb2.DirectPocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
=======
    request.directsValues.CopyFrom(direct_values)

    return request


def direct_loc_request_correct(qty_type: str, qty_percentage: str, route: str):
    request = act_ui_win_pb2.DirectLocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route
    return request


def direct_child_care_сorrect(qty_type: str, qty_percentage: str, recipient: str, route: str, count: int):
    request = act_ui_win_pb2.DirectChildCareDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    for i in range(1, count + 1):
        request.selectedRows.append(i)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.recipient = recipient
    request.route = route
    return request


def direct_moc_request_correct(qty_type: str, qty_percentage: str, route: str):
    request = act_ui_win_pb2.DirectMocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
>>>>>>> ecd4b66ac58b9df6049d87f4cd506ce2c9a3c5ea
    request.qtyType = qty_type
    request.referencePrice = reference_price
    request.percentage = percentage
    request.qtyPercentage = qty_percentage
    request.route = route

    return request

def accept_order_request(instr: str, qty: str, limit: str):
    request = act_ui_win_pb2.NewCareOrderDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.instrLookupSymbol = instr
    request.limitPrice = limit
    request.quantity = qty
    return request


def reject_order_request(instr: str, qty: str, limit: str):
    request = act_ui_win_pb2.NewCareOrderDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.instrLookupSymbol = instr
    request.limitPrice = limit
    request.quantity = qty
    return request


def direct_order_request(instr: str, qty: str, limit: str, qty_percent: str):
    request = act_ui_win_pb2.DirectOrderDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.orderDetails.instrLookupSymbol = instr
    request.orderDetails.limitPrice = limit
    request.orderDetails.quantity = qty
    request.qtyPercentage = qty_percent

    return request
