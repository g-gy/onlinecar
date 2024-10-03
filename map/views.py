from django.shortcuts import render, redirect
from user.models import user
from order.models import order


def mapview(request):

    number = request.session.get("number")
    type = request.session.get("type")
    message = request.session.get("message")
    context = {
        "message": message,
        "type": type,
    }
    request.session["message"] = None
    # 获取用户信息
    try:
        this_user = user.objects.filter(number=number).first()
        context.update(this_user.get())
    except:
        
        return render(request, "index.html")

    # 获取进行中的订单的信息
    if type == "0":
        this_order = order.objects.filter(customer=number, stage__lt=3)
    else:
        this_order = order.objects.filter(driver=number, stage__lt=3)
    if this_order:
        this_order = this_order.first()
        if(this_order.driver):
            this_driver=user()
            try:
                this_driver = user.objects.filter(number=this_order.driver).first()
                context["ddriver"]=this_driver.get()
            except:pass
        context.update(this_order.get())
        context["stage"] = this_order.stage
    else:
        context["stage"] = 3
    context["ts"] = int(context["type"]) * 4 + int(context["stage"])
    return render(request, "map.html", context)
