from lib.revChatGPT import Chatbot
from os.path import exists
import json

def init_chatbot():
    if exists("config.json"):
        with open("config.json", "r", encoding='utf-8') as f:
            config = json.load(f)
        global chatbot
        chatbot = Chatbot(config)
    else:
        print("Please create and populate config.json to continue")
        exit()

class Handler:
    res = {
        "code": 0,
        "msg": '',
        "data": {}
    }

    @staticmethod
    def getResponse() -> dict:
        res = Handler.res
        return res

    @staticmethod
    def getlogin() -> dict:
        res = Handler.res
        res["data"] = { "a": 1 }
        res["msg"] = 'success'
        return res

    @staticmethod
    def getParams(data) -> dict:
        res = Handler.res
        if data is not None:
            res["data"] = data
        return res

    @staticmethod
    def getChatBotResponseTxt(data) -> dict or None:
        res = Handler.res
        if data is not None and "txt" in data:
            prompt = []
            prompt.append(data["txt"])
            try:
                formatted_parts = []
                for message in chatbot.get_chat_response(prompt, output="stream"):
                    # Split the message by newlines
                    message_parts = message['message'].split('\n')

                    # Wrap each part separately
                    formatted_parts = []
                    for part in message_parts:
                        formatted_parts.extend(textwrap.wrap(part, width=80))
                        for formatted_line in formatted_parts:
                            if len(formatted_parts) > lines_printed+1:
                                print(formatted_parts[lines_printed])
                                lines_printed += 1
                res["data"] = formatted_parts[lines_printed]
                yield res
            except Exception as e:
                print("Something went wrong!")
                print(e)
                r = []
                r.append(r)
                res["code"] = 1
                res["msg"] = "Something went wrong!"
                return r
        else:
            res["code"] = 1
            res["msg"] = "未入txt参数！"
            return res