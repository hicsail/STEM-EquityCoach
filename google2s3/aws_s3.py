import boto3

class S3Client:
    def __init__(self, bucket_name, region, aws_key, aws_secret):
        self.bucket_name = bucket_name
        self.region = region
        self.aws_key = aws_key
        self.aws_secret = aws_secret
        self.client = boto3.client('s3', region_name=region, aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

    def upload_file(self, file_name, file_content):
        try:
            self.client.put_object(Bucket=self.bucket_name, Key=file_name, Body=file_content)
        except Exception as e:
            print(f'Error: {e}')
            return False
        
        return True