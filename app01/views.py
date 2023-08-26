from django.shortcuts import render ,HttpResponse,redirect
from .models import UserInfo,Department
from django import forms


def index(request):
    return HttpResponse("Hello World")


def user(request):
    #获取数据库中的所有用户信息
    users = UserInfo.objects.all()
    for i in users:
        print(i.name,i.password,i.age)
    return render(request,"user.html",{"users":users})

class UserModelForm(forms.ModelForm):

    #判断输入字符长度
    name = forms.CharField(label="姓名",max_length=10)
    
    #input框定义样式
    class Meta:
        model = UserInfo
        fields = ['name','password','age','account','create_time','gender','depart']

    def __init__(self,*args,**kwarges):
        super().__init__(*args,**kwarges)
        for name,field in self.fields.items():
            field.widget.attrs = {"class":"form-control"}

def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request,"user_add.html",{"form":form})

    #post校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)

        #保存数据
        form.save()
        return redirect("/user/")
    
    #校验失败
    return render(request,"user_add.html",{"form":form})


def user_del(request):
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/")

def user_edit(request,nid):
    #修改用户信息
    row_obj = UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(instance=row_obj)
    if request.method == "GET":
        return render(request,"user_edit.html",{"form":form})
    
    #修改用户信息
    form = UserModelForm(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/user/")


#部门
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