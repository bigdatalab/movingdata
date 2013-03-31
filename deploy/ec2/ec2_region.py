#
# Represents a single EC2 region
#
# Copyright (c) 2013 by Michael Luckeneder
#


import boto
import sys
import time
import itertools
import boto.ec2
import config
import paramiko
from abstract_region import AbstractRegion


class EC2Region(AbstractRegion):
    """Represents a single EC2 instance in a region"""
    def __init__(self, region, ami):
        """Initialize SSH and regions"""
        self.region, self.ami = region, ami
        self.instance = None
        self.dns = ''
        self.sftp_connected = False
        self.ssh_connected = False
        self.ssh = paramiko.SSHClient()
        # handle SSH certificate problems
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.init_connection()

    def init_connection(self):
        """Connect to the region"""
        self.conn = boto.ec2.connect_to_region(self.region, aws_access_key_id=config.AWS_ACCESS_KEY,
                                               aws_secret_access_key=config.AWS_SECRET_KEY)
        print >> sys.stderr, "Connected to %s" % (self.region)

    def check_state(self):
        """Checks if instance is running"""
        self.instance.update()
        return self.instance.state != u'running'

    def wait_for_running(self):
        """Wait until instance is running"""
        timeout = 1
        print >> sys.stderr, "Waiting for running %s" % (self.region)
        while self.instance.state != u'running':
            time.sleep(timeout)
            # exponential timeout
            timeout *= 2
            print >> sys.stderr, "Timeout %i" % (timeout)
            self.instance.update()

        return True

    def url(self):
        """Returns public URL of instance"""
        if not hasattr(self, 'dns') or not self.dns:
            self.instance.update()
            self.dns = self.instance.public_dns_name
        return self.dns

    def start(self):
        """Starts the instance in the region"""
        if not self.instance:
            reservation = self.conn.run_instances(self.ami, key_name='cs4098', instance_type='t1.micro',
                                                  security_groups=['cs4098'], user_data=config.UDAT)
            self.instance = reservation.instances[0]

        else:
            print >> sys.stderr, "Instance already running"

    def terminate(self):
        """Terminates the instance in the region"""
        if self.instance:
            print >> sys.stderr, "%s terminated" % (self.url())
            self.url = ''
            self.instance.terminate()
            self.instance = None

    def terminate_all(self):
        """Terminates all instances in all regions"""

        # get list of running instances
        instances = list(itertools.chain.from_iterable([res.instances for res in self.conn.get_all_instances()]))
        running_instances = filter(lambda i: i.state == u'running', instances)
        for i in running_instances:
            print >> sys.stderr, "%s terminated" % (i.public_dns_name)
            i.terminate()

    def invoke_ssh(self, cmd):
        """Invoke SSH command on instance in region"""
        self.connect_ssh()

        print >> sys.stderr, "Running command %s on %s" % (cmd, self.url())
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        ret = stdout.readlines()
        res = map(lambda line: line.replace("\n", ""), ret)
        print >> sys.stderr, res

        if res:
            return res[0]
        else:
            return res

    def connect_ssh(self):
        """Connects via SSH to instance"""
        if not self.ssh_connected:
            self.ssh.connect(self.url(), username='ubuntu', timeout=20000)
            self.ssh_connected = True

    def connect_sftp(self):
        """Connects via SFTP to instance"""
        self.connect_ssh()
        if not self.sftp_connected:
            self.sftp = self.ssh.open_sftp()
            self.sftp_connected = True

    def upload_file(self, localfile, remotefile):
        """Uploads file using SFTP to instance"""
        self.connect_sftp()
        self.sftp.put(localfile, remotefile)
