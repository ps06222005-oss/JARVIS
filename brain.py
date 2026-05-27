import ollama


def ask_ai(prompt):

    try:

        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'user',
                    'content': str(prompt)
                }
            ]
        )

        return response['message']['content']

    except Exception as e:

        print("AI Error:", e)

        return "Sorry sir, AI system error."