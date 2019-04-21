import boto3
import pickle


# Retrieve VPC ID from S3
s3 = boto3.client('s3')
object = s3.get_object(Bucket='vpcparamsbucketipa5360', Key='myVpc001')
serializedObject = object['Body'].read()
vpc = pickle.loads(serializedObject)
vpcid = vpc['vpc_id']
print "Retrieved from S3, VPC-ID = ", vpcid

# Fetch vpc resource based on vpc ID
ec2 = boto3.resource('ec2')
ec2client = ec2.meta.client
vpc = ec2.Vpc(vpcid)

# Delete  security groups
for sg in vpc.security_groups.all():
    if sg.group_name != 'default':
        sg.delete()

# Delete non-default network acls
for netacl in vpc.network_acls.all():
    if not netacl.is_default:
        netacl.delete()

# Detach and delete all gateways associated with the vpc
for gw in vpc.internet_gateways.all():
    vpc.detach_internet_gateway(InternetGatewayId=gw.id)
    gw.delete()

# Delete Subnets
for subnet in vpc.subnets.all():
    for interface in subnet.network_interfaces.all():
        interface.delete()
    subnet.delete()

# Delete all route table associations
for rt in vpc.route_tables.all():
    main = False
    for rta in rt.associations:
        if rta.main:
            main = True
            break
    if not main:
        rt.delete()

# Finally, delete the vpc
ec2client.delete_vpc(VpcId=vpcid)
print "VPC %s deleted successfully!" % vpcid


