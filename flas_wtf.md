# Creating Forms

没有任何配置，FlaskForm 将是具有 csrf 保护的会话安全表单。我们鼓励您什么也不做。  
如果要禁用 csrf 保护，可以通过：  
`form = FlaskForm(csrf_enabled=False)`

要为 Flask 应用程序全局启用 CSRF 保护，请注册 CSRFProtect 扩展

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

像其他 Flask 扩展一样，您可以延迟应用它：

```python
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
```

- **note** CSRF 保护需要一个密钥来对令牌进行安全签名。默认情况下，它将使用 Flask 应用程序的 SECRET_KEY。如果您想使用单独的令牌，则可以设置 `WTF_CSRF_SECRET_KEY`。
  如果模板不使用 FlaskForm，则使用表单中的标记来呈现隐藏的输入。

```python
<form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
</form>
```

## Forms and Fields¶

`class flask_wtf.FlaskForm(formdata=<object object>, **kwargs)`
如果未指定 formdata，则将使用 flask.request.form 和 flask.request.files。明确传递 formdata = None 可以防止这种情况。

`validate_on_submit()`
仅在提交表单后才调用 validate（）。这是 form.is_submitted（）和 form.validate（）的快捷方式。
