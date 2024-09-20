import ollama


model = 'codegemma'

def extract_message_from_stream(stream):
    # Process each chunk in the stream
    output = ""
    for chunk in stream:
        # Extract the LLM's response
        llm_response = chunk['message']['content']
        if (llm_response == '\n'):
            print()
        else:
            print(llm_response, end='')

        # Store the LLM's response
        output += llm_response
        # print(llm_response, end='', flush=True)

    return output

def chat_ollama_single_stream(query):
    chat_messages_context = [{'role': 'user', 'content': query + "\n"}]
    stream = ollama.chat(model=model, messages=chat_messages_context, stream=True)
    # Process each chunk in the stream
    # output = ""
    # for chunk in stream:
    #     # Extract the LLM's response
    #     llm_response = chunk['message']['content']
    #
    #     # Update the chat_messages_context with the LLM's response
    #     # chat_messages_context.append({'role': 'assistant', 'content': llm_response})
    #
    #     # Store the LLM's response
    #     output += llm_response
    #     print(llm_response, end='', flush=True)

    return stream

def chat_ollama_single_stream_1(query):
    chat_messages_context = [{'role': 'user', 'content': query + "\n"}]
    stream = ollama.chat(model=model, messages=chat_messages_context, stream=True)

    # Modify the generator to return bytes instead of a string
    for chunk in stream:
        llm_response = chunk['message']['content']
        if llm_response == '\n':
            print()
        else:
            print(llm_response, end='')
        # Ensure each chunk is converted to bytes
        yield llm_response.encode('utf-8')  # Encode to bytes

def chat_ollama_context(msg, chat_messages_context):
    # Initialize the chat session with an initial user message
    if not chat_messages_context:
        chat_messages_context1 = [{'role': 'user', 'content': msg +"\n"}]
        chat_messages_context = [{'role': 'user', 'content': ""}]
    else:
        chat_messages_context1 = chat_messages_context.copy()
        chat_messages_context1[0]['content'] += msg +"\n"

    # Start the chat stream
    stream = ollama.chat(model=model, messages=chat_messages_context1, stream=True)

    # Process each chunk in the stream
    output = ""
    for chunk in stream:
        # Extract the LLM's response
        llm_response = chunk['message']['content']

        # Update the chat_messages_context with the LLM's response
        # chat_messages_context.append({'role': 'assistant', 'content': llm_response})

        # Store the LLM's response
        output += llm_response
        print(llm_response, end='', flush=True)

    chat_messages_context[0]['content'] += output +"\n"
    return chat_messages_context, output

# msg = ""
# chat_messages_context = None
# while msg.lower() != "exit":
#     msg = input("\nEnter prompt to chat (type 'exit' to end): ")
#     chat_messages_context, assistant_responses = chat_ollama_context(msg, chat_messages_context)
#
# # Print all assistant responses
# for response in assistant_responses:
#     print(response)
