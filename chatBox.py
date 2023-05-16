from flask import Flask, render_template, request
import openai
import webbrowser

app = Flask(__name__)

# 设置OpenAI API密钥
openai.api_key = 'YOU-KEY'


# ChatGPT对话类
class ChatGPT:
    def __init__(self):
        self.chat_history = []

    def generate_reply(self, user_input):
        # 将用户输入与历史对话记录拼接为模型输入
        model_input = '\n'.join(self.chat_history + [f'User: {user_input}'])

        # 发送对话请求到ChatGPT API
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=model_input,
            max_tokens=1000,
            temperature=0.5,
            n=1,
            stop=None,
            timeout=10,
        )

        # 获取模型生成的回复
        reply = response.choices[0].text.strip()
        return reply


chatbot = ChatGPT()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    # 生成回复
    reply = chatbot.generate_reply(user_input)

    # 将用户输入和回复记录到对话历史中
    chatbot.chat_history.append(f'User: {user_input}')
    chatbot.chat_history.append(f'AI: {reply}')

    return reply

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run()
