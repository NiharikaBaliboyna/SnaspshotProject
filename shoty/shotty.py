import boto3


session=boto3.Session(profile_name='shoty')
ec2=session.resource('ec2')

def list_instances():
    for i in ec2.instances.all():
        print(','.join((i.id,i.instance_type,i.placement['AvailabilityZone'],i.state['Name'],i.public_dns_name)))
    return
if __name__=='__main__':
    list_instances()
