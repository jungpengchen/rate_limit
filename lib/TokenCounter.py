import tiktoken


def tokens_count_for_message(message, encoding):
    """Return the number of tokens used by a single message."""
    tokens_per_message = 3

    num_tokens = 0
    num_tokens += tokens_per_message
    for key, value in message.items():
        if key == "function_call":
            num_tokens += len(encoding.encode(value["name"]))
            num_tokens += len(encoding.encode(value["arguments"]))
        else:
            if key == 'content' or key == 'name':
                num_tokens += len(encoding.encode(value))

    return num_tokens


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages for both user and assistant."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    user_tokens = 0
    assistant_tokens = 0
    for i, message in enumerate(messages):
        # Check if the current message involves a service call
        # is_service_call = "assistant" in messages[i]['role']
        is_service_call = False

        # Include tokens from previous messages only when a service call is made
        if is_service_call:
            assistant_tokens += tokens_count_for_message(message, encoding)
            for j in range(i):
                user_tokens += tokens_count_for_message(messages[j], encoding)

        # Count tokens for the current message
        user_tokens += tokens_count_for_message(message, encoding)

    assistant_tokens += 3  # every reply is primed with assistant

    return user_tokens, assistant_tokens, user_tokens + assistant_tokens


def count_tokens_simple(messages_list):
    prompt_text = " ".join([t[1] for t in messages_list])
    tokens = prompt_text.split()
    token_count = len(tokens)
    return token_count


# print(count_tokens_simple(messages_list))


# print(num_tokens_from_messages(messages_list, model_name))
