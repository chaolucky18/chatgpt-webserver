import http.server
import socketserver
import json

# 创建一个处理程序类
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    # 处理GET请求
    def do_GET(self):
        # 获取客户端请求的URL路径
        path = self.path
        
        # 如果客户端请求了"/login"路径
        if path == "/login":
            # 设置响应状态码和消息头
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # 返回json格式的数据
            data = {
                "status": "success",
                "message": "Login successful"
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            # 如果客户端请求了其他路径，则返回默认响应
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Hello World!")

# 创建一个web服务器
server = socketserver.TCPServer(('', 8000), MyRequestHandler)
print("server running at: http://127.0.0.1:8000/")
# 启动web服务器，开始处理请求
server.serve_forever()