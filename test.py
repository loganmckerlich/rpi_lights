import boto3
import yaml

with open ('config.yml', 'r') as stream:
    config = yaml.safe_load(stream)

ssm = boto3.client(
    "ssm",
    region_name=config["aws_region"],
    aws_access_key_id=config["aws_access_key"],
    aws_secret_access_key=config["aws_secret_key"]) 

def to_aws(ngrok_url):
    response = ssm.put_parameter(
        Name='/traffic-light/ngrok_url',
        Value=ngrok_url,
        Type="String",
        Overwrite=True
    )
    print("PUT RESPONSE")
    print(response)
    print()

to_aws('test')


response = ssm.get_parameter(Name="/traffic-light/ngrok_url")
ws_address = response['Parameter']['Value']
print('GET RESPONSE')
print(response["ResponseMetadata"]["HTTPStatusCode"])