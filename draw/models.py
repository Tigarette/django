from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Create your models here.


class DrawQuestion(models.Model):
    draw_question_text = models.CharField(max_length=100)
    get_boom_num = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.draw_question_text


class MyUser(AbstractUser):
    likes = models.PositiveIntegerField("喜欢", default=0, editable=False)
    boom_num = models.IntegerField(default=0)
    nick_name = models.CharField(max_length=10)
    add_draw = models.CharField(max_length=10)
    give_power = models.CharField(max_length=10)


class DrawChoice(models.Model):
    draw_choice_text = models.CharField(max_length=100)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question = models.ForeignKey(DrawQuestion, on_delete=models.CASCADE)
    boom = models.IntegerField(default=-1)
    flag = models.IntegerField(default=0)
    disable = models.BooleanField(default=False)

    def __str__(self):
        return self.draw_choice_text


class EmailPro(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=10, choices=(('register', '邮箱注册'), ('forget', '忘记密码')), verbose_name='发送类型')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        db_table = 'emailpro'
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name


class UpdateLog(models.Model):
    log_text = models.TextField(max_length=10000000)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.log_text


class LikeNum(models.Model):
    user = models.ForeignKey(MyUser, null=True, on_delete=models.SET_NULL, related_name='Like_id')
    liked_user = models.ForeignKey(MyUser, null=True, on_delete=models.SET_NULL, related_name='Liked_id')

    class Meta:
        verbose_name_plural = 'user'
