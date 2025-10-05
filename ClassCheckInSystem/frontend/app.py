"""
课堂考勤签到系统 - Streamlit前端主应用
Classroom Attendance Sign-in System - Streamlit Frontend
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
import streamlit_extras as extras  # pyright: ignore[reportMissingImports]
from streamlit_extras.app_logo import add_logo  # pyright: ignore[reportMissingImports]
from streamlit_extras.colored_header import colored_header  # pyright: ignore[reportMissingImports]
from streamlit_extras.stateful_button import button  # pyright: ignore[reportMissingImports]
from streamlit_extras.metric_cards import style_metric_cards  # pyright: ignore[reportMissingImports]
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go  # pyright: ignore[reportMissingImports]
from plotly.subplots import make_subplots  # pyright: ignore[reportMissingImports]

# 页面配置
st.set_page_config(
    page_title="课堂考勤签到系统",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 导入自定义组件
from utils.auth import AuthManager
from utils.api_client import APIClient
from components.navigation import render_navigation
from components.forms import render_login_form

# 初始化认证管理器和API客户端
@st.cache_resource
def init_auth():
    return AuthManager()

@st.cache_resource
def init_api_client():
    return APIClient()

auth_manager = init_auth()
api_client = init_api_client()

# 离线模式用户数据
OFFLINE_USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "管理员", "id": 1},
    "teacher": {"password": "teacher123", "role": "teacher", "name": "张老师", "id": 2},
    "student": {"password": "student123", "role": "student", "name": "李同学", "id": 3}
}

def offline_login(username: str, password: str):
    """离线登录功能"""
    if username in OFFLINE_USERS and OFFLINE_USERS[username]["password"] == password:
        user_data = OFFLINE_USERS[username]
        return {
            "access_token": f"mock_token_{username}_{datetime.now().timestamp()}",
            "token_type": "bearer",
            "user": {
                "id": user_data["id"],
                "username": username,
                "name": user_data["name"],
                "role": user_data["role"]
            }
        }
    return None

# 自定义CSS样式
def load_custom_css():
    st.markdown("""
    <style>
    /* 主标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 卡片样式 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* 状态指示器 */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online { background-color: #28a745; }
    .status-offline { background-color: #dc3545; }
    .status-pending { background-color: #ffc107; }
    
    /* 动画效果 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 加载自定义样式
load_custom_css()

def main():
    """主应用函数"""
    
    # 渲染导航栏
    render_navigation()
    
    # 检查用户登录状态
    if not auth_manager.is_logged_in():
        show_login_page()
    else:
        show_main_dashboard()

def show_login_page():
    """显示登录页面"""
    
    # 主标题
    st.markdown('<h1 class="main-title fade-in">📚 课堂考勤签到系统</h1>', unsafe_allow_html=True)
    
    # 创建两列布局
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 登录表单
        st.markdown("### 🔐 用户登录")
        
        # 离线登录表单
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
            st.write(f"- 可用用户: {list(OFFLINE_USERS.keys())}")
            
            # 尝试离线登录
            login_result = offline_login(username, password)
            
            if login_result:
                # 保存登录状态
                st.session_state["logged_in"] = True
                st.session_state["user_info"] = login_result["user"]
                st.session_state["access_token"] = login_result["access_token"]
                
                st.success("✅ 离线登录成功！")
                st.balloons()
                
                # 显示用户信息
                st.info(f"欢迎，{login_result['user']['name']}！")
                
                # 刷新页面
                st.rerun()
            else:
                st.error("❌ 用户名或密码错误")
                st.write("**可用的测试账户:**")
                for user, data in OFFLINE_USERS.items():
                    st.write(f"- **{user}**: {data['name']} (密码: {data['password']})")
        
        # 演示账户信息
        with st.expander("📋 演示账户信息", expanded=True):
            st.markdown("""
            **管理员账户：**
            - 用户名：admin
            - 密码：admin123
            
            **教师账户：**
            - 用户名：teacher
            - 密码：teacher123
            
            **学生账户：**
            - 用户名：student
            - 密码：student123
            """)
        
        # 系统状态
        st.markdown("### 📊 系统状态")
        
        # 模拟系统状态检查
        col_status1, col_status2, col_status3 = st.columns(3)
        
        with col_status1:
            st.metric(
                label="在线用户",
                value="156",
                delta="+12"
            )
        
        with col_status2:
            st.metric(
                label="今日签到",
                value="1,234",
                delta="+89"
            )
        
        with col_status3:
            st.metric(
                label="系统状态",
                value="正常",
                delta="99.9%"
            )

def show_main_dashboard():
    """显示主仪表板"""
    
    user_info = auth_manager.get_user_info()
    user_role = user_info.get('role', 'student')
    
    # 根据用户角色显示不同的仪表板
    if user_role == 'student':
        show_student_dashboard(user_info)
    elif user_role == 'teacher':
        show_teacher_dashboard(user_info)
    elif user_role == 'admin':
        show_admin_dashboard(user_info)
    else:
        st.error("未知用户角色")

def show_student_dashboard(user_info):
    """学生仪表板"""
    
    # 页面标题
    st.markdown(f'<h1 class="main-title">👨‍🎓 欢迎，{user_info.get("name", "学生")}</h1>', unsafe_allow_html=True)
    
    # 快速操作区域
    st.markdown("### 🚀 快速操作")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📱 二维码签到", use_container_width=True):
            st.switch_page("pages/1_学生端.py")
    
    with col2:
        if st.button("📍 位置签到", use_container_width=True):
            st.switch_page("pages/1_学生端.py")
    
    with col3:
        if st.button("📊 考勤记录", use_container_width=True):
            st.switch_page("pages/1_学生端.py")
    
    with col4:
        if st.button("📝 异常反馈", use_container_width=True):
            st.switch_page("pages/1_学生端.py")
    
    # 今日考勤状态
    st.markdown("### 📅 今日考勤状态")
    
    # 模拟今日考勤数据
    attendance_data = {
        '课程': ['数据结构', '操作系统', '计算机网络', '数据库原理'],
        '签到时间': ['09:00', '14:00', '10:30', '16:00'],
        '状态': ['正常', '迟到', '正常', '正常'],
        '签到方式': ['二维码', '位置', '二维码', '二维码']
    }
    
    df_attendance = pd.DataFrame(attendance_data)
    
    # 使用彩色表格显示
    st.dataframe(
        df_attendance,
        use_container_width=True,
        hide_index=True
    )
    
    # 个人统计
    st.markdown("### 📈 个人统计")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("本月出勤", "28", "95%")
    
    with col2:
        st.metric("迟到次数", "3", "-1")
    
    with col3:
        st.metric("缺勤次数", "1", "0")
    
    with col4:
        st.metric("出勤率", "93.3%", "+2.1%")

def show_teacher_dashboard(user_info):
    """教师仪表板"""
    
    # 页面标题
    st.markdown(f'<h1 class="main-title">👨‍🏫 欢迎，{user_info.get("name", "教师")}</h1>', unsafe_allow_html=True)
    
    # 快速操作区域
    st.markdown("### 🚀 快速操作")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 出勤统计", use_container_width=True):
            st.switch_page("pages/2_教师端.py")
    
    with col2:
        if st.button("✏️ 补签管理", use_container_width=True):
            st.switch_page("pages/2_教师端.py")
    
    with col3:
        if st.button("📋 反馈处理", use_container_width=True):
            st.switch_page("pages/2_教师端.py")
    
    with col4:
        if st.button("📈 数据分析", use_container_width=True):
            st.switch_page("pages/2_教师端.py")
    
    # 实时出勤率
    st.markdown("### 📊 实时出勤率")
    
    # 创建出勤率环形图
    fig = go.Figure(go.Pie(
        labels=['已签到', '未签到'],
        values=[85, 15],
        hole=0.6,
        marker_colors=['#28a745', '#dc3545']
    ))
    
    fig.update_layout(
        title="今日出勤率：85%",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 课程统计
    st.markdown("### 📚 课程统计")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总课程数", "8", "+1")
    
    with col2:
        st.metric("平均出勤率", "87.5%", "+3.2%")
    
    with col3:
        st.metric("待处理反馈", "5", "+2")

def show_admin_dashboard(user_info):
    """管理员仪表板"""
    
    # 页面标题
    st.markdown(f'<h1 class="main-title">👨‍💼 欢迎，{user_info.get("name", "管理员")}</h1>', unsafe_allow_html=True)
    
    # 快速操作区域
    st.markdown("### 🚀 快速操作")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👥 用户管理", use_container_width=True):
            st.switch_page("pages/3_管理员端.py")
    
    with col2:
        if st.button("📊 报表查询", use_container_width=True):
            st.switch_page("pages/3_管理员端.py")
    
    with col3:
        if st.button("📈 数据分析", use_container_width=True):
            st.switch_page("pages/3_管理员端.py")
    
    with col4:
        if st.button("⚙️ 系统设置", use_container_width=True):
            st.switch_page("pages/3_管理员端.py")
    
    # 系统概览
    st.markdown("### 📊 系统概览")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总用户数", "1,256", "+23")
    
    with col2:
        st.metric("今日签到", "1,234", "+89")
    
    with col3:
        st.metric("系统状态", "正常", "99.9%")
    
    with col4:
        st.metric("异常预警", "3", "-1")
    
    # 全校出勤率趋势
    st.markdown("### 📈 全校出勤率趋势")
    
    # 模拟趋势数据
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    attendance_rates = [85 + (i % 10) - 5 for i in range(len(dates))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=attendance_rates,
        mode='lines+markers',
        name='出勤率',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    # 添加预警线
    fig.add_hline(y=80, line_dash="dash", line_color="red", 
                  annotation_text="预警线 (80%)")
    
    fig.update_layout(
        title="全校出勤率趋势图",
        xaxis_title="日期",
        yaxis_title="出勤率 (%)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
