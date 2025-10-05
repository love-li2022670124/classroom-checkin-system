"""
教师端功能页面
包含：实时出勤率统计、补签管理、反馈处理、数据分析
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go  # pyright: ignore[reportMissingImports]
from plotly.subplots import make_subplots  # pyright: ignore[reportMissingImports]
from streamlit_extras.colored_header import colored_header  # pyright: ignore[reportMissingImports]
from streamlit_extras.metric_cards import style_metric_cards  # pyright: ignore[reportMissingImports]

from utils.auth import AuthManager
from utils.api_client import APIClient

# 页面配置
st.set_page_config(
    page_title="教师端 - 课堂考勤签到系统",
    page_icon="👨‍🏫",
    layout="wide"
)

# 初始化组件
@st.cache_resource
def init_components():
    auth_manager = AuthManager()
    api_client = APIClient()
    return auth_manager, api_client

auth_manager, api_client = init_components()

# 检查登录状态
if not auth_manager.is_logged_in():
    st.warning("请先登录")
    st.stop()

# 检查教师权限
if not auth_manager.has_permission("teacher"):
    st.error("权限不足：需要教师权限")
    st.stop()

user_info = auth_manager.get_user_info()
teacher_id = auth_manager.get_user_id()

# 页面标题
colored_header(
    label=f"👨‍🏫 教师端 - 欢迎，{user_info.get('name', '教师')}",
    description="课堂考勤管理系统",
    color_name="green-70"
)

# 创建选项卡
tab1, tab2, tab3, tab4 = st.tabs(["📊 实时出勤率", "✏️ 补签管理", "📋 反馈处理", "📈 数据分析"])

with tab1:
    st.markdown("### 📊 实时出勤率统计")
    
    # 课程选择
    col1, col2 = st.columns([2, 1])
    
    with col1:
        course_options = {
            "数据结构": 1,
            "操作系统": 2,
            "计算机网络": 3,
            "数据库原理": 4
        }
        
        selected_course = st.selectbox(
            "选择课程",
            options=list(course_options.keys()),
            key="attendance_course_select"
        )
        course_id = course_options[selected_course]
    
    with col2:
        if st.button("🔄 刷新数据", type="primary", use_container_width=True):
            st.rerun()
    
    # 实时出勤率指标
    st.markdown("#### 📈 实时出勤率")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总人数", "45", "0")
    
    with col2:
        st.metric("已签到", "38", "+3")
    
    with col3:
        st.metric("未签到", "7", "-3")
    
    with col4:
        attendance_rate = 38 / 45 * 100
        st.metric("出勤率", f"{attendance_rate:.1f}%", "+6.7%")
    
    # 出勤率环形图
    st.markdown("#### 📊 出勤率分布")
    
    fig = go.Figure(go.Pie(
        labels=['已签到', '未签到'],
        values=[38, 7],
        hole=0.6,
        marker_colors=['#28a745', '#dc3545'],
        textinfo='label+percent',
        textfont_size=14
    ))
    
    fig.update_layout(
        title=f"{selected_course} - 实时出勤率：{attendance_rate:.1f}%",
        showlegend=True,
        height=400,
        annotations=[dict(text=f'{attendance_rate:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 详细出勤记录
    st.markdown("#### 📋 详细出勤记录")
    
    # 模拟出勤数据
    attendance_data = []
    for i in range(45):
        student_id = f"2024001{i:02d}"
        student_name = f"学生{i+1:02d}"
        
        if i < 38:  # 已签到
            status = "正常" if i < 35 else "迟到"
            sign_time = "09:00" if i < 35 else "09:15"
            method = "二维码" if i % 2 == 0 else "位置"
        else:  # 未签到
            status = "缺勤"
            sign_time = "-"
            method = "-"
        
        attendance_data.append({
            "student_id": student_id,
            "student_name": student_name,
            "status": status,
            "sign_time": sign_time,
            "method": method
        })
    
    df_attendance = pd.DataFrame(attendance_data)
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(df_attendance)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_selection('multiple', use_checkbox=True)
        
        # 设置列属性
        gb.configure_column("student_id", header_name="学号", width=120)
        gb.configure_column("student_name", header_name="姓名", width=120)
        gb.configure_column("status", header_name="状态", width=100)
        gb.configure_column("sign_time", header_name="签到时间", width=120)
        gb.configure_column("method", header_name="签到方式", width=120)
        
        # 设置状态列的颜色
        def status_cell_renderer(params):
            status = params.value
            color_map = {
                "正常": "#28a745",
                "迟到": "#ffc107",
                "缺勤": "#dc3545"
            }
            color = color_map.get(status, "#6c757d")
            return f'<span style="color: {color}; font-weight: bold;">{status}</span>'
        
        gb.configure_column("status", cellRenderer=status_cell_renderer)
        
        gridOptions = gb.build()
        
        selected_rows = AgGrid(df_attendance, gridOptions=gridOptions, enable_enterprise_modules=True)
        
        # 显示选中的学生
        if selected_rows['data']:
            st.info(f"已选择 {len(selected_rows['data'])} 名学生")
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(df_attendance, use_container_width=True)

with tab2:
    st.markdown("### ✏️ 补签管理")
    
    # 补签表单
    with st.form("makeup_form"):
        st.markdown("#### 📝 手动补签")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 学生选择
            student_options = {}
            for i in range(45):
                student_id = f"2024001{i:02d}"
                student_name = f"学生{i+1:02d}"
                student_options[f"{student_name} ({student_id})"] = student_id
            
            selected_student = st.selectbox(
                "选择学生",
                options=list(student_options.keys()),
                key="makeup_student_select"
            )
            student_id = student_options[selected_student]
        
        with col2:
            # 课程选择
            course_options = {
                "数据结构": 1,
                "操作系统": 2,
                "计算机网络": 3,
                "数据库原理": 4
            }
            
            selected_course = st.selectbox(
                "选择课程",
                options=list(course_options.keys()),
                key="makeup_course_select"
            )
            course_id = course_options[selected_course]
        
        # 补签原因
        reason_options = [
            "病假",
            "事假",
            "迟到",
            "系统故障",
            "其他原因"
        ]
        
        reason = st.selectbox(
            "补签原因",
            options=reason_options,
            key="makeup_reason_select"
        )
        
        # 详细说明
        detail_reason = st.text_area(
            "详细说明",
            placeholder="请详细说明补签原因...",
            height=100,
            key="makeup_detail_reason"
        )
        
        # 补签时间
        makeup_time = st.datetime_input(
            "补签时间",
            value=datetime.now(),
            key="makeup_time_input"
        )
        
        # 提交按钮
        submit_button = st.form_submit_button(
            "✅ 确认补签",
            type="primary",
            use_container_width=True
        )
        
        if submit_button:
            if detail_reason.strip():
                # 执行补签
                with st.spinner("正在处理补签..."):
                    # 这里应该调用API进行补签
                    st.success(f"补签成功！已为 {selected_student} 在 {selected_course} 课程中补签。")
                    
                    # 记录补签信息
                    makeup_record = {
                        "student_id": student_id,
                        "student_name": selected_student,
                        "course": selected_course,
                        "reason": reason,
                        "detail": detail_reason,
                        "makeup_time": makeup_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "teacher_id": teacher_id,
                        "teacher_name": user_info.get('name', '教师')
                    }
                    
                    if "makeup_records" not in st.session_state:
                        st.session_state["makeup_records"] = []
                    
                    st.session_state["makeup_records"].append(makeup_record)
            else:
                st.error("请填写详细说明")
    
    # 补签记录
    st.markdown("#### 📜 补签记录")
    
    if "makeup_records" in st.session_state and st.session_state["makeup_records"]:
        makeup_df = pd.DataFrame(st.session_state["makeup_records"])
        
        # 使用streamlit-aggrid显示表格
        try:
            from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
            
            gb = GridOptionsBuilder.from_dataframe(makeup_df)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_side_bar()
            
            # 设置列属性
            gb.configure_column("student_name", header_name="学生姓名", width=120)
            gb.configure_column("course", header_name="课程", width=120)
            gb.configure_column("reason", header_name="原因", width=100)
            gb.configure_column("detail", header_name="详细说明", width=200)
            gb.configure_column("makeup_time", header_name="补签时间", width=150)
            gb.configure_column("teacher_name", header_name="操作教师", width=120)
            
            gridOptions = gb.build()
            
            AgGrid(makeup_df, gridOptions=gridOptions, enable_enterprise_modules=True)
            
        except ImportError:
            # 如果streamlit-aggrid不可用，使用默认表格
            st.dataframe(makeup_df, use_container_width=True)
    else:
        st.info("暂无补签记录")

with tab3:
    st.markdown("### 📋 反馈处理")
    
    # 反馈筛选
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "状态筛选",
            options=["全部", "待处理", "处理中", "已处理", "已关闭"],
            key="feedback_status_filter"
        )
    
    with col2:
        priority_filter = st.selectbox(
            "优先级筛选",
            options=["全部", "低", "中", "高", "紧急"],
            key="feedback_priority_filter"
        )
    
    with col3:
        if st.button("🔄 刷新反馈", type="primary", use_container_width=True):
            st.rerun()
    
    # 模拟反馈数据
    feedback_data = [
        {
            "id": 1,
            "student_name": "张三",
            "course_name": "数据结构",
            "feedback_type": "签到异常",
            "content": "二维码扫描失败，无法正常签到",
            "priority": "高",
            "status": "待处理",
            "submit_time": "2024-01-15 09:30:00",
            "handle_time": None
        },
        {
            "id": 2,
            "student_name": "李四",
            "course_name": "操作系统",
            "feedback_type": "时间错误",
            "content": "系统显示签到时间与实际时间不符",
            "priority": "中",
            "status": "处理中",
            "submit_time": "2024-01-15 10:15:00",
            "handle_time": "2024-01-15 10:20:00"
        },
        {
            "id": 3,
            "student_name": "王五",
            "course_name": "计算机网络",
            "feedback_type": "位置错误",
            "content": "位置签到显示距离过远，但实际在教室内",
            "priority": "紧急",
            "status": "待处理",
            "submit_time": "2024-01-15 11:00:00",
            "handle_time": None
        }
    ]
    
    # 显示反馈列表
    st.markdown("#### 📋 待处理反馈")
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        df_feedback = pd.DataFrame(feedback_data)
        
        gb = GridOptionsBuilder.from_dataframe(df_feedback)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_selection('multiple', use_checkbox=True)
        
        # 设置列属性
        gb.configure_column("id", header_name="ID", width=80)
        gb.configure_column("student_name", header_name="学生姓名", width=120)
        gb.configure_column("course_name", header_name="课程名称", width=120)
        gb.configure_column("feedback_type", header_name="反馈类型", width=120)
        gb.configure_column("content", header_name="反馈内容", width=200)
        gb.configure_column("priority", header_name="优先级", width=100)
        gb.configure_column("status", header_name="状态", width=100)
        gb.configure_column("submit_time", header_name="提交时间", width=150)
        gb.configure_column("handle_time", header_name="处理时间", width=150)
        
        # 设置优先级列的颜色
        def priority_cell_renderer(params):
            priority = params.value
            color_map = {
                "低": "#28a745",
                "中": "#ffc107",
                "高": "#fd7e14",
                "紧急": "#dc3545"
            }
            color = color_map.get(priority, "#6c757d")
            return f'<span style="color: {color}; font-weight: bold;">{priority}</span>'
        
        gb.configure_column("priority", cellRenderer=priority_cell_renderer)
        
        # 设置状态列的颜色
        def status_cell_renderer(params):
            status = params.value
            color_map = {
                "待处理": "#ffc107",
                "处理中": "#17a2b8",
                "已处理": "#28a745",
                "已关闭": "#6c757d"
            }
            color = color_map.get(status, "#6c757d")
            return f'<span style="color: {color}; font-weight: bold;">{status}</span>'
        
        gb.configure_column("status", cellRenderer=status_cell_renderer)
        
        gridOptions = gb.build()
        
        selected_rows = AgGrid(df_feedback, gridOptions=gridOptions, enable_enterprise_modules=True)
        
        # 显示选中的反馈
        if selected_rows['data']:
            st.info(f"已选择 {len(selected_rows['data'])} 条反馈")
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(pd.DataFrame(feedback_data), use_container_width=True)
    
    # 反馈处理
    st.markdown("#### 🔧 反馈处理")
    
    if selected_rows and selected_rows['data']:
        selected_feedback = selected_rows['data'][0]  # 选择第一个反馈进行处理
        
        with st.expander(f"处理反馈 #{selected_feedback['id']} - {selected_feedback['feedback_type']}"):
            st.write(f"**学生：** {selected_feedback['student_name']}")
            st.write(f"**课程：** {selected_feedback['course_name']}")
            st.write(f"**反馈内容：** {selected_feedback['content']}")
            st.write(f"**优先级：** {selected_feedback['priority']}")
            st.write(f"**提交时间：** {selected_feedback['submit_time']}")
            
            # 处理表单
            with st.form("handle_feedback_form"):
                action = st.selectbox(
                    "处理动作",
                    options=["处理中", "已处理", "已关闭"],
                    key="feedback_action"
                )
                
                response_content = st.text_area(
                    "处理回复",
                    placeholder="请输入处理回复...",
                    height=100,
                    key="feedback_response"
                )
                
                submit_handle = st.form_submit_button(
                    "✅ 确认处理",
                    type="primary",
                    use_container_width=True
                )
                
                if submit_handle:
                    if response_content.strip():
                        st.success(f"反馈处理成功！状态已更新为：{action}")
                        
                        # 更新反馈状态
                        for feedback in feedback_data:
                            if feedback['id'] == selected_feedback['id']:
                                feedback['status'] = action
                                feedback['handle_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                break
                    else:
                        st.error("请填写处理回复")
    else:
        st.info("请先选择要处理的反馈")

with tab4:
    st.markdown("### 📈 数据分析")
    
    # 时间范围选择
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=30),
            key="analysis_start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "结束日期",
            value=datetime.now(),
            key="analysis_end_date"
        )
    
    # 分析按钮
    if st.button("📊 生成分析报告", type="primary"):
        with st.spinner("正在生成分析报告..."):
            # 模拟分析数据
            st.session_state["analysis_generated"] = True
    
    if st.session_state.get("analysis_generated", False):
        # 整体统计
        st.markdown("#### 📊 整体统计")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总课程数", "32", "+2")
        
        with col2:
            st.metric("平均出勤率", "87.5%", "+3.2%")
        
        with col3:
            st.metric("迟到次数", "15", "-3")
        
        with col4:
            st.metric("缺勤次数", "8", "-2")
        
        # 出勤率趋势图
        st.markdown("#### 📈 出勤率趋势")
        
        # 模拟趋势数据
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
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
        
        # 添加平均线
        avg_rate = sum(attendance_rates) / len(attendance_rates)
        fig.add_hline(y=avg_rate, line_dash="dash", line_color="red", 
                      annotation_text=f"平均出勤率 ({avg_rate:.1f}%)")
        
        fig.update_layout(
            title="出勤率趋势图",
            xaxis_title="日期",
            yaxis_title="出勤率 (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 课程出勤率对比
        st.markdown("#### 📚 课程出勤率对比")
        
        course_attendance = {
            "数据结构": 92.5,
            "操作系统": 88.3,
            "计算机网络": 85.7,
            "数据库原理": 90.1
        }
        
        fig = px.bar(
            x=list(course_attendance.keys()),
            y=list(course_attendance.values()),
            title="各课程出勤率对比",
            labels={'x': '课程', 'y': '出勤率 (%)'}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # 签到方式统计
        st.markdown("#### 📱 签到方式统计")
        
        sign_methods = {
            "二维码": 65,
            "位置": 35
        }
        
        fig = go.Figure(go.Pie(
            labels=list(sign_methods.keys()),
            values=list(sign_methods.values()),
            hole=0.4
        ))
        
        fig.update_layout(
            title="签到方式分布",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 异常情况统计
        st.markdown("#### ⚠️ 异常情况统计")
        
        anomaly_data = {
            "迟到": 15,
            "早退": 5,
            "缺勤": 8,
            "系统故障": 3
        }
        
        fig = px.bar(
            x=list(anomaly_data.keys()),
            y=list(anomaly_data.values()),
            title="异常情况统计",
            labels={'x': '异常类型', 'y': '次数'},
            color=list(anomaly_data.values()),
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# 侧边栏信息
with st.sidebar:
    st.markdown("### 👨‍🏫 教师信息")
    st.write(f"**姓名：** {user_info.get('name', '未知')}")
    st.write(f"**工号：** {user_info.get('teacher_id', '未知')}")
    st.write(f"**部门：** {user_info.get('department', '未知')}")
    
    st.markdown("### 📊 今日统计")
    st.metric("今日课程", "4", "0")
    st.metric("平均出勤率", "87.5%", "+3.2%")
    st.metric("待处理反馈", "3", "+1")
    
    st.markdown("### 🔧 操作")
    if st.button("🚪 退出登录", use_container_width=True):
        auth_manager.logout()
        st.rerun()
