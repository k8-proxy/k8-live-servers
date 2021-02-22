import os

from dotenv                         import load_dotenv
from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda


class Lambda_Deploy:

    def __init__(self, handler):
        load_dotenv()
        self.deploy_lambda                            = Deploy_Lambda(handler)
        self.deploy_lambda.package.aws_lambda.runtime = 'python3.7'

    def configure_environment_variables(self):
        vars_to_add   = ['OSBOT_LAMBDA_S3_BUCKET', 'ELASTIC_SERVER', 'ELASTIC_PORT', 'ELASTIC_USERNAME', 'ELASTIC_PASSWORD']
        env_variables = {}
        for var_to_add in vars_to_add:
            env_variables[var_to_add] = os.environ.get(var_to_add)

        return self.update_environment_variables(env_variables)

    def update_environment_variables(self, env_variables):
        aws_lambda               = self.deploy_lambda.package.aws_lambda
        aws_lambda.env_variables = env_variables
        return aws_lambda.update_lambda_configuration()

    def invoke(self,params=None):
        return self.deploy_lambda.lambda_invoke(params)

    def lambda_name(self):
        return self.deploy_lambda.lambda_name

    def now(self):
        self.deploy_lambda.package.add_osbot_utils()
        self.deploy_lambda.package.add_module('osbot_aws')
        self.deploy_lambda.package.add_module('osbot_elastic')
        self.deploy_lambda.package.add_module('osbot_browser')
        self.deploy_lambda.update()
        return self.configure_environment_variables()
