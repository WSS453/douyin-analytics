# 🎵 抖音博主数据分析系统

一个基于 Python Streamlit 的抖音博主数据分析工具，支持搜索博主、获取视频数据、按点赞数排序分析，并提供可视化图表展示。

## ✨ 功能特性

- 🔍 **博主搜索** - 输入博主名称或抖音号，快速查找博主信息
- 📥 **数据采集** - 自动获取博主近30天的视频数据
- 📊 **智能分析** - 按点赞数排序，支持多种统计维度
- 📈 **可视化展示** - 排行榜、趋势图、互动分析
- 💾 **数据导出** - 支持CSV格式导出

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/douyin-analytics.git
cd douyin-analytics
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
streamlit run app.py
```

应用将在 `http://localhost:8501` 打开。

## 📦 项目结构

```
douyin-analytics/
├── app.py              # Streamlit 主应用
├── crawlers.py         # 抖音数据采集模块
├── data_processor.py   # 数据处理与分析模块
├── requirements.txt    # Python 依赖
├── README.md           # 项目说明文档
└── .gitignore         # Git 忽略规则
```

## 🛠️ 技术栈

- **框架**: Streamlit (Python)
- **数据处理**: Pandas, NumPy
- **可视化**: Plotly, Altair
- **数据采集**: httpx, Playwright（预留）
- **部署**: Streamlit Cloud (免费)

## 📖 使用方法

1. 在左侧边栏输入博主名称或抖音号
2. 点击"搜索博主"按钮
3. 查看视频数据分析结果：
   - **排行榜** - 按点赞数排序的视频列表
   - **趋势图** - 发布时间与互动数据趋势
   - **详细数据** - 完整数据表格，支持导出
   - **对比分析** - 高赞/低赞视频对比

## ⚠️ 注意事项

1. **数据来源**: 本系统使用模拟数据进行演示，实际数据采集需要处理抖音的反爬机制
2. **反爬限制**: 抖音有严格的反爬策略，大量请求可能导致IP被封
3. **数据完整性**: 部分数据需要登录后才能完整获取

## 🔧 自定义配置

### 调整模拟数据

在 `crawlers.py` 中修改 `_demo_mode` 开关：

```python
class DouyinCrawler:
    def __init__(self):
        self._demo_mode = True  # True=模拟数据, False=真实采集
```

### 添加真实采集

如需实现真实数据采集，可参考以下方案：

1. **MediaCrawler** - 开源的多平台爬虫项目
   - GitHub: https://github.com/NanmiCoder/MediaCrawler
   - 支持抖音、B站、小红书等

2. **douyin-tiktok-scraper** - PyPI 包
   - `pip install douyin-tiktok-scraper`

## 📝 更新日志

### v1.0.0 (2024-02)
- ✨ 初始版本发布
- 🔍 博主搜索功能
- 📊 数据分析功能
- 📈 可视化图表
- 💾 CSV数据导出

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题，请联系作者。

---

**注意**: 本项目仅供学习和研究使用，请勿用于商业目的。数据采集请遵守相关法律法规和平台协议。
