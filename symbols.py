def get_symbol(response: str) -> str:
    status_mapping = {
        'pending': '🟡',
        'stopping': '🟡',
        'shutting-down': '🔴',
        'terminated': '🔴',
        'stopped': '🟠',
        'running': '🟢',
    }

    return status_mapping.get(response, '🔵')
