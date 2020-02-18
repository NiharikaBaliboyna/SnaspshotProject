import boto3
import click

session=boto3.Session(profile_name='shoty')
ec2=session.resource('ec2')


def filter_instances(project):
    instances=[]
    if project:
        filters=[{'Name':'tag:Project','Values':[project]}]
        instances=ec2.instances.filter(Filters=filters)
    else:
        instances=ec2.instances.all()
    return instances

@click.group()
def instances():
    """commands for instances"""

@instances.command('list')
@click.option('--project',default=None,help='only instances for this project')
def list_instances(project):
    instances=filter_instances('project')
    for i in instances:
        tags={t['Key']:t['Value']for t in i.tags or []}
        print(','.join((i.id,i.instance_type,i.placement['AvailabilityZone'],i.state['Name'],i.public_dns_name,tags.get('Project','<noproject name>'))))
    return

@instances.command('stop')
@click.option('--project',default=None,help='Only running instances')
def stop_instances(project):
    instances=filter_instances(project)
    for i in instances:
        i.stop()

@instances.command('start')
@click.option('--project',default=None,help="starting instances")
def start_instances(project):
    instances=filter_instances(project)
    for i in instances:
        i.start()

if __name__=='__main__':
    instances()
