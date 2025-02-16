import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Data and features
data = [
    'BFV scheme: 128-bit security, 100 Ops/sec, 500 MB memory usage, 200 KB network overhead, 1200 ms latency, used for numerical data processing, O(n log n) time complexity',
    'CKKS scheme: 128-bit security, 150 Ops/sec, 550 MB memory usage, 250 KB network overhead, 1100 ms latency, used for floating-point calculations, O(n log n) time complexity',
    'FV scheme: 192-bit security, 80 Ops/sec, 600 MB memory usage, 300 KB network overhead, 1300 ms latency, used for health data encryption, O(n log n) time complexity',
    'Helib scheme: 256-bit security, 70 Ops/sec, 650 MB memory usage, 350 KB network overhead, 1400 ms latency, used for financial data analysis, O(n log n) time complexity',
    'SEAL scheme: 128-bit security, 120 Ops/sec, 520 MB memory usage, 220 KB network overhead, 1150 ms latency, used for general purposes, O(n log n) time complexity',
    'PALISADE scheme: 256-bit security, 90 Ops/sec, 580 MB memory usage, 330 KB network overhead, 1250 ms latency, used for advanced computations, O(n^2) time complexity'
]
features = ['Security Level', 'Ops/sec', 'Memory Usage (MB)', 'Network Overhead (KB)', 'Latency (ms)', 'Use Case', 'Time Complexity']
conversation_history = []

def generate_ai_output(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=3000
        )
        # Extracting the message content correctly from the API response object
        if response.choices and len(response.choices) > 0:
            # Each choice should be accessed through its properties, not dictionary keys
            return response.choices[0].message.content.strip()  # Correct property access
        else:
            return "Received an unexpected response format from the API."
    except Exception as e:
        print("Exception occurred:", str(e))
        return f"Error generating question: {str(e)}"


def main():
    initial_message = {
    'role': 'system',
    'content': f"Initiate a discussion by welcoming a user. This user is deciding which fully-homomorphic encryption scheme to use, and they need your help \
    deciding. Arbitrarily choose ONE of the following features in ({features}) to ask a multiple-choice question about what version of that feature would best suit \
    their needs, using the data given in ({data}) to design your choices. Use each data point given for that particular feature as an option. Assume the user is a \
    beginner, so keep the questions simple and brief and include an option for uncertainty. Feel free to give a one-sentence description for each option."
    }
    conversation_history.append(initial_message)
    prompt = generate_ai_output(conversation_history)
    print("AI: ", prompt)

    while len(conversation_history) < 14:
        user_input = input("User: ")
        user_message = {'role': 'user', 'content': user_input}
        conversation_history.append(user_message)
        
        ai_message = {
            'role': 'system',
            'content': f"Continue the discussion by asking another multiple-choice question of the same relative format, addressing a new feature that has not been discussed yet. \
             Remember to keep it brief, and no need to greet the user. Just jump right into the question. If you run out of features, just ask if the user has further questions."
        }
        conversation_history.append(ai_message)
        
        prompt = generate_ai_output(conversation_history)
        print("AI: ", prompt)
    
    final_message = {
        'role': 'system',
        'content': f"Based on all these interactions, recommend a scheme or a ranked-list of schemes that best fits the needs outlined in the responses. Make sure to pick a scheme \
            from the dataset provided. End your message with a brief farewell, such as 'Goodbye.'"
    }
    conversation_history.append(final_message)
    recommendation = generate_ai_output(conversation_history)
    print("AI: ", recommendation)

if __name__ == '__main__':
    main()
