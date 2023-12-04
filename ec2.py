import boto3
import pprint


class EC2:

    def __init__(
            self,
            aws_access_key_id: str,
            aws_secret_access_key: str,
            region: str
    ) -> None:
        self.client = boto3.client(
            'ec2',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region
        )

    def start_instance(self, instance: str) -> str:
        response = self.client.start_instances(InstanceIds=[instance])
        return response['StartingInstances'][0]['CurrentState']['Name']

    def stop_instance(self, instance: str) -> str:
        response = self.client.stop_instances(InstanceIds=[instance])
        return response['StoppingInstances'][0]['CurrentState']['Name']

    def get_state(self, instance: str, verbose: bool = False, full: bool = False) -> str|dict:
        response = self.client.describe_instances(InstanceIds=[instance])

        if full:
            return response

        if not verbose:
            return response['Reservations'][0]['Instances'][0]['State']['Name']

        state = ''
        for instance in response['Reservations'][0]['Instances']:
            state += f"{instance['InstanceId']} - {instance['State']['Name']}"

        return state

    def get_state_and_ip(self, instance) -> (str, str):
        response = self.get_state(instance, full=True)
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        publicIp = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp']
        return state, publicIp
