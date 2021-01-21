from pprint import pprint
from unittest import TestCase

from osbot_aws.apis.Lambda import Lambda

from k8_live_servers.cloud.aws.Lambda_Deploy import Lambda_Deploy
from k8_live_servers.lambdas.hello_world import run


class test_hello_world(TestCase):
    def setUp(self) -> None:
        self.handler     = run
        self.lambda_name = 'k8_live_servers_lambdas_hello_world'
        print()

    def test_invoke_directy(self):
        assert self.handler.__module__.replace('.','_') == self.lambda_name
        assert self.handler({}                )         == 'From lambda code, hello None'
        assert self.handler({'name' : 'world'})         == 'From lambda code, hello world'

    def test_deploy_lambda(self):
        deploy = Lambda_Deploy(self.handler)
        result = deploy.now()
        assert result.get('name'    ) == self.lambda_name
        assert result.get('status'  ) == 'ok'
        assert deploy.invoke({'name':'there'}) == 'From lambda code, hello there'

    def test_invoke_lambda(self):
        assert Lambda(self.lambda_name).invoke() == 'From lambda code, hello None'