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
    #获取数据库中的所有部门信息
    departments = Department.objects.all()
    return render(request,"depart.html",{'departments':departments})


def depart_add(request):
    if request.method == "GET":
        return render(request,"depart_add.html")
    
    #添加部门
    title = request.POST.get("title")
    Department.objects.create(title=title)

    #重定向回部门列表
    return redirect("/depart/")


def depart_del(request):
    #删除ID部门
    nid = request.GET.get("nid")
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/")


def depart_edit(request,nid):
    #编辑部门
    #根据nid 获取数据第一条
    if request.method == "GET":
        row_obj = Department.objects.filter(id=nid).first()
        return render(request,"depart_edit.html",{"row_obj":row_obj})
    
    #修改部门
    title = request.POST.get("title")
    Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/")