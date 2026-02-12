# 🎵 抖音博主数据分析系统 - 本地版本

## 📋 本地版本说明

本版本可以在本地运行，支持**浏览器自动化**获取真实数据。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装浏览器（用于自动化）

```bash
python -m playwright install chromium
```

### 3. 运行应用

```bash
python local_app.py
```

应用将在 `http://localhost:8501` 打开

---

## 🍪 获取Cookie步骤

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

---

## ⚠️ 注意事项

- Cookie有效期有限，失效后需要重新获取
- 不要分享Cookie给他人
- 建议使用小号进行测试
- 采集时像真实用户一样操作，降低被封风险

---

## 🔒 安全提示

- Cookie仅用于读取数据，不会修改你的账号
- 采集时像真实用户一样操作，降低被封风险
- 使用完毕后可以重新登录抖音使旧Cookie失效

---

## 📁 文件说明

```
douyin-analytics/
├── local_app.py          # 本地主应用
├── app.py               # 网站版本（模拟数据）
├── crawlers.py          # 数据采集模块
├── playwright_crawler.py # 浏览器自动化模块
├── data_processor.py    # 数据处理模块
└── requirements.txt     # 依赖列表
```

---

## 💡 使用建议

**短期**：先用模拟数据模式体验功能

**长期**：设置Cookie后使用真实数据模式获取真实数据

---

## 🛠️ 故障排除

### 问题1：Cookie无效
**解决方法**：重新获取Cookie，按照上面的步骤操作

### 问题2：采集不到数据
**解决方法**：
1. 检查Cookie是否有效
2. 尝试使用模拟数据模式
3. 检查网络连接

### 问题3：浏览器安装失败
**解决方法**：
```bash
# 使用国内镜像
playwright install --with-deps chromium
```

---

## 📞 支持

如有问题，请联系开发者。

---

**注意**：本项目仅供学习和研究使用，请勿用于商业目的。
