import http.server
import socketserver
import json
from lib.handler import Handler
from lib.handler import init_chatbot

init_chatbot()

# 创建一个处理程序类
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    # 处理GET请求
    def do_GET(self):
        # 获取客户端请求的URL路径
        path = self.path
        if "Content-Length" in self.headers and self.headers["Content-Length"] is not None:
            # 获取请求体的长度
            length = int(self.headers["Content-Length"])
            # 读取请求体
            body = self.rfile.read(length)
            # 解析请求体
            try:
                data = json.loads(body)
            except:
                data = None
        else:
            data = None
        
        res = {}
        # 设置响应状态码和消息头
        self.send_response(200)
        if path != '/bot_txt':
            self.send_header('Content-type', 'application/json')
            
        # 如果客户端请求了"/login"路径
        if path == "/login":
            res = Handler.getlogin()
        elif path == "/params":
            res = Handler.getParams(data)
        elif path == '/bot_txt':
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Controle', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            res = Handler.getChatBotResponseTxt(data)
            self.wfile.write(b'event: message\n')
            for message in res:
                self.wfile.write(json.dumps(message).encode('utf-8'))
        else:
            res = Handler.getResponse()

        self.end_headers()
        if path != '/bot_txt':
            self.wfile.write(json.dumps(res).encode('utf-8'))

# 创建一个web服务器
server = socketserver.TCPServer(('', 8000), MyRequestHandler)
print("server running at: http://127.0.0.1:8000/")
# 启动web服务器，开始处理请求
server.serve_forever()