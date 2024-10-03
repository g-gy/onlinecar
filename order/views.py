from django.shortcuts import render, redirect
from user.models import user
from order.models import order


def orderview(request):

    number = request.session.get("number")
    type = request.session.get("type")
    message = request.session.get("message")
    context = {
        "message": message,
        "type": type,
    }
    request.session["message"] = None
    this_user = user.objects.filter(number=number).first()
    context.update(this_user.get())
    if type == "0":
        context["orders"] = order.objects.filter(customer=number).all()
    else:
        context["orders"] = order.objects.filter(driver=number).all()
    return render(request, "order.html", context)


def placeorder(request):
    number = request.session.get("number")
    this_user = user.objects.filter(number=number).first()
    number = this_user.number
    if request.method == "POST":
        startlocation = request.POST.get("startlocation")
        start = request.POST.get("start")
        endlocation = request.POST.get("endlocation")
        end = request.POST.get("end")
        starttime = request.POST.get("starttime").replace("T", " ")
        distance = request.POST.get("distance")
        tolls = request.POST.get("tolls")

        this_order = order()
        this_order.customer = number
        this_order.startlocation = startlocation
        this_order.start = start
        this_order.endlocation = endlocation
        this_order.end = end
        this_order.starttime = starttime
        this_order.stage = 0
        this_order.distance = str_to_float(distance)
        this_order.tolls = str_to_float(tolls)
        this_order.save()
        return redirect("/map/")


def func1(order_list):
    for this_order in order_list:
        this_order.tolls = 0
    return order_list


def func2(
    order_list,
):
    return order_list


def func3(order_list):
    return order_list


def getorder(request):
    number = request.session.get("number")
    order_list = order.objects.filter(stage=0)

    if request.method == "POST":
        this_order = order_list.first()
        startlocation = request.POST.get("startlocation")
        time = request.POST.get("starttime").replace("T", " ")
        checkbox_values = request.POST.getlist("type[]")
        if len(checkbox_values) == 0:
            pass
        else:
            if checkbox_values[0] != "1":
                order_list = func1(order_list)
            for value in checkbox_values:
                if int(value) == 2:
                    order_list = func2(order_list, startlocation)
                if int(value) == 3:
                    order_list = func3(order_list, time)
            id = getmax(order_list)
            this_order = order.objects.filter(id=id).first()
        if this_order == None:
            request.session["message"] = "暂无订单，请耐心等待"
            return redirect("/map/")
        this_order.driver = number
        this_order.stage = 1
        this_order.save()

        return redirect("/map/")


def startorder(request):
    number = request.session.get("number")
    this_user = user.objects.filter(number=number).first()
    number = this_user.number
    this_order = order.objects.filter(driver=number, stage=1).first()
    if request.method == "POST":
        phone = request.POST.get("phone")
        if phone == this_order.customer[-4:]:
            starttime = request.POST.get("starttime").replace("T", " ")
            this_order.starttime = starttime
            this_order.driver = number
            this_order.stage = 2
            this_order.save()
            return redirect("/map/")
        else:
            request.session["message"] = "输入错误，请重新输入"
            return redirect("/map/")


def endorder(request):

    number = request.session.get("number")
    this_order = order.objects.filter(customer=number, stage=2).first()
    customer = user.objects.filter(number=this_order.customer).first()
    if float(customer.money) < float(this_order.tolls):
        request.session["message"] = "余额不足，请充值"
        return redirect("/map/")
    if request.method == "POST":
        this_order.mark = request.POST.get("mark")
        this_order.endtime = request.POST.get("endtime").replace("T", " ")
        this_order.stage = 3
        this_order.save()

        customer.money = round(float(customer.money) - float(this_order.tolls),2)
        customer.corder = customer.corder + 1
        customer.save()
        driver = user.objects.filter(number=this_order.driver).first()
        driver.money = round(float(driver.money) + float(this_order.tolls), 2)
        driver.score = float(driver.score) + float(this_order.mark)
        driver.dorder = driver.dorder + 1
        driver.save()
        return redirect("/map/")


def ccorder(request):
    if request.method == "POST":
        number = request.session.get("number")
        type = request.session.get("type")
        if type == "0":
            this_order = order.objects.filter(customer=number, stage__lt=3).first()
            this_order.stage = 4
            this_order.endtime = "已取消订单"
            this_order.save()

        else:
            this_order = order.objects.filter(driver=number, stage__lt=3).first()
            this_order.stage = 0
            this_order.driver = "未接单"
            this_order.save()
    return redirect("/map/")


def str_to_float(s):
    import re

    match = re.search(r"\d+\.?\d*", s)
    if match:
        return float(match.group())
    else:
        return None


def func1(order_list):
    for this_order in order_list:
        this_order.tolls = 0
    return order_list


def func2(order_list, location):
    for this_order in order_list:
        this_order.tolls = this_order.tolls - location_tolls(
            this_order.startlocation, location
        )
    return order_list


def func3(order_list, time):
    for this_order in order_list:
        this_order.tolls = this_order.tolls + time_tolls(this_order.starttime, time)
    return order_list


def getmax(order_list):
    max = -9223372036854775808
    id = 0
    this_order = order()
    for this_order in order_list:
        if this_order.tolls > max:
            max = this_order.tolls
            id = this_order.id
    return id


def location_tolls(coord_str1, coord_str2):
    from math import radians, cos, sin, asin, sqrt

    lon1, lat1 = map(float, coord_str1.split(","))
    lon2, lat2 = map(float, coord_str2.split(","))
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    distance = c * r
    earnings = distance * 2
    return earnings


def time_tolls(time_str1, time_str2):
    from datetime import datetime

    time_format = "%Y-%m-%d %H:%M"
    time1 = datetime.strptime(time_str1, time_format)
    time2 = datetime.strptime(time_str2, time_format)
    delta = time2 - time1
    difference_in_minutes = delta.total_seconds() / 60
    return difference_in_minutes * 0.5
