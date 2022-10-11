from copy import deepcopy


class VenueSecActNameEntity:
    def __init__(self, list_of_initialization):
        self._levy_fee_exemption = list_of_initialization[0]
        self._per_transac_fee_exemption = list_of_initialization[1]
        self._stamp_fee_exemption = list_of_initialization[2]
        self._venue_account_id_source = list_of_initialization[3]
        self._venue_account_name = list_of_initialization[4]
        self._venue_client_account_name = list_of_initialization[5]
        self._venue_id = list_of_initialization[6]

    def convert_value_to_dict(self):
        return {
            'levyFeeExemption': self._levy_fee_exemption,
            'perTransacFeeExemption': self._per_transac_fee_exemption,
            'stampFeeExemption': self._stamp_fee_exemption,
            'venueAccountIDSource': self._venue_account_id_source,
            'venueAccountName': self._venue_account_name,
            'venueClientAccountName': self._venue_client_account_name,
            'venueID': self._venue_id
        }
