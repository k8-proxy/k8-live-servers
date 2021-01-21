from pprint import pprint
from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda

from k8_live_servers.cloud.aws.Lambda_Deploy import Lambda_Deploy
from k8_live_servers.cloud.aws.Lambda_Setup import Lambda_Setup
from k8_live_servers.lambdas.elastic_server_details import run


class test_elastic_server_details(TestCase):
    def setUp(self) -> None:
        self.handler     = run
        self.lambda_name = 'k8_live_servers_lambdas_elastic_server_details'
        print()

    def test_invoke_directy(self):
        assert self.handler.__module__.replace('.','_') == self.lambda_name
        assert self.handler({})   == 'going to send to elastic the server details'

    def test_deploy_lambda(self):
        #Lambda_Setup().upload_packages_to_s3__for_elastic()
        deploy = Lambda_Deploy(self.handler)
        result = deploy.now()

        pprint(deploy.invoke())

        #assert result.get('name'    ) == self.lambda_name
        #assert result.get('status'  ) == 'ok'
        #assert deploy.invoke({'name':'there'}) == 'From lambda code, hello there'

    def test_invoke_lambda(self):
        assert Lambda(self.lambda_name).invoke() == 'From lambda code, hello None'