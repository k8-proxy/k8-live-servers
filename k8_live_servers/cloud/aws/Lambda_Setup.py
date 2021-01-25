from osbot_aws.Dependencies import pip_install_dependency, upload_dependency
from osbot_utils.utils.Files import path_combine, folder_exists

from k8_kubectl.helpers.to_add_to_sbot.OSBot_AWS_AWS import Lambda_Upload_Package

class Lambda_Setup:

    def upload_packages_to_s3__for_elastic(self):
        packages = ['python-dotenv', 'elasticsearch']
        Lambda_Upload_Package().upload_to_s3(packages)

