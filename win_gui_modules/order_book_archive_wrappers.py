from th2_grpc_act_gui_quod import order_book_archive_pb2


class OrderBookArchiveDetails:
    def __init__(self, base_request=None):
        self.details = order_book_archive_pb2.OrderBookArchiveDetails()
        if base_request is not None:
            self.details.base.CopyFrom(base_request)

    def set_default_params(self, base_request):
        self.details.base.CopyFrom(base_request)

    def set_creation_date_from(self, creation_date_from=None):
        if creation_date_from is not None:
            self.details.creationDateFrom = creation_date_from

    def set_creation_date_until(self, creation_date_until=None):
        if creation_date_until is not None:
            self.details.creationDateUntil = creation_date_until

    def set_client(self, client=None):
        if client is not None:
            self.details.client = client

    def set_side(self, side=None):
        if side is not None:
            self.details.side = side

    def set_status(self, status=None):
        if status is not None:
            self.details.status = status

    def set_execution_policy(self, execution_policy=None):
        if execution_policy is not None:
            self.details.executionPolicy = execution_policy

    def set_security_account(self, security_account=None):
        if security_account is not None:
            self.details.securityAccount = security_account

    def set_instrument_symbol(self, instrument_symbol=None):
        if instrument_symbol is not None:
            self.details.instrumentSymbol = instrument_symbol

    def set_client_order_id(self, client_order_id=None):
        if client_order_id is not None:
            self.details.clientOrderId = client_order_id

    def set_quod_order_id(self, quod_order_id=None):
        if quod_order_id is not None:
            self.details.quodOrderId = quod_order_id

    def set_client_group(self, client_group=None):
        if client_group is not None:
            self.details.clientGroup = client_group

    def set_owner(self, owner=None):
        if owner is not None:
            self.details.owner = owner

    def set_route(self, route=None):
        if route is not None:
            self.details.route = route

    def set_venue(self, venue=None):
        if venue is not None:
            self.details.venue = venue

    def set_security_id_source(self, security_id_source=None):
        if security_id_source is not None:
            self.details.securityIdSource = security_id_source

    def set_security_id(self, security_id=None):
        if security_id is not None:
            self.details.securityId = security_id

    def set_remove_all(self, remove_all: bool = False):
        if remove_all:
            self.details.removeAllButton = remove_all

    def set_filter(self, filter=None):
        if filter is not None:
            self.details.filter.update(filter)

    def set_column_names(self, column_names: list = None):
        if column_names is not None:
            self.details.columnNamesForFilter.extend(column_names)

    def get_row_count(self, get_row_count: bool = False):
        if get_row_count:
            self.details.getRowCount = get_row_count

    def build(self):
        return self.details
