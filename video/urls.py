from django.urls import path
from . import views

app_name = "video"
urlpatterns = [
    path('', views.index, name='index'),
    path('addTime/<str:currentTime>', views.addTime, name='addTime'),
    path('ranklist/', views.rankList, name='rankList'),
    path('<str:id>/', views.typeView, name='type'),
    # video/是播放视频的页面
    path('watch/<str:par>/<str:type>/<str:id>', views.video, name='watch'),
    # 这里的<arg_path>作为第二个参数传递到stream_video函数中去，意义就是视频文件的路径名
    path('stream/<str:par>/<str:type>/<str:id>', views.stream_video, name='videopath'),

]
