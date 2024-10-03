from django.conf import settings
from django.shortcuts import render, redirect
from user.models import user
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from pay.views import alipay_pay


def userview(request):
    number = request.session.get("number")
    type = request.session.get("type")
    message = request.session.get("message")
    context = {
        "message": message,
        "type": type,
    }
    request.session["message"] = None
    this_user = user.objects.filter(number=number).first()
    if request.method == "POST":
        if request.POST.get("name"):
            this_user.name = request.POST.get("name")
            this_user.car = request.POST.get("car")
            this_user.detail = request.POST.get("detail")

        elif request.POST.get("addmoney"):
            if request.POST.get("addmoney") != "0":
                request.session["money"] = request.POST.get("addmoney")
                return HttpResponseRedirect(alipay_pay(request))

            if request.POST.get("submoney") != "0":
                this_user.money = round(
                    this_user.money - float(request.POST.get("submoney")), 2
                )

        this_user.save()
    context.update(this_user.get())
    context["money"] = this_user.money
    if this_user.dorder != 0:
        context["score"] = this_user.score / this_user.dorder
    else:
        context["score"] = this_user.score
    return render(request, "user.html", context)


def upload(request):
    number = request.session.get("number")
    type = request.session.get("type")
    message = request.session.get("message")
    context = {
        "message": message,
        "type": type,
    }

    if request.FILES.get("photo") == None:
        request.session["message"] = "请添加图片"
        return redirect("/user/")
    this_user = user.objects.filter(number=number).first()
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    name = number + ".jpg"
    if fs.exists(name):
        fs.delete(name)
    photo = fs.save(name, request.FILES.get("photo"))
    this_user.photo = photo
    this_user.save()
    return redirect("/user/")
