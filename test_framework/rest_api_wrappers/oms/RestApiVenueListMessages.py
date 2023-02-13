from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiVenueListMessages(RestApiMessages):
    def __init__(self, data_set: BaseDataSet):
        super().__init__("")
        self.default_venue_list_id = data_set.get_venue_list('test_auto')
        self.default_venue_list_description = 'venue list for test'
        self.default_venue_list_name = 'test_auto'
        self.default_venue_list = {'venueID': 'XETRA'}

    def create_venue_list(self, venue_list_name: str = None, venues: list = None, description: str = None):
        self.message_type = "CreateVenueList"
        list_of_venue = []
        for venue in venues:
            venue_dict = {'venueID': venue}
            list_of_venue.append(venue_dict)
        parameters = {
            "venueListName": venue_list_name,
            "venueListDescription": description,
            "venueListVenue": list_of_venue}
        self.parameters = parameters

    def modify_venue_list(self, venue_list: list = None, venue_list_id: str = None, venue_list_name: list = None,
                          description: str = None):
        self.message_type = "ModifyVenueList"
        list_of_venue = []
        if venue_list is not None:
            for venue in venue_list:
                venue_dict = {'venueID': venue}
                list_of_venue.append(venue_dict)
        else:
            list_of_venue.append(self.default_venue_list)
        parameters = {
            "venueListID": venue_list_id if description is not None else self.default_venue_list_id,
            "venueListName": venue_list_name if venue_list_name is not None else self.default_venue_list_name,
            "venueListDescription": description if description is not None else self.default_venue_list_description,
            "venueListVenue": list_of_venue,
            "alive": "true"}
        self.parameters = parameters

    def set_default_venue_list(self):
        self.message_type = "ModifyVenueList"
        parameters = {
            "venueListID": self.default_venue_list_id,
            "venueListName": self.default_venue_list_name,
            "venueListDescription": self.default_venue_list_description,
            "venueListVenue": [self.default_venue_list],
            "alive": "true"}
        self.parameters = parameters

    def delete_venue_list(self, venue_list_id: str = None):
        self.message_type = "DeleteVenueList"
        parameters = {
            "venueListID": venue_list_id}
        self.parameters = parameters
