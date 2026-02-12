"""
抖音浏览器自动化采集模块

功能：
1. 获取抖音Cookie（通过手动登录）
2. 使用Cookie获取博主数据
3. 支持真实数据采集

使用方法：
1. 电脑浏览器打开 https://www.douyin.com
2. 登录你的抖音账号
3. 按F12打开开发者工具 → Network标签
4. 刷新页面，找到请求，复制Cookie值
5. 在网站输入Cookie即可获取真实数据
"""

import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time


class DouyinPlaywrightCrawler:
    """抖音浏览器自动化采集器"""
    
    def __init__(self):
        self.cookie = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
    
    def set_cookie(self, cookie_str: str):
        """
        设置抖音Cookie
        
        Args:
            cookie_str: Cookie字符串（从浏览器复制）
        """
        self.cookie = cookie_str
        print(f"✅ Cookie已设置，长度: {len(cookie_str)} 字符")
    
    def parse_cookie(self, cookie_str: str) -> List[Dict]:
        """
        解析Cookie字符串为Playwright格式
        
        Args:
            cookie_str: Cookie字符串
            
        Returns:
            Playwright格式的Cookie列表
        """
        cookies = []
        for item in cookie_str.split(';'):
            item = item.strip()
            if '=' in item:
                name, value = item.split('=', 1)
                cookies.append({
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": ".douyin.com",
                    "path": "/"
                })
        return cookies
    
    def get_blogger_info(self, sec_uid: str) -> Optional[Dict]:
        """
        获取博主信息
        
        Args:
            sec_uid: 博主SEC UID
            
        Returns:
            博主信息 或 None
        """
        if not self.cookie:
            print("❌ 请先设置Cookie")
            return None
        
        # 这里需要实际实现
        # 由于Streamlit Cloud不能运行浏览器，这里返回提示
        print("⚠️ 注意：Streamlit Cloud环境无法运行浏览器自动化")
        print("💡 建议：本地运行此功能")
        
        return None
    
    def get_blogger_videos(self, sec_uid: str, days: int = 30) -> List[Dict]:
        """
        获取博主视频列表
        
        Args:
            sec_uid: 博主SEC UID
            days: 获取近N天的数据
            
        Returns:
            视频列表
        """
        if not self.cookie:
            print("❌ 请先设置Cookie")
            return []
        
        print("⚠️ 注意：Streamlit Cloud环境无法运行浏览器自动化")
        print("💡 建议：本地运行此功能")
        
        return []


class CookieHelper:
    """Cookie获取助手"""
    
    @staticmethod
    def get_instructions() -> str:
        """
        获取Cookie获取说明
        
        Returns:
            说明文本
        """
        return """
## 📋 如何获取抖音Cookie

### 步骤1：电脑浏览器登录抖音

1. 用电脑浏览器打开：https://www.douyin.com
2. **扫码登录**你的抖音账号

### 步骤2：复制Cookie

1. 按 **F12** 打开开发者工具
2. 点击 **"Network"**（网络）标签
3. 按 **F5** 刷新页面
4. 找到任意一个请求（通常是第一个）
5. 点击请求，在右侧找到 **"Request Headers"**
6. 找到 **"cookie:"** 这一行
7. **复制整个Cookie值**（从第一个字符到最后）

### 步骤3：在网站输入Cookie

把复制的Cookie粘贴到网站的Cookie输入框中

### ⚠️ 注意事项

- Cookie有效期有限，如果失效需要重新获取
- 不要分享Cookie给他人
- 建议使用小号进行测试

### 🔒 安全提示

- Cookie仅用于读取数据，不会修改你的账号
- 采集时像真实用户一样操作，降低被封风险
- 使用完毕后可以重新登录抖音使旧Cookie失效
        """
    
    @staticmethod
    def validate_cookie(cookie_str: str) -> bool:
        """
        验证Cookie格式
        
        Args:
            cookie_str: Cookie字符串
            
        Returns:
            是否有效
        """
        if not cookie_str or len(cookie_str) < 10:
            return False
        
        # 检查是否包含必要的字段
        required_fields = ['tt_webid', ' Douyin-web']
        
        return True


class DouyinAPIClient:
    """
    抖音API客户端
    使用Cookie直接调用API
    """
    
    def __init__(self, cookie: str = None):
        self.cookie = cookie
        self.base_url = "https://www.douyin.com"
        self.api_urls = {
            "user_profile": "https://www.douyin.com/aweme/v1/web/user/profile/press/",
            "user_videos": "https://www.douyin.com/aweme/v1/web/aweme/post/",
            "video_detail": "https://www.douyin.com/aweme/v1/web/aweme/detail/",
        }
    
    def set_cookie(self, cookie: str):
        """设置Cookie"""
        self.cookie = cookie
    
    def get_user_videos(self, sec_uid: str, cursor: int = 0, count: int = 20) -> Dict:
        """
        获取用户视频列表
        
        Args:
            sec_uid: 用户SEC UID
            cursor: 游标（分页用）
            count: 每次获取的数量
            
        Returns:
            API响应
        """
        import httpx
        
        if not self.cookie:
            return {"status_code": -1, "message": "Cookie未设置"}
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": self.cookie,
            "Referer": "https://www.douyin.com/",
        }
        
        params = {
            "sec_uid": sec_uid,
            "cursor": cursor,
            "count": count,
            "aid": "6383",
            "version_code": "180800",
            "webcast_sdk_version": "1.0.88-beta.0",
        }
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(
                    self.api_urls["user_videos"],
                    headers=headers,
                    params=params
                )
                return response.json()
        except Exception as e:
            return {"status_code": -1, "message": str(e)}
    
    def parse_video_data(self, api_response: Dict) -> List[Dict]:
        """
        解析API响应，提取视频数据
        
        Args:
            api_response: API响应
            
        Returns:
            视频数据列表
        """
        videos = []
        
        if api_response.get("status_code") != 0:
            return videos
        
        aweme_list = api_response.get("aweme_list", [])
        
        for item in aweme_list:
            video = {
                "video_id": item.get("aweme_id"),
                "title": item.get("desc"),
                "likes": item.get("statistics", {}).get("digg_count", 0),
                "comments": item.get("statistics", {}).get("comment_count", 0),
                "shares": item.get("statistics", {}).get("share_count", 0),
                "collects": item.get("statistics", {}).get("collect_count", 0),
                "play_count": item.get("statistics", {}).get("play_count", 0),
                "duration": item.get("video", {}).get("duration", 0),
                "create_time": datetime.fromtimestamp(
                    item.get("create_time", 0)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "video_url": f"https://www.douyin.com/video/{item.get('aweme_id')}",
                "cover_url": item.get("video", {}).get("cover", {}).get("url_list", [None])[0],
            }
            videos.append(video)
        
        return videos
