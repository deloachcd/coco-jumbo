def user_input_answer(question):
    response = input(question)
    return response == "" or "y" in response
