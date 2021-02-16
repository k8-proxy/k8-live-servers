import os
from unittest                                import TestCase
from osbot_aws.AWS_Config                    import AWS_Config
from osbot_aws.apis.Lambda                   import Lambda
from osbot_aws.apis.S3                       import S3
from osbot_aws.Dependencies                  import upload_dependency
from osbot_aws.Dependencies                  import pip_install_dependency
from osbot_utils.utils.Misc                  import base64_to_bytes

from k8_live_servers.cloud.aws.Lambda_Deploy import Lambda_Deploy
from k8_live_servers.lambdas.screenshot      import run

class test_screenshot(TestCase):

    def setUp(self) -> None:
        os.environ['PYPPETEER_CHROMIUM_REVISION'] = '800071'
        self.handler                              = run
        self.lambda_name                          = 'k8_live_servers_lambdas_screenshot'

    def test_check_or_upload_dependency(self):
        # Ensure that all the required dependencies are availaible in configured S3 bucket
        dependencies = 'syncer,requests,pyppeteer2,websocket-client'
        for target in dependencies.split(','):
            self.check_or_upload_dependency(target)

    def test_invoke_directy__simple_url(self):
        assert self.handler.__module__.replace('.','_') == self.lambda_name
        png_data = self.handler({'url' : 'https://www.google.com'})

        assert self.save_image(png_data, '/tmp/test.png') is True

    def test_invoke_directly__open_page(self):
        png_data = self.handler({'url'      : 'https://www.google.com',
                                 'headless' : False,
                                 'shutdown' : True})
        assert self.save_image(png_data, '/tmp/test.png') is True

    def test_deploy_lambda(self):
        deploy = Lambda_Deploy(self.handler)
        result = deploy.now()

        assert result.get('State'         ) == 'Active'
        assert result.get('FunctionName'  ) == self.lambda_name
        assert deploy.invoke({'url':'https://www.google.com'})

    def test_invoke_lambda__simple_url(self):
        png_data = Lambda(self.lambda_name).invoke({'url':'https://google.com'})

        assert self.save_image(png_data, '/tmp/test.png') is True

    def test_invoke_lambda__with_delay(self):
        png_data = Lambda(self.lambda_name).invoke({'url'   : 'https://glasswallsolutions.com/',
                                                    'delay' : 1})
        assert self.save_image(png_data, '/tmp/test.png') is True

    @staticmethod
    def save_image( png_data, image_path ):
        try:
            with open(image_path, "wb") as fh:
                fh.write(base64_to_bytes(png_data))
                fh.close()
            return True
        except Exception as error:
            print('invalid base64')
            return False

    @staticmethod
    def check_or_upload_dependency(target):
        s3 = S3()
        s3_bucket = AWS_Config().lambda_s3_bucket()
        s3_key = 'lambdas-dependencies/{0}.zip'.format(target)
        if s3.file_exists(s3_bucket, s3_key) is False:
            assert pip_install_dependency(target) is True
            assert upload_dependency(target)      is True


