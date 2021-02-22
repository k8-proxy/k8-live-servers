from osbot_aws.helpers.Lambda_Upload_Package import Lambda_Upload_Package

class Lambda_Setup:

    def upload_packages_to_s3__for_elastic(self):
        packages = ['python-dotenv', 'elasticsearch']
        Lambda_Upload_Package().upload_to_s3(packages)

