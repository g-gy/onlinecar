from django.db import models


class order(models.Model):

    stagechoice = (
        (0, "接单前"),
        (1, "接客前"),
        (2, "结单前"),
        (3, "已结束"),
    )

    customer = models.CharField(max_length=15)
    driver = models.CharField(max_length=15, null=True, default="未接单")

    startlocation = models.CharField(max_length=20)
    endlocation = models.CharField(max_length=20)

    start = models.CharField(max_length=20, null=True)
    end = models.CharField(max_length=20, null=True)

    starttime = models.CharField(max_length=20)
    endtime = models.CharField(max_length=20, null=True, default="未完成")

    distance = models.FloatField(null=True)
    tolls = models.FloatField(null=True)
    mark = models.FloatField(null=True, default=0)

    stage = models.IntegerField(choices=stagechoice, default=0)

    def get(self):
        context = {
            "customer": self.customer,
            "driver": self.driver,
            "startlocation": self.startlocation,
            "endlocation": self.endlocation,
            "start": self.start,
            "end": self.end,
            "starttime": self.starttime,
            "endtime": self.endtime,
            "tolls": self.tolls,
            "mark": self.mark,
            "stage": self.stage,
            "distance":self.distance,
        }
        return context

    class Meta:
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name
