import os
import argparse
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
EC2_INSTANCE = os.environ.get("EC2_INSTANCE")


def create_client():
    return boto3.client(
        'ec2',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )


def start_instances(instances: list):
    client = create_client()
    response = client.start_instances(InstanceIds=instances)
    return response['StartingInstances'][0]['CurrentState']['Name']


def stop_instances(instances: list):
    client = create_client()
    response = client.stop_instances(InstanceIds=instances)
    return response['StoppingInstances'][0]['CurrentState']['Name']

def get_states(instances: list):
    client = create_client()
    response = client.describe_instances(InstanceIds=instances)
    states = ''
    for instance in response['Reservations'][0]['Instances']:
        states += f"{instance['InstanceId']} - {instance['State']['Name']}"
    return states


"""
Describe the command line args and options
"""
parser = argparse.ArgumentParser(description="Start or stop EC2 instances")
parser.add_argument("instances", nargs='*',
                    help="Instance ids, you can pass 0 or more. If none is passed, it will try to read from .env file", default=[EC2_INSTANCE])

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--start", action="store_true", help="Start the instance")
group.add_argument("--stop", action="store_true", help="Stop the instance")
group.add_argument("--state", action='store_true', help="State of the instance")

args = parser.parse_args()

# Filter out invalid string
instances = list(filter(bool, args.instances))

if len(instances) == 0:
    print("No instance ID is set, please pass one in CLI or set in .env file")
    exit(1)

if args.start:
    response = start_instances(instances)
elif args.stop:
    response = stop_instances(instances)
elif args.state:
    response = get_states(instances)
else:
    print("Invalid option")
    exit(1)

print(response)
