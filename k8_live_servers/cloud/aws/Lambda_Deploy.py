from dotenv import load_dotenv
from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda


class Lambda_Deploy:

    def __init__(self, handler):
        load_dotenv()
        self.deploy_lambda = Deploy_Lambda(handler)

    def invoke(self,params=None):
        return self.deploy_lambda.lambda_invoke(params)

    def lambda_name(self):
        return self.deploy_lambda.lambda_name

    def now(self):
        return self.deploy_lambda.update()

