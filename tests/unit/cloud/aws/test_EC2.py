import os
from unittest                      import TestCase
from osbot_utils.utils.Misc        import flist
from k8_live_servers.Live_Servers  import Live_Servers
from k8_live_servers.cloud.aws.EC2 import EC2


class test_EC2(TestCase):

    def setUp(self) -> None:
        self.server_ip = flist(Live_Servers().icap_aws_ec2()).first()
        self.ec2 = EC2(self.server_ip)
        print()

    def test_ssh_config(self):
        ssh_config = self.ec2.ssh_config()
        assert ssh_config == { 'server' : self.server_ip             ,
                               'ssh_key': os.environ.get('SSH_KEY'  ),
                               'user'   : os.environ.get('SSH_USER' )}

    def test_exec_command(self):
        assert self.ec2.exec_command('uname').get('output').strip() == 'Linux'