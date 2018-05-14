############################ Delete old snaps
import boto3
from datetime import datetime,timedelta
region = 'us-gov-west-1'

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    now = datetime.now()
    retention = 7
    result = ec2.describe_snapshots(Filters=[{'Name': 'tag-value', 'Values': ['SDE']}])

    for r in result['Snapshots']:
        start_time = r['StartTime'].replace(tzinfo=None)
        snap_id = r['SnapshotId']
        if (now - start_time) > timedelta(retention):
            print r['SnapshotId']
            ec2.delete_snapshot(SnapshotId=snap_id)
