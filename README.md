# Auto_grass

更新了下y神的小草脚本，原po:https://github.com/ymmmmmmmm/getgrass_bot

新增了grass批量注册+批量挂号

register.py使用方法：

修改代码中的：yescaptcha_client_key = '' 为你的apikey
注册地址：https://yescaptcha.com/i/rPuQqA

设置下面3个值
num = 100 # 注册数量
password = '' # 密码
refcode = '' # 邀请码

执行：python3 register.py

main.py使用方法：
通过register.py生成的account.txt，将每一行结尾加上代理，格式如下
邮箱----密码----user_id----socks5://xxx:xxxx@1.1.1.1:1111
