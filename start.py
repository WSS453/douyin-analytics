#!/usr/bin/env python3
"""
启动脚本 - 启动抖音博主数据分析系统
"""

import subprocess
import sys
import os

def main():
    print("=" * 50)
    print("  抖音博主数据分析系统 - 启动程序")
    print("=" * 50)
    print()
    print("  请访问: http://localhost:8501")
    print()
    print("  按 Ctrl+C 停止服务")
    print("=" * 50)
    print()

    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 启动Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\n已停止服务")
    except FileNotFoundError:
        print("错误: 未找到Streamlit，请安装依赖:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()
