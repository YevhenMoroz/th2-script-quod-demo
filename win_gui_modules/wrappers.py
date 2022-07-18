from th2_grpc_act_gui_quod import act_ui_win_pb2
from th2_grpc_act_gui_quod.act_ui_win_pb2 import ExtractDirectsValuesRequest


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


def direct_loc_request(qty_type: str, qty_percentage: str, route: str,
                       direct_values: ExtractDirectsValuesRequest = None):
    request = act_ui_win_pb2.DirectLocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route
    request.directsValues.CopyFrom(direct_values)

    return request


def direct_child_care(qty_type: str, qty_percentage: str, recipient: str, route: str, select_rows: list,
                      filter: dict = None, direct_values: ExtractDirectsValuesRequest = None):
    request = act_ui_win_pb2.DirectChildCareDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    if qty_type:
        request.qtyType = qty_type
    if qty_percentage:
        request.qtyPercentage = qty_percentage
    if recipient:
        request.recipient = recipient
    if route:
        request.route = route
    if select_rows:
        request.selectedRows.extend(select_rows)
    if filter:
        request.filter.CopyFrom(client_inbox_filter(filter=filter))
    if direct_values:
        request.directsValues.CopyFrom(direct_values)
    return request


def direct_moc_request(qty_type: str, qty_percentage: str, route: str,
                       direct_values: ExtractDirectsValuesRequest = None):
    request = act_ui_win_pb2.DirectMocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route
    request.directsValues.CopyFrom(direct_values)
    return request


def direct_loc_request_correct(qty_type: str, qty_percentage: str, route: str, filter: dict = None):
    request = act_ui_win_pb2.DirectLocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route
    request.filter.CopyFrom(client_inbox_filter(filter=filter))
    return request


def direct_moc_request_correct(qty_type: str, qty_percentage: str, route: str, filter: dict = None):
    request = act_ui_win_pb2.DirectMocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route
    request.filter.CopyFrom(client_inbox_filter(filter=filter))
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


def direct_order_request(qty_type: str, qty_percentage: str, route: str, filter: dict = None):
    request = act_ui_win_pb2.DirectOrderDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route
    request.filter.CopyFrom(client_inbox_filter(filter=filter))
    return request


def direct_poc_request_correct(qty_type, reference_price, percentage, qty_percentage, route, filter: dict = None):
    request = act_ui_win_pb2.DirectLocDetails(sessionID=BaseParams.session_id, parentEventId=BaseParams.event_id)
    request.qtyType = qty_type
    request.qtyPercentage = qty_percentage
    request.route = route
    request.percentage = percentage
    request.reference_price = reference_price
    request.filter.CopyFrom(client_inbox_filter(filter=filter))
    return request


def client_inbox_filter(base_request=None, filter=None):
    request = act_ui_win_pb2.GridFilter()
    if filter is not None:
        request.filter.update(filter)
    if base_request is not None:
        request.base.CopyFrom(base_request)
    return request
