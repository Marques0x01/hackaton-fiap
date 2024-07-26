import boto3
from botocore.exceptions import ClientError

from src.exception.CustomException import ErrorOnConfirmingUser, UsernameAlreadyExistsException


class CognitoService:

    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name='us-east-2')
        self.USER_POOL_ID_MEDICO = "us-east-2_jQArCPh0p"
        self.USER_POOL_ID_USER = 'us-east-2_VeeUUZslG'
        self.CLIENT_ID_MEDICO = "269b27fe44k0voqf6b84s6dq33"
        self.CLIENT_ID_USER = "6v4c2oqrgv71f0slpk91fjfh2f"

    def login(self, username, password, type_user):
        CLIENT_ID = self.CLIENT_ID_MEDICO if type_user == "DOCTOR" else self.CLIENT_ID_USER

        try:
            response = self.client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                ClientId=CLIENT_ID,
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )
            return {
                "status_code": 200,
                "message": "user authenticated",
                "data": {
                    "user": username,
                    "token": response["AuthenticationResult"]["AccessToken"],
                    "refresh_token": response["AuthenticationResult"]["RefreshToken"]
                }
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'NotAuthorizedException':
                return {'status_code': 400, 'message': 'Invalid credentials'}
            elif e.response['Error']['Code'] == 'UserNotFoundException':
                return {'status_code': 400, 'message': 'Invalid credentials'}
            else:
                return {'error': str(e)}

    def register_user(self, username, email, password, type_user):
        USER_POOL = self.USER_POOL_ID_MEDICO if type_user == "DOCTOR" else self.USER_POOL_ID_USER

        try:
            if self.user_exists(username, USER_POOL):
                raise UsernameAlreadyExistsException(
                    f"User {username} already exists")

            response_creation = self.client.admin_create_user(
                UserPoolId=USER_POOL,
                Username=username,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    }
                ],
                MessageAction='SUPPRESS'
            )

            if response_creation.get("ResponseMetadata") and response_creation.get("ResponseMetadata").get("HTTPStatusCode") != 200:
                raise Exception("Error creating user")

            response_confirmation = self.client.admin_set_user_password(
                UserPoolId=USER_POOL,
                Username=username,
                Password=password,
                Permanent=True
            )

            if response_confirmation.get("ResponseMetadata") and response_confirmation.get("ResponseMetadata").get("HTTPStatusCode") != 200:
                raise ErrorOnConfirmingUser("Error confirming user")

        except UsernameAlreadyExistsException as e:
            raise e
        except ErrorOnConfirmingUser as e:
            try:
                self.client.admin_delete_user(
                    UserPoolId=USER_POOL,
                    Username=username
                )
            except Exception as delete_error:
                print({
                    'status': 'error',
                    'message': f'Failed to delete user after creation error: {delete_error}'
                })
                raise delete_error

            raise e
        except Exception as e:
            print({
                'status': 'error',
                'message': f'Failed to create user: {e}'
            })
            raise e

    def user_exists(self, username, user_pool_id):
        try:
            self.client.admin_get_user(
                UserPoolId=user_pool_id,
                Username=username
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'UserNotFoundException':
                return False
            else:
                raise e
