def manage_conversation_history(messages, max_history):
    if len(messages) > max_history:
        return messages[-max_history:]
    return messages
