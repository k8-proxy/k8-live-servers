import requests
from unittest                                    import TestCase
from osbot_aws.AWS_Config                        import AWS_Config
from osbot_aws.apis.Lambda                       import Lambda
from osbot_aws.apis.S3                           import S3
from osbot_aws.Dependencies                      import upload_dependency
from osbot_aws.Dependencies                      import pip_install_dependency
from osbot_aws.apis.STS                          import STS
from osbot_aws.helpers.Rest_API                  import Rest_API
from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper

from k8_live_servers.cloud.aws.Lambda_Deploy     import Lambda_Deploy
from k8_live_servers.lambdas.screenshot_fastapi  import run
from fastapi.testclient                          import TestClient
from k8_live_servers.fastapi.app.main            import app

client = TestClient(app)

class test_screenshot_fast_api(TestCase):

    lambda_ : Lambda
    test_rest_api_name = 'temp-test-screenshot-api'

    @staticmethod
    def check_or_upload_dependency(target):
        """
        Check if the required dependency is present in the configured bucked and if not upload the dependency
        :param target: dependency to upload
        """
        s3 = S3()
        s3_bucket = AWS_Config().lambda_s3_bucket()
        s3_key = 'lambdas-dependencies/{0}.zip'.format(target)
        if s3.file_exists(s3_bucket, s3_key) is False:
            assert pip_install_dependency(target) is True
            assert upload_dependency(target)      is True

    @staticmethod
    def setup_test_environment__Rest_API(cls):
        rest_api    = Rest_API(cls.test_rest_api_name).create()
        assert  rest_api.exists()
        parent_id   = rest_api.resource_id('/')
        rest_api.api_gateway.resource_create(rest_api.id(),parent_id,'{proxy+}')
        rest_api.add_method_lambda('/'        , 'ANY', cls.lambda_name         )
        rest_api.add_method_lambda('/{proxy+}', 'ANY', cls.lambda_name         )
        result = rest_api.deploy()
        assert result

    @staticmethod
    def teardown_test_environment__Rest_API(cls):
        rest_api = Rest_API(cls.test_rest_api_name)
        assert rest_api.delete().not_exists()

    @classmethod
    def setUpClass(cls) -> None:
        STS().check_current_session_credentials()
        cls.handler     = run
        cls.deploy      = Lambda_Deploy(cls.handler)
        # cls.deploy.deploy_lambda.package.lambda_name = 'screenshot_fastapi_lambda'
        cls.lambda_     = Lambda(name= cls.deploy.deploy_lambda.lambda_name())
        cls.lambda_name = cls.lambda_.name

        assert cls.deploy.now().get('State') == 'Active'
        assert cls.lambda_.exists()          is True
        cls.setup_test_environment__Rest_API(cls)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.teardown_test_environment__Rest_API(cls)
        assert cls.lambda_.delete(delete_log_group=False) is True

    def setUp(self):
        super().setUp()
        self.rest_api = Rest_API(self.test_rest_api_name).create()

    def test_check_or_upload_dependency(self):
        # Ensure that all the required dependencies are available in configured S3 bucket
        dependencies = 'syncer,requests,pyppeteer2,websocket-client,magnum,fastapi,nest-asyncio'
        for target in dependencies.split(','):
            self.check_or_upload_dependency(target)

    def test_invoke_api_directly__get(self):
        response = client.get("/")

        assert response.status_code    ==  200
        assert response.json()         == {"message" : "Welcome to Screenshot FastAPI"}

    def test_invoke_api_directly__post_screenshot__simple_url(self):
        payload = '{"url" : "https://google.com"}'
        response = client.post("/api/v1/screenshot", payload)

        assert response.status_code == 200
        assert Browser_Lamdba_Helper().save_png_data(response.json()['png_data']).__contains__("Png data with size")

    def test_invoke_api_directly__post_screenshot__open_page(self):
        payload = '{"url" : "https://www.google.com", "headless" : false}'
        response = client.post("/api/v1/screenshot", payload)

        assert response.status_code == 200
        assert Browser_Lamdba_Helper().save_png_data(response.json()['png_data']).__contains__("Png data with size")

    def test_invoke_api_directly__post_screenshot__exec_js_code(self):
        payload = '{"url" : "https://www.google.com", "js_code" : "document.write(\'hello world\')"}'
        response = client.post("/api/v1/screenshot", payload)

        assert response.status_code == 200
        assert Browser_Lamdba_Helper().save_png_data(response.json()['png_data']).__contains__("Png data with size")

    def test_invoke_lambda__api_gateway_base_url(self):
        response                                                           = self.rest_api.test_method('/', 'GET')

        assert response.get('status'                                     ) == 200
        assert response.get('body'                                       ) == '{"message":"Welcome to Screenshot FastAPI"}'

    def test_invoke_lambda__post_screenshot__simple_url(self):
        payload  = '{"url" : "https://google.com"}'
        response = requests.post(self.rest_api.url('/api/v1/screenshot'), payload)

        assert response.status_code == 200
        assert Browser_Lamdba_Helper().save_png_data(response.json()['png_data']).__contains__("Png data with size")

    def test_invoke_lambda__post_screenshot__exec_js_code(self):
        payload  = '{"url" : "https://www.google.com", "js_code" : "document.write(\'hello world\')"}'
        response = requests.post(self.rest_api.url('/api/v1/screenshot'), payload)

        assert response.status_code == 200
        assert Browser_Lamdba_Helper().save_png_data(response.json()['png_data']).__contains__("Png data with size")


