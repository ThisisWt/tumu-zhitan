import requests
from bs4 import BeautifulSoup

def get_image_url(url):
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    # 确保请求成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找id为"imgPath"的<img>标签
        img_tag = soup.find('img', id='imgPath')
        # 提取<img>标签中的src属性，即图片的URL
        if img_tag:
            img_url = img_tag['src']
            # 确保图片URL是完整的，如果只是相对路径则补全
            if not img_url.startswith(('http:', 'https:')):
                img_url = 'https://weather.cma.cn/' + img_url
            return img_url
        else:
            print("没有找到id为'imgPath'的图片标签")
            return None
    else:
        print(f"请求网页失败，状态码：{response.status_code}")
        return None

def download_image(image_url, local_image_path):
    # 发起GET请求下载图片
    response = requests.get(image_url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 将图片数据写入到本地文件
        with open(local_image_path, 'wb') as file:
            file.write(response.content)
        print(f"图片已成功下载并保存至：{local_image_path}")
    else:
        print("图片下载失败，状态码：", response.status_code)

def DownloadClimateImg(path):
    # 目标网页URL
    target_url = "https://weather.cma.cn/web/channel-32.html"
    # 调用函数获取图片URL
    image_url = get_image_url(target_url)
    if image_url:
        print(f"图片URL为: {image_url}")
        # 指定保存图片的本地路径
        # local_image_path = "气温.jpg"  # 根据图片实际类型调整文件名及扩展名
        # 下载图片
        download_image(image_url, path)
    else:
        print("未能获取图片URL，无法下载图片。")

basepath = r"D:\Django\myproject\MYApp\static\media/"

target_url = "https://weather.cma.cn/web/channel-32.html"
    # 调用函数获取图片URL
image_url = get_image_url(target_url)
if image_url:
    print(f"图片URL为: {image_url}")
        # 指定保存图片的本地路径
    local_image_path = basepath + "气温.jpg"  # 根据图片实际类型调整文件名及扩展名
        # 下载图片
    download_image(image_url, local_image_path)
else:
        print("未能获取图片URL，无法下载图片。")


# 目标网页URL
target_url = "https://weather.cma.cn/web/channel-45.html"
# 调用函数获取图片URL
image_url = get_image_url(target_url)
if image_url:
    print(f"图片URL为: {image_url}")
    # 指定保存图片的本地路径
    local_image_path = basepath + "土壤水分.jpg"  # 根据图片实际类型调整文件名及扩展名
    # 下载图片
    download_image(image_url, local_image_path)
else:
    print("未能获取图片URL，无法下载图片。")

target_url = "https://weather.cma.cn/web/channel-18.html"
# 调用函数获取图片URL
image_url = get_image_url(target_url)
if image_url:
    print(f"图片URL为: {image_url}")
    # 指定保存图片的本地路径
    local_image_path = basepath + "降水量.jpg"  # 根据图片实际类型调整文件名及扩展名
    # 下载图片
    download_image(image_url, local_image_path)
else:
    print("未能获取图片URL，无法下载图片。")

target_url = "https://weather.cma.cn/web/channel-339.html"
# 调用函数获取图片URL
image_url = get_image_url(target_url)
if image_url:
    print(f"图片URL为: {image_url}")
    # 指定保存图片的本地路径
    local_image_path = basepath + "天气预报.jpg"  # 根据图片实际类型调整文件名及扩展名
    # 下载图片
    download_image(image_url, local_image_path)
else:
    print("未能获取图片URL，无法下载图片。")

target_url = "https://weather.cma.cn/web/channel-2b0863600e144b13807e606f928b1266.html"
# 调用函数获取图片URL
image_url = get_image_url(target_url)
if image_url:
    print(f"图片URL为: {image_url}")
    # 指定保存图片的本地路径
    local_image_path = basepath + "卫星云图.jpg"  # 根据图片实际类型调整文件名及扩展名
    # 下载图片
    download_image(image_url, local_image_path)
else:
    print("未能获取图片URL，无法下载图片。")