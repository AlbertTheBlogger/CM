from users.models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string


# 这个方法返回一个8位数的随机字符串
def random_str(randomlength=8):
    # 生成a-z,A-Z,0-9左右的字符
    chars = string.ascii_letters + string.digits
    # 从a-zA-Z0-9生成指定数量的随机字符
    strcode = ''.join(random.sample(chars, randomlength))
    return strcode

