from custom import basic_custom_actions as bca


def hierarchical_level_updater(test_id, user_response: list, new_hierarchical_assignment: dict):
    try:
        new_user_parameters = user_response[0]
        user_response_keys = user_response[0].keys()
        institution_id = 'institutionID'
        zone_id = 'zoneID'
        location_id = 'locationID'
        desk_id = 'deskUserRole'

        if institution_id in user_response_keys:
            new_user_parameters.pop(institution_id)
            new_user_parameters.update(new_hierarchical_assignment)
            return new_user_parameters
        elif zone_id in user_response_keys:
            new_user_parameters.pop(zone_id)
            new_user_parameters.update(new_hierarchical_assignment)
            return new_user_parameters
        elif location_id in user_response_keys:
            new_user_parameters.pop(location_id)
            new_user_parameters.update(new_hierarchical_assignment)
            return new_user_parameters
        elif desk_id in user_response_keys:
            new_user_parameters.pop(desk_id)
            new_user_parameters.update(new_hierarchical_assignment)
            return new_user_parameters
        else:
            new_user_parameters.update(new_hierarchical_assignment)
            return new_user_parameters
    except (KeyError, TypeError, IndexError):
        bca.create_event(f'Hierarchical updating step was failed', status='FAILED', parent_id=test_id)