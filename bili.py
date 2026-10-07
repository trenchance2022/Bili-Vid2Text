import os
import re

import yt_dlp


def clean_bilibili_url(url):
    """清洗 B 站 URL，去掉追踪参数，避免触发安全拦截。"""
    match = re.match(r"(https?://www\.bilibili\.com/video/[a-zA-Z0-9]+)", url)
    if match:
        return match.group(1)
    return url


def downloaded_filepaths(info):
    paths = []
    for item in info.get("requested_downloads") or []:
        paths.append(item["filepath"])
    for entry in info.get("entries") or []:
        if not entry:
            continue
        for item in entry.get("requested_downloads") or []:
            paths.append(item["filepath"])
    if not paths:
        raise RuntimeError("下载结束，但是没有得到视频文件路径")
    resolved = []
    for path in paths:
        if not os.path.isfile(path):
            raise RuntimeError(f"下载结束但文件不存在: {path}")
        resolved.append(os.path.abspath(path))
    return resolved


def download_bilibili_video(url, output_dir="./downloads"):
    os.makedirs(output_dir, exist_ok=True)
    cleaned_url = clean_bilibili_url(url)
    print(f"解析并清洗后的链接: {cleaned_url}")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "nocheckcertificate": True,
        "http_headers": {
            "Origin": "https://www.bilibili.com",
            "Referer": "https://www.bilibili.com/",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        },
        # 如果依然被 412 拦截，可以改用本地浏览器的 Cookie
        # "cookiesfrombrowser": ("chrome",),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(cleaned_url, download=True)

    filepaths = downloaded_filepaths(info)
    for filepath in filepaths:
        print(f"下载完成: {filepath}")
    return filepaths


if __name__ == "__main__":
    print("=" * 40)
    print("         Bilibili 视频下载脚本")
    print("=" * 40)
    video_url = input("请输入B站视频链接: ").strip()
    if not video_url:
        raise ValueError("输入的链接不能为空。")
    download_bilibili_video(video_url)
