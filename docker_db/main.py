import chatbot

DOC_PATH = 'res/4th-LandWater-2016guide-11.pdf'

def main():
    question = 'What is the main source of water in the United States?'

    chat = chatbot.ChatBot()
    chat.ask(question, print_result=True)
    chat.load_documents(DOC_PATH)

    # Asking a question
    chat.ask(question, print_result=True)

if __name__ == '__main__':
    main()