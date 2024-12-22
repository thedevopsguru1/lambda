import boto3

def lambda_handler(event, context):
    # Specify the AWS region
    region = "us-east-1"  # Change to your preferred region
    ec2_client = boto3.client("ec2", region_name=region)
    
    try:
        # Describe all EC2 instances
        response = ec2_client.describe_instances()
        instances = []
        
        # Collect all instance IDs
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instances.append(instance["InstanceId"])
        
        if instances:
            # Add tags to all instances
            ec2_client.create_tags(
                Resources=instances,
                Tags=[
                    {
                        "Key": "Name",
                        "Value": "yannick"
                    },
                    {"Key": "TEAMS", "Value": "DEVOPS"}
                ]
            )
            return {
                "statusCode": 200,
                "body": f"Successfully tagged {len(instances)} instances with Name: yannick"
            }
        else:
            return {
                "statusCode": 200,
                "body": "No instances found to tag"
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error tagging instances: {str(e)}"
        }
