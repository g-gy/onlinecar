from django.db import models


class user(models.Model):

    number = models.CharField(max_length=15, unique=True, verbose_name="账号")
    password = models.CharField(max_length=15, verbose_name="密码")
    name = models.CharField(max_length=5, default="暂未设置",null=True, verbose_name="姓名")
    detail = models.CharField(max_length=500, default="暂未设置", verbose_name="个人简介")
    photo = models.ImageField(upload_to="",default="default.jpg",blank=True,null=True)
    car = models.CharField(max_length=15, default="", verbose_name="车牌号")
    money = models.FloatField(default=0, verbose_name="余额" )
    score = models.IntegerField(default=0, verbose_name="评分")
    corder = models.IntegerField(default=0, verbose_name="乘客订单")
    dorder = models.IntegerField(default=0, verbose_name="司机订单")

    def __str__(self):
        return self.number

    def get(self):
        context = {
            "number": self.number,
            "name": self.name,
            "detail": self.detail,
            "photo": self.photo,
            "car": self.car,
            "money": self.money,
            "score": self.score,
            "corder": self.corder,
            "dorder": self.dorder,
        }
        return context

    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name
