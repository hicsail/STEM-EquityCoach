import google_drive
import aws_s3
import llm
import time

API_KEY = 'AIzaSyA3xPXNN0A7YP7St0c0T5DE622MEVYUmk8'

AWS_BUCKET_NAME = 'stem-equitycoach'
AWS_BUCKET_REGION = 'us-east-1'
AWS_KEY = 'AKIAVKMYSWB4XJMOPAJD'
AWS_SECRET = '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'

def main():
    # google_client = google_drive.GoogleDriveClient(API_KEY)
    # s3_client = aws_s3.S3Client(AWS_BUCKET_NAME, AWS_BUCKET_REGION, AWS_KEY, AWS_SECRET)

    # file_id = '1WmR7nZB5wdKKgEP-FNyPhdOHVnS6YDt-'

    # file_name, file_content = google_client.download_file(file_id)
    # if file_name and file_content:
    #     s3_client.upload_file(file_name, file_content)
    # else:
    #     print('Error downloading file from Google Drive.')

    ollama = llm.Ollama()
    ollama.load_google_documents(id='1bzTqLQM-peEdn9yrblhvvDk5FrStaVuN')
    # ollama.load_google_documents(id='1QviuYp_buJBq9TJruJBSou4dfdQzns9C')
    # ollama.chroma_init()
    ollama.ask('Give me a summary of the curriculum.', print_result=True)
    while True:
        question = input('\033[92m' + 'Ask a question > ' + '\033[0m')
        if question == 'exit':
            break
        timestart = time.time()
        ollama.ask(question, print_result=True)
        timeend = time.time()
        print('Time taken to answer: ', timeend - timestart, 'seconds')

if __name__ == '__main__':
    main()