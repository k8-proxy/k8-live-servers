import os

from osbot_aws.Dependencies import load_dependency, load_dependencies
from osbot_aws.apis.S3 import S3
from osbot_utils.utils.Files import Files
from osbot_utils.utils.Json import json_dumps




def run(event, context=None):
    load_dependencies('elasticsearch,requests')
    from k8_live_servers.elastic.Elastic_Icap import Elastic_Icap
    return Elastic_Icap().index().info()

    return 'going to send to elastic the server details'