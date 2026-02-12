"""
数据处理模块

功能：
1. 处理视频数据
2. 统计分析
3. 数据排序
4. 数据可视化准备
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        pass
    
    def process_videos(self, videos: List[Dict]) -> pd.DataFrame:
        """
        处理视频数据列表
        
        Args:
            videos: 原始视频数据列表
            
        Returns:
            处理的DataFrame
        """
        if not videos:
            return pd.DataFrame()
        
        # 转换为DataFrame
        df = pd.DataFrame(videos)
        
        # 数据清洗和类型转换
        # 确保数值列为数字类型
        numeric_cols = ['likes', 'comments', 'shares', 'collects', 'play_count', 'duration']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        # 转换时间列
        if 'create_time' in df.columns:
            df['create_time'] = pd.to_datetime(df['create_time'], errors='coerce')
        
        # 计算派生指标
        df = self._calculate_metrics(df)
        
        return df
    
    def _calculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算派生指标"""
        
        # 总互动数
        if 'likes' in df.columns and 'comments' in df.columns and 'shares' in df.columns:
            df['total_interactions'] = df['likes'] + df['comments'] + df['shares']
        
        # 点赞率（相对于播放量）
        if 'likes' in df.columns and 'play_count' in df.columns:
            df['like_rate'] = (df['likes'] / df['play_count'] * 100).round(2)
        
        # 互动率
        if 'total_interactions' in df.columns and 'play_count' in df.columns:
            df['engagement_rate'] = (df['total_interactions'] / df['play_count'] * 100).round(2)
        
        # 评论占比
        if 'comments' in df.columns and 'total_interactions' in df.columns:
            df['comment_ratio'] = (df['comments'] / df['total_interactions'] * 100).round(2)
        
        # 分享占比
        if 'shares' in df.columns and 'total_interactions' in df.columns:
            df['share_ratio'] = (df['shares'] / df['total_interactions'] * 100).round(2)
        
        # 点赞/评论比
        if 'likes' in df.columns and 'comments' in df.columns:
            df['like_comment_ratio'] = (df['likes'] / (df['comments'] + 1)).round(0)
        
        # 发布日期
        if 'create_time' in df.columns:
            df['publish_date'] = df['create_time'].dt.date
            df['publish_hour'] = df['create_time'].dt.hour
            df['day_of_week'] = df['create_time'].dt.dayofweek
        
        return df
    
    def get_statistics(self, df: pd.DataFrame) -> Dict:
        """
        获取统计数据
        
        Args:
            df: 视频数据DataFrame
            
        Returns:
            统计字典
        """
        if df.empty:
            return {
                'total_videos': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0,
                'avg_likes': 0,
                'avg_comments': 0,
                'avg_shares': 0,
                'max_likes': 0,
                'min_likes': 0,
                'median_likes': 0,
                'std_likes': 0
            }
        
        stats = {
            'total_videos': len(df),
            'total_likes': int(df['likes'].sum()),
            'total_comments': int(df['comments'].sum()),
            'total_shares': int(df['shares'].sum()),
            'avg_likes': int(df['likes'].mean()),
            'avg_comments': int(df['comments'].mean()),
            'avg_shares': int(df['shares'].mean()),
            'max_likes': int(df['likes'].max()),
            'min_likes': int(df['likes'].min()),
            'median_likes': int(df['likes'].median()),
            'std_likes': int(df['likes'].std()) if len(df) > 1 else 0
        }
        
        return stats
    
    def sort_by_likes(self, df: pd.DataFrame, ascending: bool = False) -> pd.DataFrame:
        """
        按点赞数排序
        
        Args:
            df: 视频数据DataFrame
            ascending: 升序/降序
            
        Returns:
            排序后的DataFrame
        """
        return df.sort_values('likes', ascending=ascending)
    
    def filter_by_date(self, df: pd.DataFrame, days: int = 30) -> pd.DataFrame:
        """
        按日期筛选（近N天）
        
        Args:
            df: 视频数据DataFrame
            days: 天数
            
        Returns:
            筛选后的DataFrame
        """
        if df.empty or 'create_time' not in df.columns:
            return df
        
        cutoff_date = datetime.now() - timedelta(days=days)
        mask = df['create_time'] >= cutoff_date
        
        return df[mask]
    
    def get_top_videos(self, df: pd.DataFrame, n: int = 10, by: str = 'likes') -> pd.DataFrame:
        """
        获取Top N视频
        
        Args:
            df: 视频数据DataFrame
            n: 数量
            by: 排序字段
            
        Returns:
            Top N视频
        """
        if df.empty or by not in df.columns:
            return df.head(n) if n > 0 else df
        
        return df.nlargest(n, by)
    
    def get_daily_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        按日期统计
        
        Args:
            df: 视频数据DataFrame
            
        Returns:
            按日期统计的DataFrame
        """
        if df.empty or 'publish_date' not in df.columns:
            return pd.DataFrame()
        
        daily = df.groupby('publish_date').agg({
            'likes': 'sum',
            'comments': 'sum',
            'shares': 'sum',
            'video_id': 'count'
        }).reset_index()
        
        daily.columns = ['日期', '点赞总数', '评论总数', '分享总数', '视频数量']
        
        return daily
    
    def get_hourly_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        按小时统计
        
        Args:
            df: 视频数据DataFrame
            
        Returns:
            按小时统计的DataFrame
        """
        if df.empty or 'publish_hour' not in df.columns:
            return pd.DataFrame()
        
        hourly = df.groupby('publish_hour').agg({
            'likes': 'mean',
            'comments': 'mean',
            'video_id': 'count'
        }).reset_index()
        
        hourly.columns = ['发布小时', '平均点赞', '平均评论', '视频数量']
        
        return hourly
    
    def compare_periods(self, df: pd.DataFrame, split_date: str = None) -> Dict:
        """
        对比两个时间段的数据
        
        Args:
            df: 视频数据DataFrame
            split_date: 分隔日期（YYYY-MM-DD格式）
            
        Returns:
            对比数据字典
        """
        if df.empty or 'create_time' not in df.columns:
            return {}
        
        if split_date is None:
            split_date = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        
        try:
            split_dt = pd.to_datetime(split_date)
            
            early = df[df['create_time'] < split_dt]
            late = df[df['create_time'] >= split_dt]
            
            return {
                'early_period': {
                    'videos': len(early),
                    'avg_likes': early['likes'].mean() if len(early) > 0 else 0,
                    'total_likes': early['likes'].sum() if len(early) > 0 else 0
                },
                'late_period': {
                    'videos': len(late),
                    'avg_likes': late['likes'].mean() if len(late) > 0 else 0,
                    'total_likes': late['likes'].sum() if len(late) > 0 else 0
                },
                'growth_rate': (
                    (late['likes'].mean() - early['likes'].mean()) / 
                    early['likes'].mean() * 100 if len(early) > 0 and early['likes'].mean() > 0 else 0
                )
            }
        except Exception:
            return {}
    
    def generate_summary(self, df: pd.DataFrame) -> str:
        """
        生成数据摘要文本
        
        Args:
            df: 视频数据DataFrame
            
        Returns:
            摘要文本
        """
        if df.empty:
            return "暂无视频数据"
        
        stats = self.get_statistics(df)
        
        summary = f"""
📊 数据摘要
━━━━━━━━━━━━
• 视频总数：{stats['total_videos']} 个
• 总点赞数：{stats['total_likes']:,}
• 总评论数：{stats['total_comments']:,}
• 总分享数：{stats['total_shares']:,}

📈 平均数据
━━━━━━━━━━━━
• 平均点赞：{stats['avg_likes']:,}
• 平均评论：{stats['avg_comments']:,}
• 平均分享：{stats['avg_shares']:,}

🏆 最佳表现
━━━━━━━━━━━━
• 最高点赞：{stats['max_likes']:,}
• 中位数点赞：{stats['median_likes']:,}
        """
        
        return summary.strip()
    
    def export_data(self, df: pd.DataFrame, format: str = 'csv') -> str:
        """
        导出数据
        
        Args:
            df: 视频数据DataFrame
            format: 导出格式（csv/json）
            
        Returns:
            导出内容字符串
        """
        if format == 'json':
            return df.to_json(orient='records', force_ascii=False, indent=2)
        else:
            return df.to_csv(index=False, encoding='utf-8-sig')
