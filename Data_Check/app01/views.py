from django.shortcuts import render ,HttpResponse,redirect
from .models import UserInfo,Department



def index(request):
    return HttpResponse("Hello World")


def user(request):
    #获取数据库中的所有用户信息
    users = UserInfo.objects.all()
    for i in users:
        print(i.name,i.password,i.age)
    return render(request,"user.html",{"users":users})

def user_add(request):
    if request.method == "GET":
        return render(request,"user_add.html")
    
    name = request.POST.get("user")
    password = request.POST.get("password")
    age = request.POST.get("age")
    account = request.POST.get("account")
    department = request.POST.get("department")
    UserInfo.objects.create(name=name,password=password,age=age,account=account,department=department)


    UserInfo.objects.create(name=name,password=password,age=age)
    return redirect("/user/")


def user_del(request):
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/")

def depart(request):
    return render(request,"depart.html")