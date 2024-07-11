import llm
import time
import argparse

def main():
    ollama = llm.Ollama()

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--context", type=str, choices=["name", "raw", "none"], default="none", help="Check flag")
    args = parser.parse_args()

    load_local = input('Load from local? (y/n) > ')
    if load_local == 'y':
        ollama.load_local()

    load_drive = input('Load from Google Drive? (y/n) > ')
    if load_drive == 'y':
        folder_id = input('Enter the folder id > ')
        ollama.load_google_drive(id=folder_id.strip())

    while True:
        question = input('\033[92m' + 'Ask a question > ' + '\033[0m')
        if question == 'exit':
            break
        timestart = time.time()
        ollama.ask(question, print_result=True, context=args.context)
        timeend = time.time()
        print('Time taken to answer: ', timeend - timestart, 'seconds')

if __name__ == '__main__':
    main()