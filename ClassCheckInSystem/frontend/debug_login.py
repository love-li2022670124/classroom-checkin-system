#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临时测试页面 - 用于调试登录问题
"""

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="登录测试",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 登录测试页面")

# 模拟用户数据
MOCK_USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "管理员", "id": 1},
    "teacher001": {"password": "teacher123", "role": "teacher", "name": "张老师", "id": 2},
    "student001": {"password": "student123", "role": "student", "name": "李同学", "id": 3}
}

st.write("**可用的测试账户：**")
for user, data in MOCK_USERS.items():
    st.write(f"- **{user}**: {data['name']} (密码: {data['password']})")

st.markdown("---")

# 登录表单
with st.form("test_login"):
    username = st.text_input("用户名", value="admin")
    password = st.text_input("密码", type="password", value="admin123")
    submit_button = st.form_submit_button("测试登录")

if submit_button:
    st.write("🔍 正在测试登录...")
    
    # 显示输入信息
    st.write(f"**输入信息：**")
    st.write(f"- 用户名: `{username}`")
    st.write(f"- 密码: `{password}`")
    
    # 验证登录
    if username in MOCK_USERS and MOCK_USERS[username]["password"] == password:
        user_data = MOCK_USERS[username]
        
        # 模拟API响应
        mock_response = {
            "access_token": f"mock_token_{username}_{datetime.now().timestamp()}",
            "token_type": "bearer",
            "user": {
                "id": user_data["id"],
                "username": username,
                "name": user_data["name"],
                "role": user_data["role"]
            }
        }
        
        st.success("✅ 登录测试成功！")
        st.write("**模拟API响应：**")
        st.json(mock_response)
        
        # 保存到session state
        st.session_state["test_logged_in"] = True
        st.session_state["test_user_info"] = mock_response["user"]
        st.session_state["test_token"] = mock_response["access_token"]
        
        st.balloons()
        
    else:
        st.error("❌ 登录测试失败")
        st.write("**可能的原因：**")
        st.write("- 用户名不存在")
        st.write("- 密码错误")
        st.write("- 输入格式问题")

# 显示当前状态
if "test_logged_in" in st.session_state:
    st.markdown("---")
    st.success("✅ 当前已登录")
    st.write(f"**用户信息：** {st.session_state['test_user_info']}")
    
    if st.button("退出登录"):
        del st.session_state["test_logged_in"]
        del st.session_state["test_user_info"]
        del st.session_state["test_token"]
        st.rerun()
