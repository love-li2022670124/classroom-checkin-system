#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产环境启动脚本
"""

import os
import sys
import subprocess

def main():
    """主函数"""
    print("🚀 启动生产环境...")
    
    # 设置环境变量
    os.environ.setdefault('STREAMLIT_SERVER_PORT', '8501')
    os.environ.setdefault('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')
    os.environ.setdefault('STREAMLIT_SERVER_HEADLESS', 'true')
    os.environ.setdefault('STREAMLIT_BROWSER_GATHER_USAGE_STATS', 'false')
    
    # 启动Streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', os.environ['STREAMLIT_SERVER_PORT'],
            '--server.address', os.environ['STREAMLIT_SERVER_ADDRESS'],
            '--server.headless', os.environ['STREAMLIT_SERVER_HEADLESS'],
            '--browser.gatherUsageStats', os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS']
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()
