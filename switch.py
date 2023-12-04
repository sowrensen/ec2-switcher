import os
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
parser = argparse.ArgumentParser(description="Start or stop EC2 instances")
parser.add_argument("instances", nargs='*',
                    help="Instance ids, you can pass 0 or more. If none is passed, it will try to read from .env file", default=[EC2_INSTANCE])

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--start", action="store_true", help="Start the instance")
group.add_argument("--stop", action="store_true", help="Stop the instance")
group.add_argument("--state", action='store_true',
                   help="State of the instance")

args = parser.parse_args()

# Filter out invalid string
instances = list(filter(bool, args.instances))

if len(instances) == 0:
    print("No instance ID is set, please pass one in CLI or set in .env file")
    exit(1)

client = EC2(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region=AWS_REGION
)

if args.start:
    response = client.start_instances(instances)
elif args.stop:
    response = client.stop_instances(instances)
elif args.state:
    response = client.get_states(instances)
else:
    print("Invalid option")
    exit(1)

print(response)
