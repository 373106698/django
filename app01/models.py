from typing import Any
from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.




class UserInfo(models.Model):
    """用户表"""
    name = models.CharField(verbose_name="姓名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄",default=0)
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")   #default=timezone.now ,default=datetime.now()


    #有关联的
    # -to 与哪张表关联
    # -to_field 与表中的列关联
    #生成数据列 depart_id
    

    #1.部门id置空
    # on_delete=models.CASCADE,null=True,blank=True 
    # 2.部门删除;
    # on_delete=models.CASCADE删除用户 
    depart = models.ForeignKey(verbose_name='部门',to="Department",to_field="id",on_delete=models.SET_NULL,null=True,blank=True)

    gender_choices = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)



class Department(models.Model):
    """"部门表"""
    title = models.CharField(verbose_name="部门",max_length=32)

    #返回对象
    def __str__(self):
        return self.title

class Prettynumber(models.Model):
    """号码池"""
    phone = models.CharField(verbose_name="手机号",max_length=11)
    price = models.IntegerField(verbose_name="价格",default=0)


    level_choices = (
        (1,"1级用户"),  
        (2,"2级用户"),
        (3,"3级用户"),
        (4,"4级用户"),
        )
    level = models.SmallIntegerField(verbose_name="等级",choices=level_choices)

    status_choices = (
        (1,"占用"),
        (2,"未占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices)
    
    #返回对象
    def __str__(self):
        return self.phone
