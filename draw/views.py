from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import DrawQuestion, DrawChoice, MyUser, EmailPro, UpdateLog, LikeNum
import random
from django.utils import timezone
import sqlite3
from django.core.mail import send_mail
from chouqian.settings import EMAIL_FROM
from django.core.paginator import Paginator
from django.db.models import F
import os


# Create your views here.


def index(request):
    user_list = MyUser.objects.order_by('-boom_num')[:]
    log_list = UpdateLog.objects.order_by('-pub_date')[:]
    log = ""
    if log_list:
        log = log_list[0]
    user = request.user
    liked_user_list = list()
    if LikeNum.objects.filter(user_id=user.id):
        data = LikeNum.objects.filter(user_id=user.id)
        for user1 in user_list:
            flag = False
            for liked in data:
                if liked.liked_user_id == user1.id:
                    liked_user_list.append({
                        "user": user1,
                        'msg': '1'
                    })
                    flag = True
                    break
            if not flag:
                liked_user_list.append({
                    "user": user1,
                })
        paginator = Paginator(liked_user_list, 12)
        pag_num = paginator.num_pages
        curuent_page_num = int(request.GET.get('page', 1))
        curuent_page = paginator.page(curuent_page_num)
        if pag_num < 11:
            pag_range = paginator.page_range
        elif pag_num > 11:
            if curuent_page_num < 6:
                pag_range = range(1, 11)
            elif curuent_page_num > paginator.num_pages - 5:
                pag_range = range(pag_num - 9, pag_num + 1)
            else:
                pag_range = range(curuent_page_num - 5, curuent_page_num + 5)
        return render(request, 'draw/index.html', {
            'log': log,
            'liked_user_list': liked_user_list,
            "paginator": paginator,
            "curuent_page": curuent_page,
            "curuent_page_num": curuent_page_num,
            "pag_range": pag_range,
        })
    else:
        for user1 in user_list:
            liked_user_list.append({
                "user": user1,
            })
        paginator = Paginator(liked_user_list, 12)
        pag_num = paginator.num_pages
        curuent_page_num = int(request.GET.get('page', 1))
        curuent_page = paginator.page(curuent_page_num)
        if pag_num < 11:
            pag_range = paginator.page_range
        elif pag_num > 11:
            if curuent_page_num < 6:
                pag_range = range(1, 11)
            elif curuent_page_num > paginator.num_pages - 5:
                pag_range = range(pag_num - 9, pag_num + 1)
            else:
                 pag_range = range(curuent_page_num - 5, curuent_page_num + 5)
        return render(request, 'draw/index.html', {
            'liked_user_list': liked_user_list,
            'log': log,
            "paginator": paginator,
            "curuent_page": curuent_page,
            "curuent_page_num": curuent_page_num,
            "pag_range": pag_range,
        })


@csrf_exempt
def sign_in(request):
    if request.method == 'GET':
        return render(request, 'draw/login.html')
    elif request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        if username is '' and password is '':
            return HttpResponse("用户名和密码都为空,请检查是否输入")
        elif username is '':
            return HttpResponse("用户名为空,请检查是否输入")
        elif password is '':
            return HttpResponse("密码为空,请检查是否输入")
        if not MyUser.objects.filter(username=username):
            return HttpResponse("该用户不存在")
        user = MyUser.objects.get(username=username)
        if check_password(password, user.password):
            login(request, user)
            return HttpResponse("登录成功")
        else:
            return HttpResponse("账号或密码不正确")


def detail(request):
    latest_question_list = DrawQuestion.objects.order_by('-pub_date')[:]
    paginator = Paginator(latest_question_list, 16)
    pag_num = paginator.num_pages
    curuent_page_num = int(request.GET.get('page', 1))
    curuent_page = paginator.page(curuent_page_num)
    if pag_num < 11:
        pag_range = paginator.page_range
    elif pag_num > 11:
        if curuent_page_num < 6:
            pag_range = range(1, 11)
        elif curuent_page_num > paginator.num_pages - 5:
            pag_range = range(pag_num - 9, pag_num + 1)
        else:
            pag_range = range(curuent_page_num - 5, curuent_page_num + 5)
    template = loader.get_template('draw/drawview.html')
    context = {
        'latest_question_list': latest_question_list,
        "paginator": paginator,
        "curuent_page": curuent_page,
        "curuent_page_num": curuent_page_num,
        "pag_range": pag_range,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def register_view(request):
    if request.method == 'GET':
        return render(request, 'draw/register.html')
    elif request.method == 'POST':
        data = request.POST
        username = data['username']
        nickname = data['nick_name']
        password = data['password']
        re_password = data['re_password']
        email = data['email']
        code = data['code']
        mydb = sqlite3.connect("db.sqlite3")
        cursor = mydb.cursor()
        sql = "SELECT max(id) FROM emailpro WHERE email = ('%s')" % (email)
        cursor.execute(sql)
        get_table = cursor.fetchall()
        list_out_put = [i[0] for i in get_table]
        max_id = list_out_put[0]
        email_code = EmailPro.objects.get(id=max_id).code
        if username is '' or password is '' or re_password is '' or email is '' or nickname is '':
            return HttpResponse("all_empty")
        elif password != re_password:
            return HttpResponse("password_error")
        elif MyUser.objects.filter(username=username):
            return HttpResponse("have_username")
        elif MyUser.objects.filter(email=email):
            return HttpResponse("have_email")
        elif len(password) < 6:
            return HttpResponse("less_password")
        elif code != email_code:
            return HttpResponse("not_code")
        else:
            sql = "DELETE FROM emailpro WHERE code=('%s') AND email=('%s') AND send_type='register';" % (email_code, email)
            cursor.execute(sql)
            mydb.commit()
            user = MyUser()
            user.username = username
            user.password = make_password(password)
            user.nick_name = nickname
            user.email = email
            user.save()
            return HttpResponse("success")


@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponse("success")


def main_html(request):
    print(MyUser.add_draw)
    return render(request, 'draw/main.html')


@csrf_exempt
def add_new_draw(request):
    if request.method == 'GET':
        return render(request, 'draw/add_draw.html')
    elif request.method == 'POST':
        data = request.POST
        draw_name = data['draw_name']
        human_num = int(data['human_num'])
        boom_num = int(data['boom_num'])
        mydb = sqlite3.connect("db.sqlite3")
        cursor = mydb.cursor()
        cursor.execute("SELECT draw_question_text FROM draw_drawquestion;")
        get_table = cursor.fetchall()
        list_out_put = [i[0] for i in get_table]
        if draw_name is '' or human_num is '' or boom_num is '':
            return HttpResponse("empty")
        elif human_num <= 0 or boom_num <= 0:
            return HttpResponse("less_num")
        elif human_num <= int(boom_num):
            return HttpResponse("less_human")
        for i in range(0, len(list_out_put)):
            if list_out_put[i] == draw_name:
                return HttpResponse("same_name")
        draw = DrawQuestion()
        draw.draw_question_text = draw_name
        draw.pub_date = timezone.now()
        draw.save()
        text = ["猜猜是不是我", "其实就是我", "不是我不是我", "是我旁边那个"]
        user = MyUser.objects.get(username='admin')
        mydb = sqlite3.connect("db.sqlite3")
        cursor = mydb.cursor()
        cursor.execute("SELECT max(flag) FROM draw_drawchoice;")
        get_table = cursor.fetchall()
        list_out_put = [i[0] for i in get_table]
        max_flag = list_out_put[0]
        print(max_flag)
        if max_flag is None:
            max_flag = 0
        for i in range(max_flag, human_num + max_flag):
            choice = DrawChoice()
            choice.draw_choice_text = text[random.randint(0, 3)]
            choice.flag = i + 1
            choice.question = draw
            choice.user = user
            choice.save()
        a = []
        i = 1
        b = random.randint(1 + max_flag, human_num + max_flag)
        a.append(b)
        while i != boom_num:
            b = random.randint(1 + max_flag, human_num + max_flag)
            flag = 0
            for j in range(0, len(a)):
                if a[j] == b:
                    break
                else:
                    flag += 1
                if flag == len(a):
                    a.append(b)
                    i += 1
                    break
        for i in range(0, len(a)):
            choice = DrawChoice.objects.get(flag=a[i])
            choice.boom = 1
            choice.save()
        return HttpResponse("success")


@csrf_exempt
def add_power(request):
    if request.method == 'GET':
        return render(request, 'draw/add_power.html')
    elif request.method == 'POST':
        data = request.POST
        username = data['username']
        add_draw = data['add_draw']
        add_power_power = data['add_power']
        if username is '':
            return HttpResponse("name_empty")
        elif not MyUser.objects.filter(username=username):
            return HttpResponse("nobody")
        elif add_draw == "no" and add_power_power == "no":
            return HttpResponse("no_choice")
        user = MyUser.objects.get(username=username)
        if add_draw == "yes":
            user.add_draw = "1"
        if add_power_power == "yes":
            user.give_power = "1"
        user.save()
        return HttpResponse("success")


@csrf_exempt
def draw_begin(request, draw_id):
    if request.method == 'GET':
        draw = DrawQuestion.objects.get(id=draw_id)
        return render(request, 'draw/draw.html', {
            'draw': draw
        })
    elif request.method == 'POST':
        data = request.POST
        choice_id = data['choice_id']
        choice = DrawChoice.objects.get(id=choice_id)
        question = DrawQuestion.objects.get(id=choice.question.id)
        user = request.user

        # 新添加:判断用户是否已经抽过签
        mydb = sqlite3.connect("db.sqlite3")
        cursor = mydb.cursor()
        sql = "SELECT user_id FROM draw_drawchoice where question_id = ('%s')" % (question.pk)
        cursor.execute(sql)
        get_table = cursor.fetchall()
        list_out_put = [i[0] for i in get_table]
        for choice_user in list_out_put:
            if choice_user == user.id and choice_user != 1:
                return HttpResponse("is_choice")

        if choice.boom == 1:
            choice.draw_choice_text = "恭喜" + user.nick_name + "中奖"
            user.boom_num += 1
            question.get_boom_num += 1
        else:
            choice.draw_choice_text = "唉," + user.nick_name + "没有中奖"
        choice.user_id = user.id
        choice.disable = True
        question.save()
        user.save()
        choice.save()
        return HttpResponse("success")


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


@csrf_exempt  # 新添加
def send_register_email(request):  # 类型为注册
    email = request.POST['email']
    send_type = request.POST['type']
    email_title = ''
    email_body = ''
    if send_type == 'register':
        if email is '':
            return HttpResponse("empty")
        elif '@' not in email:
            return HttpResponse("not_email")
        elif MyUser.objects.filter(email=email):
            return HttpResponse("have_user")
        email_recode = EmailPro()
        email_recode.email = email
        email_recode.send_type = send_type
        code = random_str(6)
        email_recode.code = code
        email_recode.save()
        email_title = '超级离谱的抽签网站之邮箱验证'
        email_body = '张竣表示,顾客是上帝,上帝这是你的验证码请查收:{0}'.format(code)
    elif send_type == 'forget':
        if email is '':
            return HttpResponse("empty")
        elif '@' not in email:
            return HttpResponse("not_email")
        email_recode = EmailPro()
        email_recode.email = email
        email_recode.send_type = send_type
        code = random_str(8)
        email_recode.code = code
        email_recode.save()
        email_title = '超级离谱的抽签网站之忘记密码'
        email_body = '密码都能忘记?张竣大发慈悲给了你一串验证码并且非常鄙视你:{0}'.format(code)
    elif send_type == 'change':
        if email is '':
            return HttpResponse("empty")
        elif '@' not in email:
            return HttpResponse("not_email")
        elif MyUser.objects.filter(email=email):
            user = MyUser.objects.filter(email=email)
            if user[0].username == request.POST['username']:
                pass
            else:
                return HttpResponse("have_user")
        email_recode = EmailPro()
        email_recode.email = email
        email_recode.send_type = send_type
        code = random_str(4)
        email_recode.code = code
        email_recode.save()
        email_title = '超级离谱的抽签网站之修改信息'
        email_body = '要修改信息是吧.张竣知道你要修改信息于是给了你一个验证码:{0}'.format(code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    return HttpResponse("success")


@csrf_exempt
def forget_psw(request):
    if request.method == 'GET':
        return render(request, 'draw/forget.html')
    elif request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        re_password = data['re_password']
        email = data['email']
        code = data['code']
        mydb = sqlite3.connect("db.sqlite3")
        cursor = mydb.cursor()
        sql = "SELECT max(id) FROM emailpro WHERE email = ('%s')" % (email)
        cursor.execute(sql)
        get_table = cursor.fetchall()
        list_out_put = [i[0] for i in get_table]
        max_id = list_out_put[0]
        email_code = EmailPro.objects.get(id=max_id).code
        if username is '' or password is '' or re_password is '' or email is '' or code is '':
            return HttpResponse("all_empty")
        elif password != re_password:
            return HttpResponse("password_error")
        elif not MyUser.objects.filter(username=username):
            return HttpResponse("no_username")
        user = MyUser.objects.get(username=username)
        if user.email != email:
            return HttpResponse("no_email")
        elif len(password) < 6:
            return HttpResponse("less_password")
        elif code != email_code:
            return HttpResponse("not_code")
        else:
            sql = "DELETE FROM emailpro WHERE code=('%s') AND email=('%s');" % (email_code, email)
            cursor.execute(sql)
            mydb.commit()
            user.password = make_password(password)
            user.save()
            return HttpResponse("success")


@csrf_exempt  # 新添加
def change_psw(request):
    if request.method == 'GET':
        return render(request, 'draw/change_psw.html')
    elif request.method == 'POST':
        data = request.POST
        print(data)
        username = data['username']
        old_password = data['old_password']
        new_password = data['new_password']
        email = data['email']
        code = data['code']
        if code is not '':
            mydb = sqlite3.connect("db.sqlite3")
            cursor = mydb.cursor()
            sql = "SELECT max(id) FROM emailpro WHERE email = ('%s')" % (email)
            cursor.execute(sql)
            get_table = cursor.fetchall()
            list_out_put = [i[0] for i in get_table]
            max_id = list_out_put[0]
            email_code = EmailPro.objects.get(id=max_id).code
        user = MyUser.objects.get(username=username)
        if old_password is '':
            return HttpResponse('empty')
        elif not check_password(old_password, user.password):
            return HttpResponse('error_psw')
        elif new_password is '' and email is '':
            return HttpResponse('no_change')
        elif new_password is '' and email is not '':
            if email_code != code:
                return HttpResponse('code_error')
            elif check_password(old_password, user.password):
                user.email = email
                user.save()
                return HttpResponse('change_email')
        elif new_password is not '' and email is '':
            if old_password == new_password:
                return HttpResponse('same')
            elif len(new_password) < 6:
                return HttpResponse('less_psw')
            elif check_password(old_password, user.password):
                user.password = make_password(new_password)
                user.save()
                logout(request)
                return HttpResponse('change_psw')
        elif new_password is not '' and email is not '':
            if check_password(old_password, user.password):
                user.password = make_password(new_password)
                user.email = email
                user.save()
                logout(request)
                return HttpResponse('success')


def admin_reg(request):
    if request.method == 'GET':
        return render(request, "draw/admin_reg.html")
    elif request.method == 'POST':
        data = request.POST
        print(data)
        username = data['username']
        print(username)
        psw = data['psw']
        nickname = data['nickname']
        email = data['email']
        user = MyUser()
        user.username = username
        user.password = make_password(psw)
        user.nick_name = nickname
        user.email = email
        user.save()
        return render(request, "draw/admin_reg.html", {
            "msg": "注册成功",
        })


@csrf_exempt
def update_log(request):
    if request.method == "GET":
        log_list = UpdateLog.objects.order_by('-pub_date')[:]
        log = ""
        if log_list:
            log = log_list[0]
        return render(request, 'draw/update_log.html', {
            'log': log,
        })
    elif request.method == "POST":
        data = request.POST
        msg = data['msg']
        print(data, type(msg), sep=' ')
        if msg == "1":
            have_log = data['have_log']
            log_list = UpdateLog.objects.order_by('-pub_date')[:]
            log = log_list[0]
            log.log_text = have_log
        else:
            not_log = data['not_log']
            log = UpdateLog()
            log.log_text = not_log
            log.pub_date = timezone.now()
        log.save()
        return HttpResponse('success')


def user_main(request, username):
    if request.method == 'GET':
        msg = ""
        msg1 = ""
        msg2 = ""
        user_list = MyUser.objects.order_by('-boom_num')[:1]
        latest_question_list = DrawQuestion.objects.order_by('-pub_date')[:]
        like_list = MyUser.objects.order_by('-likes')[:1]
        time_list = MyUser.objects.order_by('-time')[:1]
        question_list = []
        for question in latest_question_list:
            for choice in question.drawchoice_set.all():
                if choice.boom == 1 and choice.user_id == MyUser.objects.get(username=username).id:
                    question_list.append(DrawQuestion.objects.get(id=choice.question_id))
                    break
        if username == time_list[0].username:
            msg2 = "1"
        if username == user_list[0].username:
            msg = "1"
        if username == like_list[0].username:
            msg1 = "1"
        if MyUser.objects.filter(username=username) and MyUser.objects.filter(username=request.user):
            user = MyUser.objects.get(username=username)
            user_now = MyUser.objects.get(username=request.user)
            username = user_now.nick_name
            email = user_now.email
            return render(request, "draw/user_main.html", {
                "user": user,
                "username": username,
                "email": email,
                "msg": msg,
                "question_list": question_list,
                "msg1": msg1,
                "msg2": msg2,
            })
        else:
            user = MyUser.objects.get(username=username)
            return render(request, "draw/user_main.html", {
                "user": user,
                "msg": msg,
                "question_list": question_list,
                "msg1": msg1,
                "msg2": msg2,
            })


@csrf_exempt
def add_likes(request):
    if request.method == 'POST':
        data = request.POST
        like_id = data['like_id']
        liked_id = data['liked_id']
        if like_id == "None":
            return HttpResponse("not_login")
        liked_user = MyUser.objects.get(id=liked_id)
        mydb = sqlite3.connect("db.sqlite3")
        cursor = mydb.cursor()
        sql = "SELECT max(id) FROM draw_likenum;"
        cursor.execute(sql)
        get_table = cursor.fetchall()
        list_out_put = [i[0] for i in get_table]
        print(list_out_put)
        if list_out_put[0]:
            max_id = list_out_put[0]
        else:
            max_id = 0
        sql = "UPDATE sqlite_sequence SET seq = ('%s') WHERE name = 'draw_likenum';" % (max_id)
        cursor.execute(sql)
        mydb.commit()
        if LikeNum.objects.filter(user_id=like_id, liked_user_id=liked_id):
            LikeNum.objects.get(user_id=like_id, liked_user_id=liked_id).delete()
            liked_user.likes = F('likes') - 1
            liked_user.save()
            liked_user = MyUser.objects.get(id=liked_id)
            data = 'not_like+' + str(liked_user.likes)
            return HttpResponse(data)
        else:
            like = LikeNum()
            like.user_id = like_id
            like.liked_user_id = liked_id
            liked_user.likes = F('likes') + 1
            like.save()
            liked_user.save()
            liked_user = MyUser.objects.get(id=liked_id)
            data = 'like+' + str(liked_user.likes)
            return HttpResponse(data)
