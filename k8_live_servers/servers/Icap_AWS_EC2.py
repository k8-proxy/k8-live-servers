from k8_live_servers.Live_Servers import Live_Servers
from k8_live_servers.elastic.Elastic_Icap import Elastic_Icap


class Icap_AWS_EC2:

    def __init__(self):
        pass

    def elastic_update_server_metadata(self):
        elastic = Elastic_Icap()
        return elastic.add(self.live_servers(), id_key='server_id')

    def live_servers(self):
        return Live_Servers().icap_aws_ec2__list()