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

    def start_instance(self, instance_id: str) -> str:
        response = self.client.start_instances(InstanceIds=[instance_id])
        return response['StartingInstances'][0]['CurrentState']['Name']

    def stop_instance(self, instance_id: str) -> str:
        response = self.client.stop_instances(InstanceIds=[instance_id])
        return response['StoppingInstances'][0]['CurrentState']['Name']

    def get_state(self, instance_id: str, verbose: bool = False, full: bool = False) -> str | dict:
        response = self.client.describe_instances(InstanceIds=[instance_id])

        if full:
            return response

        if not verbose:
            return response['Reservations'][0]['Instances'][0]['State']['Name']

        state = ''
        for instance in response['Reservations'][0]['Instances']:
            status = instance['State']['Name']
            # Safely retrieve the public ip
            public_ip = instance.get('NetworkInterfaces', [{}])[0].get(
                'Association', {}).get('PublicIp', 'n/a')
            state += f"{instance_id} - {status} - {public_ip}"

        return state

    def get_state_and_ip(self, instance_id: str) -> (str, str):
        response = self.get_state(instance_id, full=True)
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        # Safely retrieve the public ip
        public_ip = response.get('Reservations', [{}])[0].get('Instances', [{}])[0].get(
            'NetworkInterfaces', [{}])[0].get('Association', {}).get('PublicIp', 'n/a')
        return state, public_ip
