"""
Symbol map for different EC2 status based on AWS documentation. For details,
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html
"""
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
