from th2_grpc_act_gui_quod import bookings_blotter_pb2


class ExtractBookingDataDetails:
    def __init__(self, base_request=None):
        if base_request:
            self.__booking_details = bookings_blotter_pb2.ExtractBookingDataDetails()
            self.__booking_details.base.CopyFrom(base_request)
        else:
            self.__booking_details = bookings_blotter_pb2.ExtractBookingDataDetails()

    def set_default_param(self, base_request):
        self.__booking_details.base.CopyFrom(base_request)

    def set_filter(self, filter_dict: dict):
        self.__booking_details.filter.update(filter_dict)

    def set_extraction_columns(self, list_of_column: list):
        for column in list_of_column:
            self.__booking_details.columnNames.append(column)

    def build(self):
        return self.__booking_details


class ExtractSubLvlDetails:
    def __init__(self):
        self.__extract_sub_level_details = bookings_blotter_pb2.ExtractSubLvlDataDetails()

    def set_sub_level_details(self, booking_details: ExtractBookingDataDetails, tab_name: str,
                              rows_number_in_second_tab: int = 1):
        self.__extract_sub_level_details.rowsNumber = rows_number_in_second_tab
        self.__extract_sub_level_details.tabName = tab_name
        self.__extract_sub_level_details.extractDetails.CopyFrom(booking_details.build())

    def build(self):
        return self.__extract_sub_level_details
