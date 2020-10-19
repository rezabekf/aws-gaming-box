import os

import boto3
from botocore import exceptions

gaming_instance_name = os.environ['GAMING_INSTANCE_NAME']
gaming_instance_region = os.environ['GAMING_INSTANCE_REGION']
gaming_instance_size_gb = os.environ['GAMING_INSTANCE_SIZE_GB']

# Connect to region
ec2_client = boto3.client('ec2', region_name=gaming_instance_region)
ec2_resource = boto3.resource('ec2', region_name=gaming_instance_region)


def lambda_handler(event, context):
    # Get all available volumes
    volumes = ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']

    # Get all volumes for the given instance
    volumes_to_delete = []
    for volume in volumes:
        for tag in volume['Tags']:
            if tag['Key'] == 'Name' and tag['Value'] == gaming_instance_name:
                volumes_to_delete.append(volume)

    if len(volumes_to_delete) == 0:
        print('No volumes found. Nothing to do! Aborting...')
        return

    # Create a snapshot of the volumes
    snaps_created = []
    for volume in volumes:
        snap = ec2_client.create_snapshot(VolumeId=volume['VolumeId'])
        snap_id = snap['SnapshotId']
        snap_waiter = ec2_client.get_waiter('snapshot_completed')

        try:
            snap_waiter.wait(SnapshotIds=[snap_id], WaiterConfig={'Delay': 15, 'MaxAttempts': 59})
        except exceptions.WaiterError as e:
            print("Could not create snapshot, aborting")
            print(e.last_response)
            return

        print("Created snapshot: {}".format(snap['SnapshotId']))
        snaps_created.append(snap['SnapshotId'])

    # Tag the snapshots
    if len(snaps_created) > 0:
        ec2_client.create_tags(
            Resources=snaps_created,
            Tags=[
                {'Key': 'SnapAndDelete', 'Value': 'True'},
                {'Key': 'Name', 'Value': gaming_instance_name}
            ]
        )

    # Delete any current AMIs
    images = ec2_client.describe_images(Owners=['self'])['Images']
    for ami in images:
        if ami['Name'] == gaming_instance_name:
            print('Deleting image {}'.format(ami['ImageId']))
            ec2_client.deregister_image(DryRun=False, ImageId=ami['ImageId'])

    # Remove previous snapshots of the volumes
    previous_snapshots = ec2_client.describe_snapshots(Filters=[{'Name': 'tag-key', 'Values': ['SnapAndDelete']}])[
        'Snapshots']
    for snapshot in previous_snapshots:
        if snapshot['SnapshotId'] not in snaps_created:
            print("Removing previous snapshot: {}".format(snapshot['SnapshotId']))
            ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

    # Delete the volumes
    for volume in volumes_to_delete:
        v = ec2_resource.Volume(volume['VolumeId'])
        print("Deleting EBS volume: {}, Size: {} GiB".format(v.id, v.size))
        v.delete()

    # Create a new AMI
    if len(snaps_created) > 0:
        amis_created = []
        ami = ec2_client.register_image(
            Name=gaming_instance_name,
            Description=gaming_instance_name + ' Automatic AMI',
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'DeleteOnTermination': False,
                        'SnapshotId': snaps_created[0],
                        'VolumeSize': int(gaming_instance_size_gb),
                        'VolumeType': 'gp2'
                    }
                },
            ],
            Architecture='x86_64',
            RootDeviceName='/dev/sda1',
            DryRun=False,
            VirtualizationType='hvm',
            SriovNetSupport='simple'
        )
        print('Created image {}'.format(ami['ImageId']))
        amis_created.append(ami['ImageId'])

        if len(amis_created) > 0:
            # Tag the AMI
            ec2_client.create_tags(
                Resources=amis_created,
                Tags=[
                    {'Key': 'SnapAndDelete', 'Value': 'True'},
                    {'Key': 'Name', 'Value': gaming_instance_name}
                ]
            )
