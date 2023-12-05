def get_symbol(response: str) -> str:
    symbol_map = {
        'pending': '🟡',
        'stopping': '🟡',
        'shutting-down': '🔴',
        'terminated': '🔴',
        'stopped': '🟠',
        'running': '🟢',
    }

    return symbol_map.get(response, '🔵')
