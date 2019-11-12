> 存储在服务端：通过cookie存储一个session_id，然后具体的数据则是保存在session中。如果用户已经登录，则服务器会在cookie中保存一个session_id，下次再次请求的时候，会把该session_id携带上来，服务器根据session_id在session库中获取用户的session数据。就能知道该用户到底是谁，以及之前保存的一些状态信息。这种专业术语叫做server side session。

将session数据加密，然后存储在cookie中。这种专业术语叫做client side session。flask采用的就是这种方式，但是也可以替换成其他形式。

每个网站都有登录功能，当登录成功，一段时间都不需要再登录了。那登录保持这个状态我们就可以通过session来搞定。 flask里面的session必须要设置SECRET_KEY

- flask_session是flask框架实现session功能的一个插件，用来替代flask自带的session实现机制。

### flask默认提供了session, 但是存在以下问题:

　　① session数据存在客户端, 不安全

　　② 大小有限制

　　③ 增加了客户端的压力

### 配置参数
- `SESSION_COOKIE_NAME`
```
设置返回给客户端的cookie的名称，默认是“session”;放置在response的头部；
```
- `SESSION_COOKIE_DOMAIN`
```
设置会话的域，默认是当前的服务器，因为Session是一个全局的变量，可能应用在多个app中；

```
- `SESSION_COOKIE_PATH`
```
设置会话的路径，即哪些路由下应该设置cookie，如果不设置，那么默认为‘/’，所有的路由都会设置cookie
```
- `SESSION_COOKIE_SECURE`
```
cookie是否和安全标志一起设置，默认为false，这个一般采用默认。
```
- `PERMANENT_SESSION_LIFETIME`
```
设置session的有效期，即cookie的失效时间，单位是s。这个参数很重要，因为默认会话是永久性的。
```
- `SESSION_TYPE`
```
设置session保存的位置，可以有多种配置，
SESSION_TYPE = ‘null’          : 采用flask默认的保存在cookie中；
SESSION_TYPE = ‘redis’         : 保存在redis中
SESSION_TYPE = ‘memcached’     : 保存在memcache
SESSION_TYPE = 'filesystem'      : 保存在文件
SESSION_TYPE = 'mongodb'        : 保存在MongoDB
SESSION_TYPE = 'sqlalchemy'     : 保存在关系型数据库
```
- `SESSION_PERMANENT`
```
是否使用永久会话，默认True，但是如果设置了PERMANENT_SESSION_LIFETIME，则这个失效；
```
- `SESSION_KEY_PREFIX`
```
在所有的会话键之前添加前缀，对于不同的应用程序可以使用不同的前缀；默认“session:”，即保存在redis中的键的名称前都是以“session:”开头；

for example:
SESSION_KEY_PREFIX = 'session:'
```
- `SESSION_REDIS`
```
如果SESSION_TYPE = ‘redis’，那么设置该参数连接哪个redis，其是一个连接对象；如果不设置的话，默认连接127.0.0.1:6379/0
for example:
SESSION_REDIS = redis.StrictRedis(host="127.0.0.1", port=6390, db=4)
```

