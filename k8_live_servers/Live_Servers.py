from osbot_utils.utils.Files import path_combine, file_contents
from osbot_utils.utils.Yaml import yaml_load


class Live_Servers:
    def __init__(self):
        self.path_live_servers = path_combine('../../data', 'icap-servers.yaml')

    def icap_aws_ec2(self):
        return self.icap().get('aws-ec2')

    def icap(self):
        return yaml_load(self.path_live_servers)

