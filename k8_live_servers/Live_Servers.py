from osbot_utils.utils.Files import path_combine, file_contents
from osbot_utils.utils.Yaml import yaml_load


class Live_Servers:
    def __init__(self):
        self.path_live_servers = path_combine(__file__,'../../data/icap-servers.yaml')

    def icap_aws_ec2(self):
        return self.icap().get('aws-ec2')

    def icap_aws_ec2__list(self):
        data = []
        servers = self.icap_aws_ec2()
        for server_id in servers:
            item = servers[server_id]
            item['server_id'] = server_id
            data.append(item)
        return data

    def icap(self):
        return yaml_load(self.path_live_servers)


