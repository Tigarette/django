import re
import os
import mimetypes
import time
from wsgiref.util import FileWrapper
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from draw.models import *

video_path = "\\\\10.0.38.10\Vedio"


def video(request, par, type, id):
    user = request.user
    path = os.path.join(par, type, id)
    if not id.endswith('.mp4'):
        f = open(os.path.join(video_path, path), 'rb')
        response = HttpResponse(f, content_type='application/octet-stream')  # 文件流类型
        response['Content-Disposition'] = 'attachment; filename={}'.format(id)  # 表示带有文件附件，指定了文件名；浏览器会自动下载
        return response

    return render(request, 'video/video.html', {
        "user": user,
        "par": par,
        "type": type,
        "id": id
    })


def file_iterator(file_name, chunk_size=1048576, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def stream_video(request, par, type, id):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)  # 使匹配大小写不敏感
    range_match = range_re.match(range_header)
    path = os.path.join(video_path, par, type, id)
    size = os.path.getsize(path)  # 文件总大小
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 10  # 设定一次读取10兆
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206,
                                     content_type=content_type)  # 流式传播
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)  # 按此长度来显示返回的内容
    resp['Accept-Ranges'] = 'bytes'
    return resp


def get_dir(path):
    dirs = []
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            dirs.append(i)
    return dirs


def index(request):
    if request.method == 'GET':
        user = request.user
        type_list = get_dir(video_path)
        paginator = Paginator(type_list, 16)
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

        return render(request, 'video/index.html', {
            'user': user,
            "type_list": type_list,
            "paginator": paginator,
            "curuent_page": curuent_page,
            "curuent_page_num": curuent_page_num,
            "pag_range": pag_range,
        })


def get_files(path):
    files = []
    for i in os.listdir(path):
        if not os.path.isdir(os.path.join(path, i)):
            files.append(i)
    return files


def typeView(request, id):
    if request.method == 'GET':
        user = request.user
        # type_list = VideoType.objects.filter(superior_id=id)
        res = dict()
        dirs = get_dir(os.path.join(video_path, id))
        for i in dirs:
            res[i] = get_files(os.path.join(video_path, id, i))
        return render(request, 'video/intype.html', {
            'user': user,
            'video_type': res,
            'par': id,
        })


@csrf_exempt
def addTime(request, currentTime):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        getTime = data['time']
        if int(getTime) != 5:
            return HttpResponse('error')
        user = request.user
        user.time += int(getTime)
        user.save()
        return HttpResponse('success')


def get_time(ss):
    hh = ss // 3600
    mm = (ss % 3600) // 60
    ss %= 60
    res = ""
    if hh != 0:
        res += str(hh) + "小时"
    if mm != 0:
        res += str(mm) + "分钟"
    return res + str(ss) + "秒"


def rankList(request):
    if request.method == 'GET':
        user = request.user
        user_list = MyUser.objects.order_by('-time')[:]
        for i in user_list:
            i.time = get_time(int(i.time))
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
        # print(liked_user_list)
        return render(request, 'video/ranklist.html', {
            'user': user,
            "user_list": liked_user_list,
            "paginator": paginator,
            "pag_num": pag_num,
            "curuent_page": curuent_page,
            "curuent_page_num": curuent_page_num,
            "pag_range": pag_range,
        })
