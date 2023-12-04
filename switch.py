import os
import time
import argparse
from dotenv import load_dotenv

from ec2 import EC2

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
EC2_INSTANCE = os.environ.get("EC2_INSTANCE")

"""
Describe the command line args and options
"""
parser = argparse.ArgumentParser(description="Start or stop EC2 instance")
parser.add_argument("instance",
                    nargs='?',
                    type=str,
                    help="Instance id, if none is passed, it will try to read from .env file",
                    default=EC2_INSTANCE)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--start", action="store_true", help="Start the instance")
group.add_argument("--stop", action="store_true", help="Stop the instance")
group.add_argument("--state", action='store_true',
                   help="State of the instance")

args = parser.parse_args()

instance = args.instance

if instance is None or instance == '':
    print("No instance ID is set, please pass one in CLI or set in .env file")
    exit(1)

client = EC2(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region=AWS_REGION
)

if args.start:
    response = client.start_instance(instance)
    print("starting, please wait...")
    while response != 'running':
        time.sleep(5)
        response = client.get_state(instance)
elif args.stop:
    response = client.stop_instance(instance)
    print("stopping, please wait...")
    while response != 'stopped':
        time.sleep(5)
        response = client.get_state(instance)
elif args.state:
    response = client.get_state(instance)
else:
    print("Invalid option")
    exit(1)

print(f"✅ {response}")
