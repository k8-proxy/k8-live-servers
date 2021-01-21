from osbot_utils.utils.Misc import split_lines

from k8_kubectl.helpers.to_add_to_sbot.OSBot_Utils__Local import split_spaces
from k8_live_servers.cloud.aws.EC2 import EC2

K8_GW_LOGS_FOLDER = '/run/desktop/mnt/host/c/'

class Server_EC2:
    def __init__(self, server_ip):
        self.ec2 = EC2(server_ip=server_ip)

    def exec_command(self, command):
        return self.ec2.exec_command(command)

    def gw_logs_folder_size(self):
        df_raw  = split_lines(self.ec2.df(K8_GW_LOGS_FOLDER))
        headers = split_spaces(df_raw[0].replace('Mounted on', "Mounted_on"))
        values    = split_spaces(df_raw[1])
        data = {}
        for index, key in enumerate(headers):
            data[key] = values[index]
        return data