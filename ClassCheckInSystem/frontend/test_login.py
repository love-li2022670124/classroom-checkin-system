#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录功能
"""

import streamlit as st
from utils.api_client import APIClient

st.set_page_config(page_title="登录测试", page_icon="🔐")

st.title("🔐 登录测试")

# 创建API客户端
api_client = APIClient()

# 显示当前配置
st.info(f"API地址: {api_client.base_url}")
st.info(f"离线模式: {api_client.offline_mode}")

# 登录表单
with st.form("login_form"):
    username = st.text_input("用户名", value="admin")
    password = st.text_input("密码", type="password", value="admin123")
    submit_button = st.form_submit_button("登录")

if submit_button:
    st.write("正在登录...")
    
    # 尝试登录
    result = api_client.login(username, password)
    
    if "error" in result:
        st.error(f"登录失败: {result['error']}")
    else:
        st.success("登录成功！")
        st.json(result)
        
        # 保存登录状态
        st.session_state["logged_in"] = True
        st.session_state["user_info"] = result["user"]
        st.session_state["access_token"] = result["access_token"]
        
        st.balloons()
