# Django
> 基于Django开发的抽签与视频网课平台
## 更新日志

>2022年6月16日 增加点赞功能  
2022年6月15日 增加抽签项目分页功能  
2022年6月16日 增加更新日志功能  
2022年7月10日 增加排行榜分页功能  
2022年7月27日 正式上线在线视频播放功能  

## 基于Docker运行本项目
### 构建
```bash
docker build -t hnie:viedo . 
```
### 运行
```bash
docker run --name video -d \
  -p 8000:8000 \
  -v "$PWD":/usr/src/app \
  -v /mnt/dsm:/mnt/dsm \ #共享目录
  hnie:video
```