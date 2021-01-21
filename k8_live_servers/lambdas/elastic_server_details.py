import json

from osbot_aws.Dependencies import load_dependencies
from osbot_utils.utils.Json import json_dumps


def run(event, context=None):
    load_dependencies('elasticsearch,requests')
    from k8_live_servers.elastic.Elastic_Icap import Elastic_Icap

    return json.dumps(list(Elastic_Icap().index().data()))

