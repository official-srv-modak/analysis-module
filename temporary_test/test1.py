import ollama

def send(chat):
    messages = []
    messages.append({'role': 'user', 'content': chat})
    stream = ollama.chat(model='llama3', messages=messages, stream=True)

    for chunk in stream:
        part = chunk['message']['content']
        print(part, end='', flush=True)
        messages.append({'role': 'assistant', 'content': part})

while True:
    print()
    chat = input(">>> ")
    if chat.lower() == "/exit":
        break
    elif len(chat) > 0:
        send(chat)
