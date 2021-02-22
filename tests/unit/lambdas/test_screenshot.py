from unittest                                    import TestCase
from osbot_aws.AWS_Config                        import AWS_Config
from osbot_aws.apis.Lambda                       import Lambda
from osbot_aws.apis.S3                           import S3
from osbot_aws.Dependencies                      import upload_dependency
from osbot_aws.Dependencies                      import pip_install_dependency
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper

from k8_live_servers.cloud.aws.Lambda_Deploy     import Lambda_Deploy
from k8_live_servers.lambdas.screenshot          import run

class test_screenshot(TestCase):

    def setUp(self) -> None:
        self.handler                              = run
        self.lambda_name                          = 'k8_live_servers_lambdas_screenshot'

    def test_check_or_upload_dependency(self):
        dependencies = 'syncer,requests,pyppeteer2,websocket-client'
        for target in dependencies.split(','):
            self.check_or_upload_dependency(target)

    def test_invoke_directy__simple_url(self):
        assert self.handler.__module__.replace('.','_') == self.lambda_name
        png_data                                        = self.handler({'url' : 'https://github.com'})

        assert Browser_Lamdba_Helper().save_png_data(png_data).__contains__("Png data with size")

    def test_invoke_directly__open_page(self):
        payload  = {'url'      : 'https://www.google.com',
                    'headless' : False}
        png_data = self.handler(payload)

        assert Browser_Lamdba_Helper().save_png_data(png_data).__contains__("Png data with size")

    def test_invoke_directly__exec_js_code(self):
        payload  = {'url'     : 'https://google.com',
                    'delay'   : 0,
                    'headless': True,
                    'js_code' : "document.write('hello world')"}
        png_data = self.handler(payload)

        assert Browser_Lamdba_Helper().save_png_data(png_data).__contains__("Png data with size")

    def test_deploy_lambda(self):
        deploy = Lambda_Deploy(self.handler)
        result = deploy.now()

        assert result.get('State'         ) == 'Active'
        assert result.get('FunctionName'  ) == self.lambda_name

    def test_invoke_lambda__simple_url(self):
        png_data = Lambda(self.lambda_name).invoke({'url':'https://google.com'})

        assert Browser_Lamdba_Helper().save_png_data(png_data).__contains__("Png data with size")

    def test_invoke_lambda__with_delay(self):
        payload  = {'url'   : 'https://glasswallsolutions.com/',
                    'delay' : 1}
        png_data = Lambda(self.lambda_name).invoke(payload)

        assert Browser_Lamdba_Helper().save_png_data(png_data).__contains__("Png data with size")

    def test_invoke_lambda__github_url(self):
        png_data = Lambda(self.lambda_name).invoke({'url':'https://github.com'})

        assert Browser_Lamdba_Helper().save_png_data(png_data).__contains__("Png data with size")

    @staticmethod
    def check_or_upload_dependency(target):
        s3 = S3()
        s3_bucket = AWS_Config().lambda_s3_bucket()
        s3_key = 'lambdas-dependencies/{0}.zip'.format(target)
        if s3.file_exists(s3_bucket, s3_key) is False:
            assert pip_install_dependency(target) is True
            assert upload_dependency(target)      is True


