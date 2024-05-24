import google_drive
import aws_s3

API_KEY = 'secret'

AWS_BUCKET_NAME = 'bucket-name'
AWS_BUCKET_REGION = 'bucket-region'
AWS_KEY = 'secret'
AWS_SECRET = 'secret'

def main():
    google_client = google_drive.GoogleDriveClient(API_KEY)
    s3_client = aws_s3.S3Client(AWS_BUCKET_NAME, AWS_BUCKET_REGION, AWS_KEY, AWS_SECRET)

    file_id = '1-Z9TsBVxwyBp7SIERC8bxbm1m3j3oBmW'

    file_name, file_content = google_client.download_file(file_id)
    if file_name and file_content:
        s3_client.upload_file(file_name, file_content)
    else:
        print('Error downloading file from Google Drive.')

if __name__ == '__main__':
    main()