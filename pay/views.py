from alipay import AliPay
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from onlinecar import settings
from user.models import user
import time
import random

# 使用时间戳和随机数生成订单号


alipay = AliPay(
    appid=settings.ALIPAY_APP_ID,
    app_private_key_string=settings.APP_PRIVATE_KEY,
    alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY,
    sign_type="RSA2",
    debug=settings.ALIPAY_DEBUG,
)


def alipay_pay(request):
    # 获取订单信息
    money = request.session.get("money")
    timestamp = str(int(time.time() * 1000))
    random_number = str(random.randint(1000, 9999))
    order_id = f"{timestamp}{random_number}"
    # 生成支付订单
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=money,
        subject="充值",
        return_url=settings.ALIPAY_RETURN_URL,
        notify_url=settings.ALIPAY_NOTIFY_URL,
    )

    # 构建跳转支付宝支付的URL
    pay_url = settings.ALIPAY_URL + "?" + order_string
    return pay_url


def alipay_return(request):
    number = request.session.get("number")
    this_user = user.objects.filter(number=number).first()
    addmoney = request.session.get("money")
    this_user.money = this_user.money + float(addmoney)
    this_user.save()
    return redirect("/user/")


def alipay_notify(request):
    return HttpResponse("success")  # 需要返回'success'，不然支付宝会持续发送通知
