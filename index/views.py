from django.shortcuts import render,redirect


def index(request):
    if request.session.get("number")!=None:
        return redirect("/map/")
    return render(request, "index.html")
