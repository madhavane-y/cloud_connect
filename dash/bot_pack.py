import boto3


class instance:
    reg=''
    api=''
    sec=''
    sess=''
    req=''
    count=1
    def __init__(self,iam,api,sec):
        self.reg=iam
        self.api=api
        self.sec=sec
        self.sess = boto3.session.Session(aws_access_key_id=self.api,aws_secret_access_key=self.sec,region_name=self.reg)
    

    def display(self):
        print(self.reg,self.api,self.sec)

    def set_alarm(self,iid):
        # Create CloudWatch client
        cloudwatch = self.sess.client('cloudwatch')

        for id in iid:
        # Create alarm with actions enabled
            cloudwatch.put_metric_alarm(
                AlarmName='Web_Server_CPU_Utilization',
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=1,
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Period=60,
                Statistic='Average',
                Threshold=80.0,
                ActionsEnabled=True,
                AlarmActions=[
                'arn:aws:swf:'+self.reg+':{CUSTOMER_ACCOUNT}:action/actions/AWS_EC2.InstanceId.Reboot/1.0'
                ],
                AlarmDescription='Alarm when server CPU exceeds 80%',
                Dimensions=[
                    {
                    'Name': 'InstanceId',
                    'Value': id,
                    },
                ],
                Unit='Seconds'
            )

    # def auto_sp(self):

    def create_instance(self,image):
        
        ec2 = self.sess.resource('ec2')

        # VPC
        vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
        vpc.create_tags(Tags=[{"Key":"Name","Value":"Custom VPC"}])
        vpc.wait_until_available()

        # Internet gateway
        ig = ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)

        ###############################################################################################
                                                # ROUTE TABLE CREATION
        ###############################################################################################

        # Route table Private
        route_pri = vpc.create_route_table()
        route_pr = route_pri.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig.id
        )

        # Route table public
        route_pub = vpc.create_route_table()
        route_p = route_pub.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig.id
        )
        
        ###############################################################################################
                                                # SUBNET WITH ROUTE TABLE
        ###############################################################################################
        # private subnet
        subnet_pr = ec2.create_subnet(CidrBlock='10.0.1.0/24',VpcId=vpc.id)

        route_pri.associate_with_subnet(SubnetId=subnet_pr.id)

        # Public subnet
        subnet_p = ec2.create_subnet(CidrBlock='10.0.0.0/24',VpcId=vpc.id)
        
        route_pub.associate_with_subnet(SubnetId=subnet_p.id)

        ################################################################################################
                                            # Public security group
        ################################################################################################


        # security group
        sec_grp_public = ec2.create_security_group(GroupName='1', Description='Public sec grp', VpcId=vpc.id)
        
        sec_grp_public.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=80,ToPort=80)
        sec_grp_public.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=443,ToPort=443)
        sec_grp_public.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=3389,ToPort=3389)
        sec_grp_public.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=22,ToPort=22)

        # instances = ec2.create_instances(ImageId='ami-835b4efa', InstanceType='t2.micro', MaxCount=1, MinCount=1,NetworkInterfaces=[{'SubnetId': subnet_p.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_group.group_id]}])

        ################################################################################################
                                            # Private Security Group
        ################################################################################################


        sec_grp_private = ec2.create_security_group(GroupName='2', Description='Private sec grp', VpcId=vpc.id)
        
        sec_grp_private.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=22,ToPort=22)
        sec_grp_private.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=3389,ToPort=3389)
        sec_grp_private.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=1403,ToPort=1403)
        sec_grp_private.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=3306,ToPort=3306)


        ################################################################################################
                                            # Create Load balancer
        ################################################################################################

        # client = self.sess.client('elbv2')
        # lb = client.create_load_balancer(
        #     Name='webLoadBalancer',
        #     Subnets=[subnet_p.id,subnet_pr.id],
        #     Scheme='internet-facing',
        # )
        # lb_id = lb.id


        ################################################################################################
                                            # Create web server
        ################################################################################################


        if('ubuntu'==image):
            instances = ec2.create_instances(ImageId='ami-0d773a3b7bb2bb1c1', InstanceType='t2.micro', MaxCount=1, MinCount=1,NetworkInterfaces=[{'SubnetId': subnet_p.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_grp_public.group_id]}])
            instances = ec2.create_instances(ImageId='ami-0d773a3b7bb2bb1c1', InstanceType='t2.micro', MaxCount=1, MinCount=1,NetworkInterfaces=[{'SubnetId': subnet_p.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_grp_public.group_id]}])

        elif ('redhat'==image):
            instances = ec2.create_instances(ImageId='ami-5b673c34', InstanceType='t2.micro', MaxCount=1, MinCount=1,NetworkInterfaces=[{'SubnetId': subnet_p.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_grp_public.group_id]}])
            instances = ec2.create_instances(ImageId='ami-5b673c34', InstanceType='t2.micro', MaxCount=1, MinCount=1,NetworkInterfaces=[{'SubnetId': subnet_p.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_grp_public.group_id]}])

        elif ('windows'==image):
            instances = ec2.create_instances(ImageId='ami-07e6b11175e3fa715', InstanceType='t2.micro', MaxCount=1, MinCount=1,NetworkInterfaces=[{'SubnetId': subnet_p.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_grp_public.group_id]}])
            instances = ec2.create_instances(ImageId='ami-07e6b11175e3fa715', InstanceType='t2.micro', MaxCount=1, MinCount=1,NetworkInterfaces=[{'SubnetId': subnet_p.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sec_grp_public.group_id]}])


        ################################################################################################
                                            # Create Database server
        ################################################################################################


        db = self.sess.client('rds')

        # db_subnet = db.create_db_subnet_group(
        #     DBSubnetGroupName='dbsubnet',
        #     DBSubnetGroupDescription='this is db subnet',
        #     SubnetIds=[
        #         subnet_pr.id,
        #     ]
        # )
        inst = db.create_db_instance(
            DBName='database1',
            DBInstanceIdentifier='a'+str(self.count),
            DBInstanceClass='db.t2.micro',
            Engine='mysql',
            MasterUsername='root',
            MasterUserPassword='a12345678',
            # DBSubnetGroupName='dbsubnet',
            AllocatedStorage=22,
        )
        self.count+=1

        # i_id = [instances.id]+[inst.id]
        # self.set_alarm(i_id)

        return

    def list_inst(self):
        cli = self.sess.resource('ec2')
        inst = cli.instances.all()
        return inst

if __name__ == "__main__":
    api = ''
    secret = ''
    region = '  '

    ins = instance(region,api,secret)
    # ins.create_instance()
    print(ins.list_inst())