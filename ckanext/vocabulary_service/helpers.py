def get_vocabulary_service_types():
    return [
        {'text': 'CKAN CSV Resource', 'value': 'ckan_csv'},
        {'text': 'GitHub CSV', 'value': 'github_csv'},
        {'text': 'GSQ VocPrez', 'value': 'vocprez'},
    ]


def get_vocabulary_service_update_frequencies():
    return [
        {'text': 'Daily', 'value': 'daily'},
        {'text': 'Weekly', 'value': 'weekly'},
        {'text': 'Monthly', 'value': 'monthly'},
    ]
