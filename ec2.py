import boto3


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

    def start_instances(self, instances: list) -> str:
        response = self.client.start_instances(InstanceIds=instances)
        return response['StartingInstances'][0]['CurrentState']['Name']

    def stop_instances(self, instances: list) -> str:
        response = self.client.stop_instances(InstanceIds=instances)
        return response['StoppingInstances'][0]['CurrentState']['Name']

    def get_states(self, instances: list) -> str:
        response = self.client.describe_instances(InstanceIds=instances)
        states = ''
        for instance in response['Reservations'][0]['Instances']:
            states += f"{instance['InstanceId']} - {instance['State']['Name']}"
        return states
