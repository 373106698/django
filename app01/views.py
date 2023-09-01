from django.shortcuts import render ,HttpResponse,redirect
from .models import UserInfo,Department,Prettynumber
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.pagination import Pagination

def index(request):
    return HttpResponse("Hello World")


def user(request):
    #获取数据库中的所有用户信息
    queryset = UserInfo.objects.all()

    page_object = Pagination(request,queryset)

    context = {

        "queryset":page_object.page_queryset,#分完页的数据
        "page_string":page_object.html() #页码
    }

    return render(request,"user.html",context)

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
    #添加用户
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
    #删除用户信息
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/")

def user_edit(request,nid):
    #修改用户信息
    row_obj = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_obj)
        return render(request,"user_edit.html",{"form":form})
        
    form = UserModelForm(data=request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/user/")
    #校验失败
    return render(request,"user_add.html",{"form":form})

#部门
def depart(request):
    #获取数据库中的所有部门信息
    queryset = Department.objects.all()
    
    page_object = Pagination(request,queryset)

    context = {

        "queryset":page_object.page_queryset,#分完页的数据
        "page_string":page_object.html() #页码
    }



    return render(request,"depart.html",context)


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



#靓号
def number(request):
    #号码列表


    data_dict={}
    search_data = request.GET.get("q",'')
    
    print(search_data)

    if search_data:
        data_dict["phone__contains"] = search_data

    queryset = Prettynumber.objects.filter(**data_dict).order_by("-level")
    
    page_object = Pagination(request,queryset)

    context = {
        "search_data":search_data,

        "queryset":page_object.page_queryset,#分完页的数据
        "page_string":page_object.html() #页码
    }

    return render(request,"number.html",context)




class PhoneModelForm(forms.ModelForm):

    #判断输入格式
    phone = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    #input框定义样式
    class Meta:
        model = Prettynumber
        fields = ['phone','price','level','status']

    def __init__(self,*args,**kwarges):
        super().__init__(*args,**kwarges)
        for name,field in self.fields.items():
            field.widget.attrs = {"class":"form-control"}
    # 钩子方法校验
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        #判断手机号是否重复
        if Prettynumber.objects.filter(phone=phone).exists():
            raise ValidationError("手机号已存在")
        return phone

#新建号码
def pretty_add(request):
    if request.method == "GET":
        form = PhoneModelForm
        return render(request,"number_add.html",{"form":form})
    
    #新建号码
    form = PhoneModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("/number/")
    return render(request,"number_add.html",{"form":form})




class PhoneeditModelForm(forms.ModelForm):

    #判断输入格式
    phone = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    #input框定义样式
    class Meta:
        model = Prettynumber
        fields = ['phone','price','level','status']

    def __init__(self,*args,**kwarges):
        super().__init__(*args,**kwarges)
        for name,field in self.fields.items():
            field.widget.attrs = {"class":"form-control"}
    # 钩子方法校验
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        #判断手机号是否重复

        #排查自身以外的id
        if Prettynumber.objects.exclude(id=self.instance.pk).filter(phone=phone).exists():
            raise ValidationError("手机号已存在")
        return phone



#编辑号码
def pretty_edit(request,nid):

    #获取表单
    row_obj = Prettynumber.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PhoneeditModelForm(instance=row_obj)
        return render(request,"number_edit.html",{"form":form})
    #编辑号码
    form = PhoneeditModelForm(request.POST,instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/number/")
    #校验失败
    return render(request,"number_edit.html",{"form":form})


#删除号码
def pretty_del(request,nid):
    Prettynumber.objects.filter(id=nid).delete()
    return redirect("/number/")
