import boto3
import json
import pickle


class VpcResource():
    def __init__(self):
        self.region = None
        self.resource = None
        self.vpc = None
        self.ig = None
        self.public_subnet1 = None
        self.public_subnet2 = None
        self.public_subnet3 = None
        self.private_subnet1 = None
        self.private_subnet2 = None
        self.private_subnet3 = None
        self.public_route_table = None
        self.private_route_table = None
        self.input_params = self.s3_store_retrieve_input_params()


    def s3_store_retrieve_input_params(self):
        s3_resource = boto3.resource('s3')
        s3 = boto3.client('s3')
        inputList = {'Region': 'us-east-1', 'VPC_CIDR': '10.0.0.0/16', 'VPC_NAME': 'STACK_NAME-IPA5360-VPC',
                     'Zone1': 'us-east-1a', 'Zone2': 'us-east-1b', 'Zone3': 'us-east-1c',
                     'IGW_NAME': 'STACK_NAME-IPA5360-InternetGateway',
                     'PublicSubnet1': 'STACK_NAME-IPA5360-public-subnet-1',
                     'PublicSubnet2': 'STACK_NAME-IPA5360-public-subnet-2',
                     'PublicSubnet3': 'STACK_NAME-IPA5360-public-subnet-3',
                     'PrivateSubnet1': 'STACK_NAME-IPA5360-private-subnet-1',
                     'PrivateSubnet2': 'STACK_NAME-IPA5360-private-subnet-2',
                     'PrivateSubnet3': 'STACK_NAME-IPA5360-private-subnet-3',
                     'PublicRouteTable_Name': 'STACK_NAME-IPA5360-public-route-table',
                     'PrivateRouteTable_Name': 'STACK_NAME-IPA5360-private-route-table'}
        serializedListObject = pickle.dumps(inputList)
        s3_resource.create_bucket(Bucket="inputparamsbucketipa5360")
        s3.put_object(Bucket='inputparamsbucketipa5360', Key='myList001', Body=serializedListObject)
        object = s3.get_object(Bucket='inputparamsbucketipa5360', Key='myList001')
        serializedObject = object['Body'].read()
        inputList = pickle.loads(serializedObject)
        return inputList


    def create_resource(self):
        self.resource = boto3.resource('ec2', region_name=self.input_params['Region'])


    def create_configure_vpc(self):
        self.vpc = self.resource.create_vpc(CidrBlock=self.input_params['VPC_CIDR'])
        self.vpc.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['VPC_NAME']}])
        self.vpc.wait_until_available()
        print  "*" * 130 + "\nCreated VPC %s with VPC_ID = %s" % (self.input_params['VPC_NAME'], self.vpc.id)


    def create_attach_gateway(self):
        if not self.vpc:
            print "Please create VPC first before attaching gateway!"
            return
        self.ig = self.resource.create_internet_gateway()
        self.vpc.attach_internet_gateway(InternetGatewayId=self.ig.id)
        self.ig.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['IGW_NAME']}])
        print "Created and attached Internet Gateway %s with ID = %s" \
              % (self.input_params['IGW_NAME'], self.ig.id)


    def create_public_subnets(self):
        print "*" * 130 + "\nCreating public subnets"
        self.public_subnet1 = self.resource.create_subnet(CidrBlock='10.0.1.0/24', VpcId=self.vpc.id,
                                                          AvailabilityZone=self.input_params['Zone1'])
        self.public_subnet1.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['PublicSubnet1']}])
        print "Created %s with ID = %s CIDR = %s and Availability Zone = %s " \
              % (self.input_params['PublicSubnet1'], self.public_subnet1.id, '10.0.1.0/24',self.input_params['Zone1'])

        self.public_subnet2 = self.resource.create_subnet(CidrBlock='10.0.2.0/24', VpcId=self.vpc.id,
                                                          AvailabilityZone=self.input_params['Zone2'])
        self.public_subnet2.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['PublicSubnet2']}])
        print "Created %s with ID = %s CIDR = %s and Availability Zone = %s " \
              % (self.input_params['PublicSubnet2'], self.public_subnet2.id, '10.0.2.0/24',self.input_params['Zone2'])

        self.public_subnet3 = self.resource.create_subnet(CidrBlock='10.0.3.0/24', VpcId=self.vpc.id,
                                                          AvailabilityZone=self.input_params['Zone3'])
        self.public_subnet3.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['PublicSubnet3']}])
        print "Created %s with ID = %s CIDR = %s and Availability Zone = %s " \
              % (self.input_params['PublicSubnet3'], self.public_subnet3.id, '10.0.3.0/24', self.input_params['Zone3'])


    def create_private_subnets(self):
        print "*" * 130 + "\nCreating private subnets"
        self.private_subnet1 = self.resource.create_subnet(CidrBlock='10.0.4.0/24', VpcId=self.vpc.id,
                                                           AvailabilityZone=self.input_params['Zone1'])
        self.private_subnet1.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['PrivateSubnet1']}])
        print "Created %s with ID = %s CIDR = %s and Availability Zone = %s " \
              % (self.input_params['PrivateSubnet1'], self.private_subnet1.id, '10.0.4.0/24',self.input_params['Zone1'])

        self.private_subnet2 = self.resource.create_subnet(CidrBlock='10.0.5.0/24',VpcId=self.vpc.id,
                                                           AvailabilityZone=self.input_params['Zone2'])
        self.private_subnet2.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['PrivateSubnet2']}])
        print "Created %s with ID = %s CIDR = %s and Availability Zone = %s " \
              % (self.input_params['PrivateSubnet2'], self.private_subnet2.id, '10.0.5.0/24',self.input_params['Zone2'])

        self.private_subnet3 = self.resource.create_subnet(CidrBlock='10.0.6.0/24', VpcId=self.vpc.id,
                                                           AvailabilityZone=self.input_params['Zone3'])
        self.private_subnet3.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['PrivateSubnet3']}])
        print "Created %s with ID = %s CIDR = %s and Availability Zone = %s " \
              % (self.input_params['PrivateSubnet3'], self.private_subnet3.id, '10.0.6.0/24', self.input_params['Zone3'])


    def create_public_route_routetable(self):
        self.public_route_table = self.vpc.create_route_table()
        self.public_route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=self.ig.id)
        self.public_route_table.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['PublicRouteTable_Name']}])
        print "*" * 130 + "\nCreated public route table %s with ID = %s " \
              % (self.input_params['PublicRouteTable_Name'], self.public_route_table.id)
        print "Created route to Internet Gateway for traffic to flow in/out!"


    def create_private_route_table(self):
        self.private_route_table = self.vpc.create_route_table()
        self.private_route_table.create_tags(Tags=[{"Key": "Name", "Value": self.input_params['PrivateRouteTable_Name']}])
        print  "*" * 130 + "\nCreated private route table %s with ID = %s " \
              % (self.input_params['PrivateRouteTable_Name'], self.private_route_table.id)


    def attach_public_route_tables_subnets(self):
        self.public_route_table.associate_with_subnet(SubnetId=self.public_subnet1.id)
        self.public_route_table.associate_with_subnet(SubnetId=self.public_subnet2.id)
        self.public_route_table.associate_with_subnet(SubnetId=self.public_subnet3.id)
        print "Attached public route table to all 3 public subnets"


    def attach_private_route_tables_subnets(self):
        self.private_route_table.associate_with_subnet(SubnetId=self.private_subnet1.id)
        self.private_route_table.associate_with_subnet(SubnetId=self.private_subnet2.id)
        self.private_route_table.associate_with_subnet(SubnetId=self.private_subnet3.id)
        print "Attached private route table to all 3 private subnets"



if __name__ == '__main__':
    ec2_resource = VpcResource()
    ec2_resource.create_resource()

    ec2_resource.create_configure_vpc()
    ec2_resource.create_attach_gateway()

    ec2_resource.create_public_subnets()
    ec2_resource.create_private_subnets()

    ec2_resource.create_public_route_routetable()
    ec2_resource.attach_public_route_tables_subnets()

    ec2_resource.create_private_route_table()
    ec2_resource.attach_private_route_tables_subnets()




