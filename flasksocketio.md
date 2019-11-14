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
    let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace, {'reconnect': true});
</script>
```
