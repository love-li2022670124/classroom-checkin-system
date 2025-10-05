"""
通用组件模块
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
from streamlit_extras.colored_header import colored_header  # pyright: ignore[reportMissingImports]
from streamlit_extras.metric_cards import style_metric_cards  # pyright: ignore[reportMissingImports]
from streamlit_extras.stateful_button import button  # pyright: ignore[reportMissingImports]
from streamlit_extras.app_logo import add_logo  # pyright: ignore[reportMissingImports]
import plotly.express as px  # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go  # pyright: ignore[reportMissingImports]
from typing import Dict, List, Any, Optional
import pandas as pd

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

def render_login_form(auth_manager, api_client):
    """渲染登录表单"""
    with st.form("login_form"):
        st.markdown("### 🔐 用户登录")
        
        username = st.text_input(
            "用户名",
            placeholder="请输入用户名",
            help="请输入您的用户名"
        )
        
        password = st.text_input(
            "密码",
            type="password",
            placeholder="请输入密码",
            help="请输入您的密码"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            login_button = st.form_submit_button(
                "🔑 登录",
                type="primary",
                use_container_width=True
            )
        
        with col2:
            remember_me = st.checkbox("记住我")
        
        if login_button:
            if username and password:
                with st.spinner("正在登录..."):
                    success = auth_manager.login(username, password, api_client)
                    if success:
                        st.success("登录成功！")
                        st.rerun()
                    else:
                        st.error("登录失败，请检查用户名和密码")
            else:
                st.error("请输入用户名和密码")

def render_feedback_form(attendance_record: Dict[str, Any]) -> Dict[str, Any]:
    """渲染反馈表单"""
    with st.form("feedback_form"):
        st.markdown("### 📝 考勤异常反馈")
        
        # 显示考勤记录信息
        st.info(f"""
        **考勤记录信息：**
        - 日期：{attendance_record.get('date', '未知')}
        - 课程：{attendance_record.get('course', '未知')}
        - 时间：{attendance_record.get('time', '未知')}
        - 状态：{attendance_record.get('status', '未知')}
        """)
        
        feedback_type = st.selectbox(
            "反馈类型",
            options=["签到异常", "时间错误", "位置错误", "系统问题", "其他"],
            help="请选择问题类型"
        )
        
        feedback_content = st.text_area(
            "详细描述",
            placeholder="请详细描述您遇到的问题...",
            height=100,
            help="请尽可能详细地描述问题"
        )
        
        priority = st.selectbox(
            "优先级",
            options=["低", "中", "高", "紧急"],
            help="请选择问题的紧急程度"
        )
        
        contact_method = st.selectbox(
            "联系方式",
            options=["邮箱", "电话", "微信", "QQ"],
            help="我们如何联系您"
        )
        
        contact_info = st.text_input(
            "联系方式信息",
            placeholder="请输入您的联系方式",
            help="请输入具体的联系方式"
        )
        
        submit_button = st.form_submit_button(
            "📤 提交反馈",
            type="primary",
            use_container_width=True
        )
        
        if submit_button:
            if feedback_content.strip():
                feedback_data = {
                    "attendance_record": attendance_record,
                    "feedback_type": feedback_type,
                    "feedback_content": feedback_content,
                    "priority": priority,
                    "contact_method": contact_method,
                    "contact_info": contact_info,
                    "submit_time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "status": "待处理"
                }
                
                st.success("反馈提交成功！我们会尽快处理您的问题。")
                return feedback_data
            else:
                st.error("请填写反馈内容")
                return None
    
    return None

def render_attendance_table(attendance_data: List[Dict[str, Any]]):
    """渲染考勤记录表格"""
    if not attendance_data:
        st.warning("暂无考勤记录")
        return
    
    df = pd.DataFrame(attendance_data)
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_selection('multiple', use_checkbox=True)
        
        # 设置列属性
        gb.configure_column("date", header_name="日期", width=120)
        gb.configure_column("course", header_name="课程", width=150)
        gb.configure_column("time", header_name="时间", width=100)
        gb.configure_column("method", header_name="签到方式", width=120)
        gb.configure_column("status", header_name="状态", width=100)
        
        # 设置状态列的颜色
        def status_cell_renderer(params):
            status = params.value
            color_map = {
                "正常": "#28a745",
                "迟到": "#ffc107", 
                "缺勤": "#dc3545",
                "早退": "#17a2b8"
            }
            color = color_map.get(status, "#6c757d")
            return f'<span style="color: {color}; font-weight: bold;">{status}</span>'
        
        gb.configure_column("status", cellRenderer=status_cell_renderer)
        
        gridOptions = gb.build()
        
        AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(df, use_container_width=True)

def render_metric_cards(metrics: List[Dict[str, Any]]):
    """渲染指标卡片"""
    if not metrics:
        return
    
    cols = st.columns(len(metrics))
    
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.metric(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta", None)
            )

def render_chart(chart_type: str, data: pd.DataFrame, **kwargs):
    """渲染图表"""
    if chart_type == "line":
        fig = px.line(data, **kwargs)
    elif chart_type == "bar":
        fig = px.bar(data, **kwargs)
    elif chart_type == "pie":
        fig = px.pie(data, **kwargs)
    elif chart_type == "scatter":
        fig = px.scatter(data, **kwargs)
    else:
        st.error(f"不支持的图表类型: {chart_type}")
        return
    
    st.plotly_chart(fig, use_container_width=True)

def render_status_indicator(status: str, text: str = None):
    """渲染状态指示器"""
    status_colors = {
        "online": "#28a745",
        "offline": "#dc3545",
        "pending": "#ffc107",
        "error": "#dc3545",
        "success": "#28a745",
        "warning": "#ffc107",
        "info": "#17a2b8"
    }
    
    color = status_colors.get(status, "#6c757d")
    display_text = text or status
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 0.5rem 0;">
        <div style="width: 12px; height: 12px; background-color: {color}; border-radius: 50%; margin-right: 8px;"></div>
        <span>{display_text}</span>
    </div>
    """, unsafe_allow_html=True)

def render_progress_bar(progress: float, label: str = None):
    """渲染进度条"""
    if label:
        st.write(label)
    
    st.progress(progress)
    st.write(f"{progress:.1%}")

def render_info_box(title: str, content: str, box_type: str = "info"):
    """渲染信息框"""
    box_colors = {
        "info": "#d1ecf1",
        "success": "#d4edda",
        "warning": "#fff3cd",
        "error": "#f8d7da"
    }
    
    box_borders = {
        "info": "#bee5eb",
        "success": "#c3e6cb",
        "warning": "#ffeaa7",
        "error": "#f5c6cb"
    }
    
    color = box_colors.get(box_type, box_colors["info"])
    border = box_borders.get(box_type, box_borders["info"])
    
    st.markdown(f"""
    <div style="background-color: {color}; border: 1px solid {border}; border-radius: 5px; padding: 1rem; margin: 1rem 0;">
        <h4 style="margin: 0 0 0.5rem 0; color: #0c5460;">{title}</h4>
        <p style="margin: 0; color: #0c5460;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def render_loading_spinner(text: str = "加载中..."):
    """渲染加载动画"""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div style="border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite; margin: 0 auto;"></div>
        <p style="margin-top: 1rem; color: #666;">{text}</p>
    </div>
    
    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_success_message(message: str):
    """渲染成功消息"""
    st.markdown(f"""
    <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px; padding: 1rem; margin: 1rem 0;">
        <div style="display: flex; align-items: center;">
            <span style="color: #155724; font-size: 1.2rem; margin-right: 0.5rem;">✅</span>
            <span style="color: #155724;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_error_message(message: str):
    """渲染错误消息"""
    st.markdown(f"""
    <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 1rem; margin: 1rem 0;">
        <div style="display: flex; align-items: center;">
            <span style="color: #721c24; font-size: 1.2rem; margin-right: 0.5rem;">❌</span>
            <span style="color: #721c24;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_warning_message(message: str):
    """渲染警告消息"""
    st.markdown(f"""
    <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 1rem; margin: 1rem 0;">
        <div style="display: flex; align-items: center;">
            <span style="color: #856404; font-size: 1.2rem; margin-right: 0.5rem;">⚠️</span>
            <span style="color: #856404;">{message}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
