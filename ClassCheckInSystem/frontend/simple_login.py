#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版登录页面 - 直接实现离线登录
"""

import streamlit as st
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="课堂考勤签到系统 - 登录",
    page_icon="🔐",
    layout="centered"
)

# 自定义CSS
st.markdown("""
<style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background: white;
    }
    .login-title {
        text-align: center;
        color: #667eea;
        margin-bottom: 2rem;
    }
    .login-button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 5px;
        font-size: 1.1rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown('<h1 class="login-title">🔐 用户登录</h1>', unsafe_allow_html=True)

# 模拟用户数据
MOCK_USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "管理员", "id": 1},
    "teacher": {"password": "teacher123", "role": "teacher", "name": "张老师", "id": 2},
    "student": {"password": "student123", "role": "student", "name": "李同学", "id": 3}
}

# 登录表单
with st.form("login_form"):
    username = st.text_input("用户名", value="admin", help="请输入用户名")
    password = st.text_input("密码", type="password", value="admin123", help="请输入密码")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        remember_me = st.checkbox("记住我")
    with col2:
        submit_button = st.form_submit_button("登录", use_container_width=True)

# 处理登录
if submit_button:
    st.write("🔍 正在验证登录信息...")
    
    # 显示调试信息
    st.write(f"**调试信息:**")
    st.write(f"- 用户名: `{username}`")
    st.write(f"- 密码长度: {len(password)}")
    st.write(f"- 可用用户: {list(MOCK_USERS.keys())}")
    
    # 验证登录
    if username in MOCK_USERS and MOCK_USERS[username]["password"] == password:
        user_data = MOCK_USERS[username]
        
        # 保存登录状态
        st.session_state["logged_in"] = True
        st.session_state["user_info"] = {
            "id": user_data["id"],
            "username": username,
            "name": user_data["name"],
            "role": user_data["role"]
        }
        st.session_state["access_token"] = f"mock_token_{username}_{datetime.now().timestamp()}"
        
        st.success("✅ 登录成功！")
        st.balloons()
        
        # 显示用户信息
        st.info(f"欢迎，{user_data['name']}！")
        
        # 跳转到主应用
        st.markdown("### 🚀 正在跳转到主应用...")
        st.markdown("请访问主应用页面开始使用系统功能。")
        
    else:
        st.error("❌ 用户名或密码错误")
        st.write("**可用的测试账户:**")
        for user, data in MOCK_USERS.items():
            st.write(f"- **{user}**: {data['name']} (密码: {data['password']})")

# 显示测试账户信息
st.markdown("---")
st.markdown("### 📋 测试账户信息")
st.markdown("""
| 用户名 | 密码 | 角色 | 姓名 |
|--------|------|------|------|
| admin | admin123 | 管理员 | 管理员 |
| teacher | teacher123 | 教师 | 张老师 |
| student | student123 | 学生 | 李同学 |
""")

st.markdown('</div>', unsafe_allow_html=True)
