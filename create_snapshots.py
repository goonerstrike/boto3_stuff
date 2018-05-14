############################ Create snapshots and tag
import boto3
region = 'us-gov-west-1'

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    result = ec2.describe_instances(Filters=[{'Name': 'tag-value', 'Values': ['SDE']}])
    for r in result['Reservations']:
        for i in r['Instances']:
            for t in i['Tags']:
                if 'test-' in t['Value']:
                    hostname = t['Value']
            for d in i['BlockDeviceMappings']:
                device = d['DeviceName']
                volume = d['Ebs']['VolumeId']
                desc = "%s %s %s" % (hostname, device, volume)
                print "Creating Snapshot of %s %s %s" % (hostname, device, volume)
                snapshot = ec2.create_snapshot(VolumeId=volume,Description=desc)
                snapid = snapshot['SnapshotId']
                print "The snapshot ID is %s" % (snapid)
                ec2.create_tags(Resources=[snapid], Tags=[{'Key':'Project', 'Value':'SDE'}])
