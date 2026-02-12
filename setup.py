#!/usr/bin/env python3
"""
项目设置脚本
安装依赖并验证环境
"""

import subprocess
import sys
import os


def install_requirements():
    """安装项目依赖"""
    print("📦 正在安装依赖...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", 
            os.path.join(os.path.dirname(__file__), "requirements.txt"),
            "--quiet"
        ])
        print("✅ 依赖安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False


def verify_installation():
    """验证安装"""
    print("\n🔍 验证安装...")
    
    try:
        import streamlit
        print(f"  ✅ Streamlit: {streamlit.__version__}")
        
        import pandas
        print(f"  ✅ Pandas: {pandas.__version__}")
        
        import plotly
        print(f"  ✅ Plotly: {plotly.__version__}")
        
        print("\n✅ 所有依赖安装成功！")
        return True
    except ImportError as e:
        print(f"  ❌ 导入失败: {e}")
        return False


def run_app():
    """运行应用"""
    print("\n🚀 启动应用...")
    print("应用将在 http://localhost:8501 打开")
    print("按 Ctrl+C 停止应用\n")
    
    os.chdir(os.path.dirname(__file__))
    subprocess.call([sys.executable, "-m", "streamlit", "run", "app.py"])


def main():
    """主函数"""
    print("=" * 50)
    print("🎵 抖音博主数据分析系统 - 设置脚本")
    print("=" * 50)
    
    if not install_requirements():
        sys.exit(1)
    
    if not verify_installation():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("设置完成！选择操作：")
    print("=" * 50)
    print("1. 运行应用 (streamlit run app.py)")
    print("2. 仅验证安装")
    print("3. 退出")
    
    choice = input("\n请输入选项 (1/2/3): ").strip()
    
    if choice == "1":
        run_app()
    elif choice == "2":
        print("\n✅ 验证完成！")
    else:
        print("\n👋 再见！")


if __name__ == "__main__":
    main()
