import ollama


model = 'phi3'

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


def generate_sample_stream_data():
    code_string = """
    ```python
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively sort both halves
        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        # Merge the sorted sub-arrays
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Example usage:
if __name__ == "__main__":
    input_array = [54, 26, 93, 17, 77, 31, 44, 55]
    print("Original array:", input_array)
    merge_sort(input_array)
    print("Sorted array:", input_array)
    ```
    """

    yield "Starting stream...\n"

    # Break the code string into chunks
    for i in range(0, len(code_string), 100):  # Each chunk is 100 characters
        yield code_string[i:i + 100] + "\n"
        print(code_string[i:i + 100])

    yield "Stream complete.\n"


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
