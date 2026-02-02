# env_setup.py
import os

# 定义免检清单
no_proxy_list = "127.0.0.1,localhost,0.0.0.0"

# 在模块被 import 的那一刻，这两行就会执行
os.environ["no_proxy"] = no_proxy_list
os.environ["NO_PROXY"] = no_proxy_list

print(f"🚀 [自动初始化] 已绕过代理地址: {no_proxy_list}")