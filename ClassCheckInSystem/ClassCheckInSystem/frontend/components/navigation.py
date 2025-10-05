"""
导航组件模块
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
from streamlit_extras.colored_header import colored_header  # pyright: ignore[reportMissingImports]
from streamlit_extras.app_logo import add_logo  # pyright: ignore[reportMissingImports]

def render_navigation():
    """渲染导航栏"""
    st.markdown("""
    <style>
    .nav-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .nav-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin: 0;
    }
    
    .nav-subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
    }
    </style>
    
    <div class="nav-container">
        <h1 class="nav-title">📚 课堂考勤签到系统</h1>
        <p class="nav-subtitle">Classroom Attendance Sign-in System</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_navigation():
    """渲染侧边栏导航"""
    with st.sidebar:
        st.markdown("### 🧭 导航菜单")
        
        # 根据用户角色显示不同的导航选项
        if st.session_state.get("user_role") == "student":
            st.markdown("**学生功能**")
            if st.button("📱 二维码签到", use_container_width=True):
                st.switch_page("pages/1_学生端.py")
            if st.button("📍 位置签到", use_container_width=True):
                st.switch_page("pages/1_学生端.py")
            if st.button("📊 考勤记录", use_container_width=True):
                st.switch_page("pages/1_学生端.py")
            if st.button("📝 异常反馈", use_container_width=True):
                st.switch_page("pages/1_学生端.py")
        
        elif st.session_state.get("user_role") == "teacher":
            st.markdown("**教师功能**")
            if st.button("📊 出勤统计", use_container_width=True):
                st.switch_page("pages/2_教师端.py")
            if st.button("✏️ 补签管理", use_container_width=True):
                st.switch_page("pages/2_教师端.py")
            if st.button("📋 反馈处理", use_container_width=True):
                st.switch_page("pages/2_教师端.py")
            if st.button("📈 数据分析", use_container_width=True):
                st.switch_page("pages/2_教师端.py")
        
        elif st.session_state.get("user_role") == "admin":
            st.markdown("**管理员功能**")
            if st.button("👥 用户管理", use_container_width=True):
                st.switch_page("pages/3_管理员端.py")
            if st.button("📚 课程管理", use_container_width=True):
                st.switch_page("pages/3_管理员端.py")
            if st.button("📊 报表查询", use_container_width=True):
                st.switch_page("pages/3_管理员端.py")
            if st.button("📈 数据分析", use_container_width=True):
                st.switch_page("pages/3_管理员端.py")
            if st.button("⚙️ 系统设置", use_container_width=True):
                st.switch_page("pages/3_管理员端.py")

def render_breadcrumb(current_page: str):
    """渲染面包屑导航"""
    breadcrumb_items = [
        ("🏠 首页", "app.py"),
        ("👨‍🎓 学生端", "pages/1_学生端.py"),
        ("👨‍🏫 教师端", "pages/2_教师端.py"),
        ("👨‍💼 管理员端", "pages/3_管理员端.py")
    ]
    
    breadcrumb_html = '<nav aria-label="breadcrumb"><ol class="breadcrumb">'
    
    for item_text, item_page in breadcrumb_items:
        if item_page == current_page:
            breadcrumb_html += f'<li class="breadcrumb-item active">{item_text}</li>'
        else:
            breadcrumb_html += f'<li class="breadcrumb-item"><a href="{item_page}">{item_text}</a></li>'
    
    breadcrumb_html += '</ol></nav>'
    
    st.markdown(f"""
    <style>
    .breadcrumb {{
        background-color: #f8f9fa;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        border-radius: 0.375rem;
    }}
    .breadcrumb-item {{
        display: inline-block;
    }}
    .breadcrumb-item + .breadcrumb-item::before {{
        content: ">";
        padding: 0 0.5rem;
        color: #6c757d;
    }}
    .breadcrumb-item.active {{
        color: #495057;
    }}
    .breadcrumb-item a {{
        color: #007bff;
        text-decoration: none;
    }}
    .breadcrumb-item a:hover {{
        text-decoration: underline;
    }}
    </style>
    {breadcrumb_html}
    """, unsafe_allow_html=True)

def render_page_header(title: str, description: str = "", icon: str = ""):
    """渲染页面标题"""
    colored_header(
        label=f"{icon} {title}",
        description=description,
        color_name="blue-70"
    )

def render_footer():
    """渲染页脚"""
    st.markdown("""
    <style>
    .footer {
        background-color: #f8f9fa;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #dee2e6;
        text-align: center;
        color: #6c757d;
    }
    </style>
    
    <div class="footer">
        <p>© 2024 课堂考勤签到系统 | 基于 Streamlit 构建</p>
        <p>Classroom Attendance Sign-in System | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
