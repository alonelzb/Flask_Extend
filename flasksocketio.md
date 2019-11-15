# 简单的连接
- app.py
```python
from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'luozaibo'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    print('connented!')

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
```
- index.html
```python
<script>
    const namespace = '/test';
    let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
</script>
```
# 发送消息到服务器
- app.py
```python
@socketio.on('send_to_server', namespace='/test')
def send_to_server(data):
    print(data)
```
- index.html
```python
    // 发送消息
    data = '我是客户端的消息!';
    socket.emit('send_to_server', data); 
```

# socketio对象的参数
- `always_connect`
当设置为“False”时，新连接是

连接处理程序返回之前的临时

不是“假”的东西，这时

被接受。当设置为“True”时，连接是

立即接受，然后如果连接

处理程序返回“False”断开连接。
如果需要从
连接处理程序和您的客户端在
接收连接接受之前的事件。
在任何其他情况下，使用默认值“False”。


socketio.emit默认`broadcast=True`

所有客户端在连接时都会分配一个房间，该房间以连接的会话ID命名，可以从request.sid获取。
给定的客户可以加入任何房间，可以给任何名称。
当客户端断开连接时，会将其从其所在的所有房间中删除。上下文无关的socketio.send（）和socketio.emit（）函数还接受一个room参数，以广播给房间中的所有客户端。
