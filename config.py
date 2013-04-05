"""Configuration options"""
AWS_ACCESS_KEY = "<YOUR_AWS_ACCESS_KEY>"
AWS_SECRET_KEY = "<YOUR_AWS_SECRET_KEY>"
IPINFODB_API_KEY = "<YOUR_INFODB_API_KEY>"

# Don't change anything starting here
AMI_ID = "ami-dac679b3"
AMIS = {'ap-northeast-1':'ami-22ad1223', 
            'ap-southeast-1': 'ami-e88acaba', 
            'eu-west-1': 'ami-c1aaabb5', 
            'sa-east-1': 'ami-c819c0d5', 
            'us-east-1': 'ami-3d4ff254', 
            'us-west-1': 'ami-0d153248', 
            'us-west-2': 'ami-8e109ebe', 
            'ap-southeast-2':'ami-fb8611c1'}
UDAT= """#!/bin/sh
               echo "running" >> /root/output.txt"""