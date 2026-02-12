"""
抖音数据采集模块

功能：
1. 搜索博主
2. 获取博主视频列表
3. 获取视频详情
"""

import httpx
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import asyncio


class DouyinCrawler:
    """抖音数据采集器"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        self.base_url = "https://www.douyin.com"
        
        # 模拟数据（用于演示和开发测试）
        self._demo_mode = True
        self.cookie = None
        
    def set_cookie(self, cookie: str):
        """设置Cookie用于真实数据采集"""
        self.cookie = cookie
        print(f"✅ Cookie已设置: {len(cookie)} 字符")
        
    def enable_real_mode(self):
        """启用真实数据模式"""
        self._demo_mode = False
        
    def enable_demo_mode(self):
        """启用模拟数据模式"""
        self._demo_mode = True
        
    def search_blogger(self, query: str, search_type: str = "博主名称") -> Optional[Dict]:
        """
        搜索博主
        
        Args:
            query: 搜索关键词
            search_type: 搜索类型（博主名称/抖音号）
            
        Returns:
            博主信息字典 或 None
        """
        # 如果启用了真实数据模式且有Cookie
        if not self._demo_mode and self.cookie:
            real_result = self._search_real_blogger(query, search_type)
            if real_result:
                return real_result
        
        # 使用模拟数据
        return self._get_demo_blogger(query)
    
    def _search_real_blogger(self, query: str, search_type: str) -> Optional[Dict]:
        """
        真实搜索博主（使用Cookie）
        
        注意：由于Streamlit Cloud无法运行浏览器，
        真实数据采集需要在本地环境使用浏览器自动化
        """
        import streamlit as st
        
        st.warning("⚠️ 真实数据采集需要在本地环境运行")
        st.info("💡 请使用本地脚本或在支持浏览器的环境中运行")
        
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
        # 如果启用了真实数据模式且有Cookie
        if not self._demo_mode and self.cookie:
            real_videos = self._get_real_videos(sec_uid, days)
            if real_videos:
                return real_videos
        
        # 使用模拟数据
        return self._get_demo_videos(days)
    
    def _get_real_videos(self, sec_uid: str, days: int) -> List[Dict]:
        """
        真实获取视频数据（使用Cookie）
        
        注意：由于Streamlit Cloud无法运行浏览器，
        真实数据采集需要在本地环境使用浏览器自动化
        """
        import streamlit as st
        
        st.warning("⚠️ 真实数据采集需要在本地环境运行")
        st.info("💡 请使用本地脚本或在支持浏览器的环境中运行")
        
        return []
    
    def _get_demo_blogger(self, query: str) -> Dict:
        """
        获取模拟博主数据
        
        Args:
            query: 搜索关键词
            
        Returns:
            模拟的博主信息
        """
        # 根据输入生成一些变化
        hash_val = hash(query)
        
        return {
            "sec_uid": f"MS4wLjAB{hash_val % 1000000}",
            "nickname": query if len(query) <= 10 else query[:8] + "...",
            "unique_id": query.replace(" ", "").lower()[:8],
            "avatar": f"https://p29.douyinpic.com/avatar/{hash_val % 1000}.webp",
            "follower_count": (hash_val % 1000 + 1) * 10000,
            "following_count": (hash_val % 500 + 1) * 100,
            "video_count": (hash_val % 100 + 1),
            "signature": f"这是{query}的抖音号，分享有趣的视频内容",
            "verified": hash_val % 3 == 0,
            "verified_reason": "优质创作者" if hash_val % 3 == 0 else ""
        }
    
    def _get_demo_videos(self, days: int) -> List[Dict]:
        """
        获取模拟视频数据
        
        Args:
            days: 近N天的数据
            
        Returns:
            模拟的视频列表
        """
        videos = []
        base_date = datetime.now()
        
        # 生成10-30个视频
        num_videos = 15 + hash(str(base_date)) % 15
        
        for i in range(num_videos):
            # 随机日期（近days天内）
            days_ago = i % days + (hash(i) % 3)
            publish_date = base_date - timedelta(days=days_ago)
            
            # 随机互动数据（模拟真实分布）
            base_likes = 10000 + (hash(i) % 100) * 1000
            like_count = base_likes + (hash(i * 2) % 50000)
            comment_count = like_count // 50 + (hash(i * 3) % 1000)
            share_count = like_count // 100 + (hash(i * 4) % 500)
            
            # 视频标题
            titles = [
                f"第{i+1}个视频 - 今天分享{['有趣','精彩','实用','搞笑','温馨'][i%5]}的内容",
                f"盘点{['2024','热门','爆款','必看','推荐'][i%5]}的{['那些事','合集','TOP10','技巧','攻略'][i%5]}",
                f"姐妹们！{['这个','今天','教你们','分享','强烈推荐'][i%5]}的一定要看！",
                f"【{['干货','教程','测评','开箱','日常'][i%5]}】{['必看','分享','第{i+1}期','更新','上架'][i%5]}",
                f"关于{['生活','工作','学习','恋爱','美食'][i%5]}，我想说几句"
            ]
            
            video = {
                "video_id": f"720{1000000000000 + i * 100000000}",
                "title": titles[i % len(titles)],
                "likes": like_count,
                "comments": comment_count,
                "shares": share_count,
                "collects": like_count // 30,
                "play_count": like_count * 15 + (hash(i * 5) % 100000),
                "duration": 15 + (hash(i) % 60),
                "create_time": publish_date.strftime("%Y-%m-%d %H:%M:%S"),
                "video_url": f"https://www.douyin.com/video/{7200000000000000000 + i}",
                "cover_url": f"https://p29.douyinpic.com/img/{1000000000 + i}.webp",
                "music_title": f"背景音乐{i+1}",
                "music_author": f"音乐人{i%5+1}",
                "tags": [f"tag{i%10+1}", f"热门{i%5+1}", f"推荐{i%3+1}"],
                "desc": titles[i % len(titles)]
            }
            
            videos.append(video)
        
        return videos
    
    def get_video_detail(self, video_id: str) -> Optional[Dict]:
        """
        获取单个视频详情
        
        Args:
            video_id: 视频ID
            
        Returns:
            视频详情 或 None
        """
        videos = self._get_demo_videos(1)
        if videos:
            return videos[0]
        return None
    
    def export_to_json(self, videos: List[Dict], filepath: str):
        """
        导出视频数据到JSON文件
        
        Args:
            videos: 视频列表
            filepath: 文件路径
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)
    
    def export_to_csv(self, videos: List[Dict], filepath: str):
        """
        导出视频数据到CSV文件
        
        Args:
            videos: 视频列表
            filepath: 文件路径
        """
        import pandas as pd
        
        df = pd.DataFrame(videos)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')


class DouyinAPIClient:
    """抖音API客户端（实际采集需要用到）"""
    
    def __init__(self):
        self.client = httpx.Client(timeout=30.0)
        self.api_endpoints = {
            "user_info": "https://www.douyin.com/aweme/v1/web/user/profile/press/",
            "user_videos": "https://www.douyin.com/aweme/v1/web/aweme/post/",
            "video_detail": "https://www.douyin.com/aweme/v1/web/aweme/detail/",
            "search": "https://www.douyin.com/aweme/v1/web/search/item/"
        }
    
    async def get_user_info(self, sec_uid: str) -> Dict:
        """获取用户信息"""
        # 实际实现需要处理反爬
        pass
    
    async def get_user_videos(self, sec_uid: str, cursor: int = 0) -> Dict:
        """获取用户视频列表"""
        # 实际实现需要处理反爬
        pass
