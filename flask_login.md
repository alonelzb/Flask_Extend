# Flask-Login

Flask-Login为Flask提供用户会话管理,它可以处理登录，注销和记住用户长时间会话的常见任务
使用Flask-Login的应用程序中最重要的部分是LoginManager类。您应该在代码中的某个位置为应用程序创建一个，如下所示：

```python
login_manager = LoginManager()
```

login manager 包含使您的应用程序和Flask-Login一起工作的代码
一旦创建了实际的应用程序对象,您可以使用以下命令配置登录：

```python
login_manager.init_app(app)
```

默认情况下，Flask-Login使用会话进行身份验证,这意味着您必须在应用程序上设置密钥，

## How it Works

您将需要提供一个user_loader回调。此回调用于从会话中存储的用户ID重新加载用户对象,它应该采用用户的unicode ID，并返回相应的用户对象。例如：

```python
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
```

如果ID无效，则应返回None（不会引发异常）。（在这种情况下，将手动从会话中删除该ID，然后继续处理。)

## Your User Class

您用来表示用户的类需要实现以下属性和方法：
`is_authenticated`
  如果用户通过了验证，则此属性应返回True，

`is_active`
  如果这是一个活动用户，则此属性应返回True-除了通过身份验证之外,

`is_anonymous`
  如果这是匿名用户，则此属性应返回True。（实际用户应返回False。）

`get_id()`
  此方法必须返回一个唯一标识此用户的unicode, 并且可以用来从user_loader回调中加载用户。请注意，这必须是unicode-如果ID本身是int或其他某种类型，则需要将其转换为unicode

> 为了简化用户类的实现，您可以从UserMixin继承，后者为所有这些属性和方法提供了默认实现。（不过，这不是必需的。）

## Login Example

用户通过身份验证后，即可使用login_user函数登录。  
要求您的用户登录的视图可以用login_required装饰器修饰  

```python
@app.route("/settings")
@login_required
def settings():
    pass
```

当用户准备注销时：

```python
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)
```

They will be logged out, and any cookies for their session will be cleaned up.

## Customizing the Login Process

默认情况下，当用户尝试不登录而访问login_required视图时，Flask-Login将闪烁一条消息并将其重定向到登录视图。（如果未设置登录视图，它将终止并显示401错误。）  
The name of the log in view can be set as LoginManager.login_view. For example:

```python
login_manager.login_view = "users.login
```

闪烁的默认消息是“请登录以访问此页面”。要自定义消息，请设置LoginManager.login_message：

```python
login_manager.login_message = u"Bonvolu ensaluti por uzi tiun paĝon."
```

要自定义消息类别，请设置LoginManager.login_message_category：

```python
login_manager.login_message_category = "info"
```

登录视图重定向到后，它将在查询字符串中具有下一个变量，即用户试图访问的页面。或者，如果USE_SESSION_FOR_NEXT为True，则该页面将存储在会话中的下一个键下。  
如果您想进一步自定义流程，请使用LoginManager.unauthorized_handler装饰一个函数：

```python
@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return a_response
```

## Custom Login using Request Loader¶

有时，您希望不使用Cookie来登录用户，例如使用标头值或作为查询参数传递的api键。在这些情况下，应使用request_loader回调。此回调的行为应与user_loader回调相同，除了它接受Flask请求而不是user_id。  
例如，要支持使用Authorization标头从url参数和Basic Auth登录：

```python
@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None
```

## Anonymous Users

默认情况下，当用户实际未登录时，current_user设置为AnonymousUserMixin对象。它具有以下属性和方法：

- is_active and is_authenticated are False
- is_anonymous is True
- get_id() returns None

如果您对匿名用户有自定义要求（例如，他们需要具有权限字段），则可以通过以下方式向LoginManager提供可创建匿名用户的可调用对象（类或工厂函数）：

```python
login_manager.anonymous_user = MyAnonymousUser
```

## Remember Me

默认情况下，当用户关闭其浏览器时，会删除Flask会话并注销用户。“记住我”可防止用户在关闭浏览器时意外注销。这并不意味着在用户注销后记住或在登录表单中预先填写用户名或密码。  
“记住我”功能可能难以实现。但是，Flask-Login使其变得几乎透明-只需将Remember = True传递给login_user调用即可。  
Cookie将保存在用户计算机上，然后Flask-Login将自动从该Cookie中恢复用户ID（如果该ID不在会话中）。  
可以使用REMEMBER_COOKIE_DURATION配置设置cookie过期之前的时间，也可以将其传递给login_user。Cookie是防篡改的，  因此，如果用户对其进行篡改（即插入其他人的用户ID代替自己的用户ID），则该Cookie只会被拒绝，就好像它不在那里一样.

该级别的功能会自动处理。但是，您可以（并且应该，如果您的应用程序处理任何类型的敏感数据）提供其他基础结构，以提高记住的Cookie的安全性  

## Alternative Tokens¶

使用用户ID作为记住令牌的值意味着您必须更改用户ID才能使他们的登录会话无效。一种改善方法是使用`alternative user id`代替`user’s ID`。例如：

```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(alternative_id=user_id).first()
```

然后，您的User类的get_id方法将返回alternative id,而不是用户的primary ID:

```python
def get_id(self):
    return unicode(self.alternative_id)
```

这样，您可以在用户更改密码时自由地将用户的替代ID更改为新的随机生成的值，这将确保其旧的身份验证会话将不再有效。请注意，备用ID仍必须唯一标识用户……将其视为第二个用户ID。

## Fresh Logins¶

用户登录后，其会话将被标记为“fresh,”, 这表明他们实际上在该会话上进行了身份验证,当会话被销毁并且使用“记住我” cookie重新登录时,它被标记为 “non-fresh.”  
login_required不能区分新鲜度,大多数页面都可以,但是，诸如更改个人信息之类的敏感操作应要求重新登录(无论如何，诸如更改密码之类的操作都应始终要求重新输入密码。)  

fresh_login_required除了验证用户已登录外，还将确保其登录名是最新的。如果没有，它将把他们发送到一个页面，他们可以在其中重新输入凭据。您可以通过设置LoginManager.refresh_view，needs_refresh_message和needs_refresh_message_category来以与自定义login_required相同的方式自定义其行为：

```python
login_manager.refresh_view = "accounts.reauthenticate"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page."
)
login_manager.needs_refresh_message_category = "info"
```

或通过提供自己的回调来处理刷新：

```python
@login_manager.needs_refresh_handler
def refresh():
    # do stuff
    return a_response
```

要将会话再次标记为新鲜，请调用confirm_login函数。

## Session Protection¶

尽管上述功能有助于保护您的“记住我”令牌免受cookie窃贼的侵害，但会话cookie仍然很容易受到攻击。Flask-Login包含会话保护，以帮助防止用户的会话被盗。  
您可以在LoginManager和应用程序的配置中配置会话保护。如果启用，则可以在基本模式或增强模式下运行。要在LoginManager上进行设置，请将session_protection属性设置为“ basic”或“ strong”：

```python
login_manager.session_protection = "strong"

```

Or, to disable it:

```python
login_manager.session_protection = None
```

默认情况下，它在“基本”模式下被激活。通过将SESSION_PROTECTION设置设置为“None，“basic”或“strong”，可以在应用的配置中将其禁用。

会话保护处于活动状态时，每个请求都会为用户的计算机生成一个标识符（基本上是IP地址和用户代理的安全哈希）。如果会话没有关联的标识符，则将存储所生成的标识符。如果它具有标识符，并且与生成的标识符匹配，则该请求正常。

如果标识符在基本模式下不匹配，或者会话是永久性的，则该会话将被简单地标记为非新会话，并且任何需要重新登录的操作都将迫使用户重新进行身份验证。（当然，您必须已经在适当的位置使用了新的登录名才能使此操作生效。）

如果标识符与非永久会话的强模式不匹配，则将删除整个会话（以及记住令牌（如果存在

## Disabling Session Cookie for APIs

在对API进行身份验证时，您可能需要禁用设置Flask Session cookie。为此，请使用自定义会话界面，该界面根据您在请求上设置的标志跳过保存会话。例如：

```python
from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header

class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)

app.session_interface = CustomSessionInterface()

@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True
```

这样可以防止在用户使用header_loader进行身份验证时设置Flask Session cookie。

## API

`class flask_login.LoginManager(app=None, add_context_processor=True)`  
此对象用于保存用于登录的设置。LoginManager的实例未绑定到特定的应用程序，因此您可以在代码主体中创建一个实例，然后在工厂函数中将其绑定到您的应用程序。

`user_loader(callback)`  
这将设置用于从会话中重新加载用户的回调。设置的函数应带有用户ID（Unicode）并返回用户对象，如果用户不存在，则返回None。  
`needs_refresh()`  
当用户登录时会调用此方法，但由于会话已过时，因此需要重新认证。如果您在needs_refresh_handler中注册了一个回调，那么它将被调用。否则，它将采取以下措施：  
`login_view`  
用户需要登录时重定向到的视图的名称。（如果您的身份验证机制在应用程序外部，则该名称也可以是绝对URL。）  
`login_message`  
将用户重定向到登录页面时闪烁的消息。  
`refresh_view`  
用户需要重新认证时重定向到的视图的名称。  
`needs_refresh_message`  
当用户重定向到重新认证页面时，该消息将闪烁。  

### Login Mechanisms

`flask_login.current_user`  
当前用户的代理。  
`flask_login.login_fresh()`  
如果当前登录是最新的，则返回True。  
`flask_login.login_user(user, remember=False, duration=None, force=False, fresh=True)`  
登录用户。您应该将实际的用户对象传递给该用户。如果用户的is_active属性为False，则除非force为True，否则他们将不会登录。  
如果登录尝试成功，则返回True，否则返回False（即，由于用户处于非活动状态）。  
`flask_login.logout_user()`  
注销用户。（您不需要传递实际用户。）这也将清除“记住我” cookie（如果存在）。  
`flask_login.confirm_login()`  
这会将当前会话设置为新会话。从Cookie重新加载会话后，会话就会过时。  

### Protecting Views

`flask_login.login_required(func)`  
如果用此装饰视图，它将确保在调用实际视图之前，当前用户已登录并通过身份验证。（如果不是，则调用LoginManager.unauthorized回调。）例如：  

```python
@app.route('/post')
@login_required
def post():
    pass
```

如果仅在某些情况下需要要求用户登录，则可以执行以下操作：

```python
if not current_user.is_authenticated:
    return current_app.login_manager.unauthorized()
```

`flask_login.fresh_login_required(func)`  
如果您以此装饰一个视图，它将确保当前用户的登录名是最新的-也就是说，他们的会话没有从“记住我” cookie中恢复。以此来保护敏感操作，例如更改密码或电子邮件，以阻止cookie小偷的努力。  
如果用户未通过身份验证，则正常调用LoginManager.unauthorized（）。如果它们通过了身份验证，但是它们的会话不是最新的，它将改为调用LoginManager.needs_refresh（）。（在这种情况下，您将需要提供一个LoginManager.refresh_view。）  
关于配置变量，其行为与login_required（）装饰器相同。  

### User Object Helpers

`class flask_login.UserMixin`  
这为Flask-Login期望用户对象具有的方法提供了默认实现。  
`class flask_login.AnonymousUserMixin`  
这是代表匿名用户的默认对象。  

### Utilities

`flask_login.login_url(login_view, next_url=None, next_field='next')`  
创建用于重定向到登录页面的URL。如果仅提供login_view，则将仅返回其URL。  
但是，如果提供了next_url，它将在查询字符串后附加一个next = URL参数，以便登录视图可以重定向回该URL。  
Flask-Login的默认未授权处理程序在重定向到您的登录URL时会使用此功能。要强制使用主机名，请将FORCE_HOST_FOR_REDIRECTS设置为主机。  
如果存在请求标头Host或X-Forwarded-For，这可以防止重定向到外部站点。

### Signals

