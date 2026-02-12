"""
抖音博主数据分析系统
Streamlit Web Application

功能：
1. 搜索博主（名称/抖音号）
2. 获取近30天视频数据
3. 按点赞数排序分析
4. 可视化展示
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from pathlib import Path

from crawlers import DouyinCrawler
from data_processor import DataProcessor

# 页面配置
st.set_page_config(
    page_title="抖音博主数据分析",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
if 'crawler' not in st.session_state:
    st.session_state.crawler = DouyinCrawler()
if 'processor' not in st.session_state:
    st.session_state.processor = DataProcessor()
if 'current_blogger' not in st.session_state:
    st.session_state.current_blogger = None
if 'videos_data' not in st.session_state:
    st.session_state.videos_data = None


def main():
    """主应用入口"""
    
    # 标题
    st.title("🎵 抖音博主数据分析系统")
    st.markdown("---")
    
    # 侧边栏 - 搜索
    with st.sidebar:
        st.header("🔍 博主搜索")
        
        search_type = st.radio(
            "搜索方式",
            ["博主名称", "抖音号"]
        )
        
        if search_type == "博主名称":
            search_query = st.text_input("输入博主名称", placeholder="例如：papi酱")
        else:
            search_query = st.text_input("输入抖音号", placeholder="例如：papi")
        
        search_btn = st.button("搜索博主", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        # Cookie设置
        st.header("🍪 Cookie设置")
        
        with st.expander("📖 如何获取Cookie？", expanded=False):
            st.markdown("""
            ### 获取步骤：
            1. 电脑浏览器打开 https://www.douyin.com
            2. **扫码登录**你的抖音账号
            3. 按 **F12** 打开开发者工具
            4. 点击 **"Network"** 标签
            5. 按 **F5** 刷新页面
            6. 找到请求，复制 **Cookie** 值
            7. 粘贴到下方输入框
            """)
        
        cookie_input = st.text_area(
            "粘贴抖音Cookie",
            placeholder="复制浏览器中的Cookie值...",
            height=100,
            help="获取方法见上方说明"
        )
        
        if cookie_input:
            st.session_state.cookie = cookie_input
            st.success("✅ Cookie已设置")
        
        use_real_data = st.checkbox(
            "使用真实数据",
            value=False,
            help="勾选后使用Cookie获取真实数据（需要先设置Cookie）"
        )
        
        if use_real_data and not cookie_input:
            st.warning("⚠️ 请先设置Cookie才能使用真实数据")
        
        st.markdown("---")
        
        # 缓存管理
        st.header("💾 数据管理")
        if st.button("清除缓存数据", use_container_width=True):
            st.session_state.current_blogger = None
            st.session_state.videos_data = None
            st.success("缓存已清除！")
        
        # 关于
        st.markdown("---")
        st.caption("🎯 数据来源：抖音公开数据")
        st.caption("📊 分析维度：点赞、评论、分享")
        
        # 设置数据源模式
        if 'use_real_data' not in st.session_state:
            st.session_state.use_real_data = False
        st.session_state.use_real_data = use_real_data
    
    # 主内容区
    if search_btn and search_query:
        search_and_display(search_query, search_type)
    elif st.session_state.videos_data is not None:
        # 显示已缓存的数据
        display_analysis()
    else:
        # 欢迎页面
        display_welcome()


def search_and_display(query: str, search_type: str):
    """搜索并显示结果"""
    with st.spinner(f"正在搜索博主: {query}..."):
        try:
            # 搜索博主
            blogger_info = st.session_state.crawler.search_blogger(query, search_type)
            
            if blogger_info:
                st.session_state.current_blogger = blogger_info
                
                # 获取视频数据
                with st.spinner("正在获取视频数据..."):
                    videos = st.session_state.crawler.get_blogger_videos(
                        blogger_info['sec_uid'],
                        days=30
                    )
                    st.session_state.videos_data = videos
                
                # 显示分析结果
                display_analysis()
            else:
                st.error(f"未找到博主: {query}")
                st.info("💡 提示：请检查输入是否正确，或尝试其他名称/抖音号")
                
        except Exception as e:
            st.error(f"搜索失败: {str(e)}")
            st.info("💡 建议：抖音有反爬机制，可能需要稍后再试")


def display_welcome():
    """显示欢迎页面"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🔍 **输入博主信息** - 输入博主名称或抖音号")
    with col2:
        st.info("📥 **自动采集** - 获取近30天视频数据")
    with col3:
        st.info("📊 **智能分析** - 按点赞数排序展示")
    
    st.markdown("### 📌 使用方法")
    st.markdown("""
    1. 在左侧输入博主名称或抖音号
    2. 点击"搜索博主"按钮
    3. 查看视频数据分析结果
    
    ### 💡 热门博主示例
    - papi酱
    - 疯产姐妹
    - 迪丽热巴
    - 人民日报
    """)


def display_analysis():
    """显示数据分析结果"""
    if st.session_state.current_blogger is None:
        return
    
    blogger = st.session_state.current_blogger
    videos = st.session_state.videos_data
    
    # 博主信息卡片
    st.markdown("### 👤 博主信息")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.image(blogger['avatar'], width=80, caption="头像")
    with col2:
        st.metric("昵称", blogger['nickname'])
    with col3:
        st.metric("抖音号", blogger['unique_id'])
    with col4:
        st.metric("粉丝数", format_number(blogger['follower_count']))
    
    st.markdown(f"📝 简介: {blogger.get('signature', '暂无简介')}")
    st.markdown("---")
    
    # 视频统计概览
    if videos:
        st.markdown("### 📊 视频数据概览")
        
        df = st.session_state.processor.process_videos(videos)
        stats = st.session_state.processor.get_statistics(df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("视频总数", stats['total_videos'])
        with col2:
            st.metric("总点赞数", format_number(stats['total_likes']))
        with col3:
            st.metric("平均点赞", format_number(stats['avg_likes']))
        with col4:
            st.metric("最高点赞", format_number(stats['max_likes']))
        
        st.markdown("---")
        
        # 数据分析选项卡
        tab1, tab2, tab3, tab4 = st.tabs(["📋 排行榜", "📈 趋势图", "📊 详细数据", "🔍 对比分析"])
        
        with tab1:
            display_ranking(df)
        
        with tab2:
            display_trends(df)
        
        with tab3:
            display_details(df)
        
        with tab4:
            display_comparison(df)
    else:
        st.warning("未获取到视频数据")


def display_ranking(df: pd.DataFrame):
    """显示点赞排行榜"""
    st.markdown("#### 🎬 视频排行榜（按点赞数排序）")
    
    # 按点赞数排序
    sorted_df = df.sort_values('likes', ascending=False)
    
    # 显示前20个视频
    top_videos = sorted_df.head(20)
    
    # 创建展示数据
    display_data = top_videos[['title', 'likes', 'comments', 'shares', 'create_time']].copy()
    display_data['likes'] = display_data['likes'].apply(lambda x: format_number(x))
    display_data['comments'] = display_data['comments'].apply(lambda x: format_number(x))
    display_data['shares'] = display_data['shares'].apply(lambda x: format_number(x))
    display_data.columns = ['标题', '点赞', '评论', '分享', '发布时间']
    
    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
    
    # 可视化排名
    st.markdown("#### 🏆 Top 10 点赞分布")
    
    if len(top_videos) >= 10:
        top10 = top_videos.head(10)
        chart_data = pd.DataFrame({
            '排名': range(1, 11),
            '点赞数': top10['likes'].values,
            '标题': [title[:15] + '...' if len(title) > 15 else title for title in top10['title'].values]
        })
        
        st.bar_chart(
            chart_data.set_index('标题')['点赞数'],
            use_container_width=True
        )


def display_trends(df: pd.DataFrame):
    """显示数据趋势图"""
    st.markdown("#### 📈 发布时间与互动数据趋势")
    
    # 按日期分组统计
    df['date'] = pd.to_datetime(df['create_time']).dt.date
    daily_stats = df.groupby('date').agg({
        'likes': 'sum',
        'comments': 'sum',
        'shares': 'sum'
    }).reset_index()
    
    if not daily_stats.empty:
        # 互动趋势图
        st.line_chart(
            daily_stats.set_index('date')[['likes', 'comments', 'shares']],
            use_container_width=True
        )
        
        # 每日视频发布数量
        daily_count = df.groupby('date').size()
        st.markdown("#### 📅 每日发布视频数量")
        st.bar_chart(daily_count, use_container_width=True)
    else:
        st.info("时间数据不完整，无法生成趋势图")


def display_details(df: pd.DataFrame):
    """显示详细数据表格"""
    st.markdown("#### 📋 完整视频数据")
    
    # 可下载数据
    csv = df.to_csv(index=False)
    st.download_button(
        "📥 下载CSV数据",
        csv,
        "douyin_videos.csv",
        "text/csv",
        use_container_width=True
    )
    
    # 详细表格
    st.dataframe(
        df[['title', 'likes', 'comments', 'shares', 'create_time', 'video_url']],
        use_container_width=True,
        hide_index=True
    )


def display_comparison(df: pd.DataFrame):
    """显示对比分析"""
    st.markdown("#### 🔍 互动数据对比")
    
    # 互动比率
    df['like_comment_ratio'] = df['likes'] / (df['comments'] + 1)
    df['engagement_rate'] = (df['likes'] + df['comments'] + df['shares']) / 10000
    
    # 高赞视频 vs 低赞视频
    median_likes = df['likes'].median()
    high_likes = df[df['likes'] >= median_likes]
    low_likes = df[df['likes'] < median_likes]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### ⭐ 高赞视频（≥中位数）")
        if len(high_likes) > 0:
            st.metric("数量", len(high_likes))
            st.metric("平均点赞", format_number(high_likes['likes'].mean()))
            st.metric("平均评论", format_number(high_likes['comments'].mean()))
        else:
            st.info("无数据")
    
    with col2:
        st.markdown("##### 📉 低赞视频（<中位数）")
        if len(low_likes) > 0:
            st.metric("数量", len(low_likes))
            st.metric("平均点赞", format_number(low_likes['likes'].mean()))
            st.metric("平均评论", format_number(low_likes['comments'].mean()))
        else:
            st.info("无数据")
    
    # 互动率分布
    st.markdown("##### 📊 互动率分布")
    engagement_data = df[['likes', 'comments', 'shares']].sum()
    total = engagement_data.sum()
    
    if total > 0:
        ratios = {
            '点赞': engagement_data['likes'] / total * 100,
            '评论': engagement_data['comments'] / total * 100,
            '分享': engagement_data['shares'] / total * 100
        }
        
        st.bar_chart(pd.Series(ratios), use_container_width=True)


def format_number(num: int) -> str:
    """格式化数字"""
    if num >= 10000:
        return f"{num/10000:.1f}万"
    elif num >= 1000:
        return f"{num/1000:.1f}k"
    else:
        return str(num)


if __name__ == "__main__":
    main()
