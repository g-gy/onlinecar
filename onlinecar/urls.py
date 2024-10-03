from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
import login.views
import index.views
import order.views
import map.views
import user.views
import pay.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index.views.index, name="主页"),
    path("login/", login.views.login, name="登录"),
    path("register/", login.views.register, name="注册"),
    path("change/", login.views.change, name="修改密码"),
    path("logout/", login.views.logout, name="退出"),
    path("index/", index.views.index, name="主页"),
    path("map/", map.views.mapview, name="地图"),
    path("order/", order.views.orderview, name="订单"),
    path("user/", user.views.userview, name="个人"),
    path("placeorder/", order.views.placeorder, name="下单"),
    path("getorder/", order.views.getorder, name="接单"),
    path("startorder/", order.views.startorder, name="开始"),
    path("endorder/", order.views.endorder, name="结束"),
    path("upload/", user.views.upload, name="上传头像"),
    path("ccorder/", order.views.ccorder, name="取消订单"),
    path('pay/', pay.views.alipay_pay, name='支付'),
    path('return/', pay.views.alipay_return, name='返回'),
    path('notify/', pay.views.alipay_notify, name='通知'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
