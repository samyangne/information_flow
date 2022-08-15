import socket
import threading
# import json
import wei_bo_login

# https://blog.csdn.net/yexuejianghan/article/details/119255663
def main_n():
    # 创建服务器套接字
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取本地主机名称
    # host = socket.gethostname()
    host = "localhost"
    # 设置端口号
    port = 8888

    # 将套接字与本地主机和端口绑定
    serversocket.bind((host, port))

    # 设置监听最大连接数
    serversocket.listen(5)

    # 获取本地服务器的连接信息
    myaddr = serversocket.getsockname()

    print("服务器地址:%s" % str(myaddr))

    # 循环等待接受客户端信息
    while True:
        # 获取一个客户端连接
        clientsocket, addr = serversocket.accept()
        print("连接地址:%s" % str(addr))

        try:
            # 为每一个请求开启一个处理线程
            t = ServerThreading(clientsocket)
            t.start()
            pass
        except Exception as identifier:
            print(identifier)
            pass
        pass
    serversocket.close()
    pass


class ServerThreading(threading.Thread):

    def __init__(self, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        pass

    def run(self):
        print("开启线程.....")
        try:
            while True:
                # 接受数据
                msg = ''
                while True:
                    # 从Java端读取recvsize个字节
                    rec = self._socket.recv(self._recvsize)

                    # 解码成字符串
                    msg += rec.decode(self._encoding)
                    print("解码后数据：")
                    print(msg)

                    # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕
                    # 所以需要自定义协议标志数据接受完毕
                    if msg.strip().endswith('over!!!'):
                        msg = msg[:-7]
                        break
                '''
                # 将字符串解析成JSON格式数据
                re = json.loads(msg)
                print("解析成JSON数据：")
                print(re)
    
                # 修改JSON数据并转换成字符串
                re["content"] = "python收到数据>> "+re["content"]
                # sendmsg = json.dumps(re)
                # print("修改JSON数据并发送：")
                print(re)
                '''
                print("收到外来数据：" + msg)
                if msg == "quit":
                    break
                else:
                    # 发送字符串数据给Java端
                    back_msg = "数据收到！正在发表中。。。\n"
                    self._socket.send(("%s" % back_msg).encode(self._encoding))

                    wei_bo_login.send_msg_to_weibo(msg)

            pass
        except Exception as identifier:
            #self._socket.send("500".encode(self._encoding))
            print(identifier)
            pass
        finally:
            self._socket.close()
        print("任务结束.....")
        pass

    def __del__(self):
        pass


if __name__ == "__main__":
    main_n()
