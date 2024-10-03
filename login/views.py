from django.shortcuts import render, redirect
from user.models import user


def login(request):
    context = {}
    if request.method == "POST":
        try:
            number = request.POST.get("number")
            password = request.POST.get("password")
            type = request.POST.get("type")
        except:
            context["message"] = "请输入信息"
            return render(request, "login.html", context)
        this_user = user.objects.filter(number=number, password=password).first()
        if this_user == None:
            context["message"] = "账号或密码错误"
            return render(request, "login.html", context)
        request.session["type"] = type
        request.session["number"] = this_user.number
        return redirect("/map/")

    return render(request, "login.html")

def register(request):
    context = {}
    if request.method == "POST":
        number = request.POST.get("number")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        this_user = user.objects.filter(number=number).first()
        if this_user:
            message = "该账号已经被注册，请重新输入"
            return render(request, "register.html", context)
        if password != repassword:
            message = "两次输入密码不同"
            return render(request, "register.html", context)
        this_user = user()
        this_user.number = number
        this_user.password = password
        this_user.save()
        return redirect("/index/")
    return render(request, "register.html")


def change(request):
    context = {}
    if request.method == "POST":
        number = request.POST.get("number")
        password = request.POST.get("password")
        newpassword = request.POST.get("newpassword")
        repassword = request.POST.get("repassword")
        this_user = user.objects.filter(number=number, password=password).first()
        if this_user == None:
            context["message"] = "账号或密码错误"
            return render(request, "change.html", context)
        if newpassword != repassword:
            context["message"] = "两次输入密码不同"
            return render(request, "change.html", context)
        this_user.number = number
        this_user.password = newpassword
        this_user.save()
        return redirect("/index/")
    return render(request, "change.html")


def logout(request):
    request.session.flush()
    return redirect("/index/")
