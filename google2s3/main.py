import llm
import time

def main():
    ollama = llm.Ollama()

    load_drive = input('Load from Google Drive? (y/n) > ')
    if load_drive == 'y':
        folder_id = input('Enter the folder id > ')
        ollama.load_google_documents(id=folder_id.strip())

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