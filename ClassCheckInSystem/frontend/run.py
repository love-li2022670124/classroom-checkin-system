"""
课堂考勤签到系统 - Streamlit前端启动脚本
Classroom Attendance Sign-in System - Streamlit Frontend Launcher
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import streamlit  # pyright: ignore[reportMissingImports]
        import streamlit_extras    # pyright: ignore[reportMissingImports]
        import plotly  # pyright: ignore[reportMissingImports]
        import pandas
        import requests
        import qrcode  # pyright: ignore[reportMissingModuleSource]
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        return False

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def start_streamlit():
    """启动Streamlit应用"""
    print("🚀 正在启动Streamlit应用...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "127.0.0.1",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("📚 课堂考勤签到系统 - Streamlit前端")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists("app.py"):
        print("❌ 请在项目根目录下运行此脚本")
        return
    
    # 检查依赖
    if not check_dependencies():
        print("🔧 正在安装依赖...")
        if not install_dependencies():
            print("❌ 依赖安装失败，请手动安装")
            return
    
    # 启动应用
    print("\n🌐 应用将在浏览器中打开: http://127.0.0.1:8501")
    print("💡 按 Ctrl+C 停止应用")
    print("-" * 50)
    
    start_streamlit()

if __name__ == "__main__":
    main()
