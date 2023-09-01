# Generated by Django 4.1.7 on 2023-08-28 15:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0003_remove_userinfo_depart_id_userinfo_depart"),
    ]

    operations = [
        migrations.CreateModel(
            name="Prettynumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.CharField(max_length=11, verbose_name="手机号")),
                ("price", models.IntegerField(default=0, verbose_name="价格")),
                (
                    "level",
                    models.SmallIntegerField(
                        choices=[(1, "1级用户"), (2, "2级用户"), (3, "3级用户"), (4, "4级用户")],
                        verbose_name="等级",
                    ),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(1, "占用"), (2, "未占用")], verbose_name="状态"
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="create_time",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 8, 28, 23, 37, 39, 886878),
                verbose_name="入职时间",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="depart",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app01.department",
                verbose_name="部门",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="gender",
            field=models.SmallIntegerField(
                choices=[(1, "男"), (2, "女")], verbose_name="性别"
            ),
        ),
    ]
