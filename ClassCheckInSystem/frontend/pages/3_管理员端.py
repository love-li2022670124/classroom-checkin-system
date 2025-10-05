"""
管理员端功能页面
包含：用户管理、课程管理、报表查询、数据分析、系统设置
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go  # pyright: ignore[reportMissingImports]
from plotly.subplots import make_subplots  # pyright: ignore[reportMissingImports]
from streamlit_extras.colored_header import colored_header  # pyright: ignore[reportMissingImports]
from streamlit_extras.metric_cards import style_metric_cards  # pyright: ignore[reportMissingImports]
import io

from utils.auth import AuthManager
from utils.api_client import APIClient
from components.tables import render_course_table, render_user_table

# 页面配置
st.set_page_config(
    page_title="管理员端 - 课堂考勤签到系统",
    page_icon="👨‍💼",
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

# 检查管理员权限
if not auth_manager.has_permission("admin"):
    st.error("权限不足：需要管理员权限")
    st.stop()

user_info = auth_manager.get_user_info()
admin_id = auth_manager.get_user_id()

# 页面标题
colored_header(
    label=f"👨‍💼 管理员端 - 欢迎，{user_info.get('name', '管理员')}",
    description="系统管理中心",
    color_name="red-70"
)

# 创建选项卡
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 用户管理", "📚 课程管理", "📊 报表查询", "📈 数据分析", "⚙️ 系统设置"])

with tab1:
    st.markdown("### 👥 用户管理")
    
    # 用户类型选择
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        user_type = st.selectbox(
            "用户类型",
            options=["全部", "学生", "教师", "管理员"],
            key="user_type_filter"
        )
    
    with col2:
        user_status = st.selectbox(
            "用户状态",
            options=["全部", "active", "inactive", "pending", "banned"],
            key="user_status_filter"
        )
    
    with col3:
        if st.button("🔄 刷新用户列表", type="primary"):
            st.rerun()
    
    # 模拟用户数据
    users_data = []
    for i in range(100):
        if i < 80:  # 学生
            user_type_val = "student"
            username = f"student{i+1:03d}"
            name = f"学生{i+1:03d}"
            email = f"student{i+1:03d}@university.edu"
        elif i < 95:  # 教师
            user_type_val = "teacher"
            username = f"teacher{i-79:03d}"
            name = f"教师{i-79:03d}"
            email = f"teacher{i-79:03d}@university.edu"
        else:  # 管理员
            user_type_val = "admin"
            username = f"admin{i-94:03d}"
            name = f"管理员{i-94:03d}"
            email = f"admin{i-94:03d}@university.edu"
        
        users_data.append({
            "id": i + 1,
            "username": username,
            "name": name,
            "email": email,
            "role": user_type_val,
            "status": "active" if i % 10 != 0 else "inactive",
            "created_at": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            "last_login": (datetime.now() - timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # 显示用户表格
    st.markdown("#### 📋 用户列表")
    
    selected_users = render_user_table(users_data)
    
    # 用户操作
    st.markdown("#### 🔧 用户操作")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ 添加用户", use_container_width=True):
            st.session_state["show_add_user_form"] = True
    
    with col2:
        if st.button("✏️ 编辑用户", use_container_width=True):
            if selected_users:
                st.session_state["show_edit_user_form"] = True
                st.session_state["selected_user"] = selected_users[0]
            else:
                st.warning("请先选择要编辑的用户")
    
    with col3:
        if st.button("🗑️ 删除用户", use_container_width=True):
            if selected_users:
                st.session_state["show_delete_confirm"] = True
            else:
                st.warning("请先选择要删除的用户")
    
    with col4:
        if st.button("📊 批量操作", use_container_width=True):
            if selected_users:
                st.session_state["show_batch_operation"] = True
            else:
                st.warning("请先选择要操作的用户")
    
    # 添加用户表单
    if st.session_state.get("show_add_user_form", False):
        with st.expander("➕ 添加新用户", expanded=True):
            with st.form("add_user_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_username = st.text_input("用户名", key="new_username")
                    new_name = st.text_input("姓名", key="new_name")
                    new_email = st.text_input("邮箱", key="new_email")
                
                with col2:
                    new_role = st.selectbox("角色", options=["student", "teacher", "admin"], key="new_role")
                    new_password = st.text_input("密码", type="password", key="new_password")
                    new_status = st.selectbox("状态", options=["active", "inactive"], key="new_status")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("✅ 确认添加", type="primary"):
                        if new_username and new_name and new_email and new_password:
                            st.success(f"用户 {new_username} 添加成功！")
                            st.session_state["show_add_user_form"] = False
                            st.rerun()
                        else:
                            st.error("请填写所有必填字段")
                
                with col2:
                    if st.form_submit_button("❌ 取消"):
                        st.session_state["show_add_user_form"] = False
                        st.rerun()
    
    # 编辑用户表单
    if st.session_state.get("show_edit_user_form", False):
        selected_user = st.session_state.get("selected_user")
        if selected_user:
            with st.expander(f"✏️ 编辑用户 - {selected_user['姓名']}", expanded=True):
                with st.form("edit_user_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_username = st.text_input("用户名", value=selected_user['用户名'], key="edit_username")
                        edit_name = st.text_input("姓名", value=selected_user['姓名'], key="edit_name")
                        edit_email = st.text_input("邮箱", value=selected_user['邮箱'], key="edit_email")
                    
                    with col2:
                        edit_role = st.selectbox("角色", options=["student", "teacher", "admin"], 
                                               index=["student", "teacher", "admin"].index(selected_user['角色']), key="edit_role")
                        edit_status = st.selectbox("状态", options=["active", "inactive", "pending", "banned"],
                                                 index=["active", "inactive", "pending", "banned"].index(selected_user['状态']), key="edit_status")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.form_submit_button("✅ 确认修改", type="primary"):
                            st.success(f"用户 {edit_username} 修改成功！")
                            st.session_state["show_edit_user_form"] = False
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("❌ 取消"):
                            st.session_state["show_edit_user_form"] = False
                            st.rerun()
    
    # 删除确认
    if st.session_state.get("show_delete_confirm", False):
        st.warning("⚠️ 确认删除选中的用户吗？此操作不可撤销！")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ 确认删除", type="primary"):
                st.success("用户删除成功！")
                st.session_state["show_delete_confirm"] = False
                st.rerun()
        
        with col2:
            if st.button("❌ 取消"):
                st.session_state["show_delete_confirm"] = False
                st.rerun()

with tab2:
    st.markdown("### 📚 课程管理")
    
    # 课程操作
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("➕ 添加课程", type="primary"):
            st.session_state["show_add_course_form"] = True
    
    with col2:
        if st.button("🔄 刷新课程", type="primary"):
            st.rerun()
    
    with col3:
        course_search = st.text_input("搜索课程", placeholder="输入课程名称或代码...")
    
    # 模拟课程数据
    courses_data = [
        {
            "id": 1,
            "name": "数据结构",
            "code": "CS101",
            "teacher": "张教授",
            "schedule": "周一 09:00-11:00",
            "location": "教学楼A101",
            "credits": 3,
            "status": "active"
        },
        {
            "id": 2,
            "name": "操作系统",
            "code": "CS102",
            "teacher": "李教授",
            "schedule": "周二 14:00-16:00",
            "location": "教学楼A102",
            "credits": 4,
            "status": "active"
        },
        {
            "id": 3,
            "name": "计算机网络",
            "code": "CS103",
            "teacher": "王教授",
            "schedule": "周三 10:00-12:00",
            "location": "教学楼A103",
            "credits": 3,
            "status": "active"
        },
        {
            "id": 4,
            "name": "数据库原理",
            "code": "CS104",
            "teacher": "赵教授",
            "schedule": "周四 16:00-18:00",
            "location": "教学楼A104",
            "credits": 4,
            "status": "active"
        }
    ]
    
    # 显示课程表格
    st.markdown("#### 📋 课程列表")
    
    selected_courses = render_course_table(courses_data)
    
    # 添加课程表单
    if st.session_state.get("show_add_course_form", False):
        with st.expander("➕ 添加新课程", expanded=True):
            with st.form("add_course_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_course_name = st.text_input("课程名称", key="new_course_name")
                    new_course_code = st.text_input("课程代码", key="new_course_code")
                    new_teacher = st.text_input("授课教师", key="new_teacher")
                
                with col2:
                    new_schedule = st.text_input("上课时间", key="new_schedule")
                    new_location = st.text_input("上课地点", key="new_location")
                    new_credits = st.number_input("学分", min_value=1, max_value=10, value=3, key="new_credits")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("✅ 确认添加", type="primary"):
                        if new_course_name and new_course_code and new_teacher:
                            st.success(f"课程 {new_course_name} 添加成功！")
                            st.session_state["show_add_course_form"] = False
                            st.rerun()
                        else:
                            st.error("请填写所有必填字段")
                
                with col2:
                    if st.form_submit_button("❌ 取消"):
                        st.session_state["show_add_course_form"] = False
                        st.rerun()

with tab3:
    st.markdown("### 📊 报表查询")
    
    # 查询条件
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_start_date = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=30),
            key="report_start_date"
        )
    
    with col2:
        report_end_date = st.date_input(
            "结束日期",
            value=datetime.now(),
            key="report_end_date"
        )
    
    with col3:
        report_type = st.selectbox(
            "报表类型",
            options=["考勤汇总", "出勤率统计", "异常情况", "用户活跃度"],
            key="report_type_select"
        )
    
    # 生成报表
    if st.button("📊 生成报表", type="primary"):
        with st.spinner("正在生成报表..."):
            st.session_state["report_generated"] = True
    
    if st.session_state.get("report_generated", False):
        # 报表统计
        st.markdown("#### 📈 报表统计")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总签到次数", "1,234", "+89")
        
        with col2:
            st.metric("平均出勤率", "87.5%", "+3.2%")
        
        with col3:
            st.metric("异常次数", "23", "-5")
        
        with col4:
            st.metric("活跃用户", "156", "+12")
        
        # 详细报表数据
        st.markdown("#### 📋 详细数据")
        
        # 模拟报表数据
        report_data = []
        for i in range(50):
            report_data.append({
                "date": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
                "total_users": 150 + (i % 10),
                "attended_users": 130 + (i % 8),
                "attendance_rate": round((130 + (i % 8)) / (150 + (i % 10)) * 100, 1),
                "late_count": i % 5,
                "absent_count": i % 3,
                "anomaly_count": i % 2
            })
        
        df_report = pd.DataFrame(report_data)
        
        # 使用streamlit-aggrid显示表格
        try:
            from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
            
            gb = GridOptionsBuilder.from_dataframe(df_report)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_side_bar()
            
            # 设置列属性
            gb.configure_column("date", header_name="日期", width=120)
            gb.configure_column("total_users", header_name="总用户数", width=120)
            gb.configure_column("attended_users", header_name="签到用户数", width=120)
            gb.configure_column("attendance_rate", header_name="出勤率(%)", width=120)
            gb.configure_column("late_count", header_name="迟到次数", width=120)
            gb.configure_column("absent_count", header_name="缺勤次数", width=120)
            gb.configure_column("anomaly_count", header_name="异常次数", width=120)
            
            gridOptions = gb.build()
            
            AgGrid(df_report, gridOptions=gridOptions, enable_enterprise_modules=True)
            
        except ImportError:
            # 如果streamlit-aggrid不可用，使用默认表格
            st.dataframe(df_report, use_container_width=True)
        
        # 导出报表
        st.markdown("#### 📥 导出报表")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 导出Excel", use_container_width=True):
                # 生成Excel文件
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_report.to_excel(writer, sheet_name='考勤报表', index=False)
                
                st.download_button(
                    label="下载Excel报表",
                    data=output.getvalue(),
                    file_name=f"attendance_report_{report_start_date}_{report_end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            if st.button("📄 导出CSV", use_container_width=True):
                csv_data = df_report.to_csv(index=False)
                st.download_button(
                    label="下载CSV报表",
                    data=csv_data,
                    file_name=f"attendance_report_{report_start_date}_{report_end_date}.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("📊 导出PDF", use_container_width=True):
                st.info("PDF导出功能开发中...")

with tab4:
    st.markdown("### 📈 数据分析")
    
    # 分析类型选择
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_type = st.selectbox(
            "分析类型",
            options=["出勤率趋势", "用户活跃度", "异常分析", "课程对比"],
            key="analysis_type_select"
        )
    
    with col2:
        if st.button("📊 生成分析", type="primary"):
            st.session_state["analysis_generated"] = True
    
    if st.session_state.get("analysis_generated", False):
        if analysis_type == "出勤率趋势":
            st.markdown("#### 📈 出勤率趋势分析")
            
            # 模拟趋势数据
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
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
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 趋势分析
            st.markdown("#### 📊 趋势分析")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("平均出勤率", "87.5%", "+3.2%")
            
            with col2:
                st.metric("最高出勤率", "95.2%", "2024-01-15")
            
            with col3:
                st.metric("最低出勤率", "78.3%", "2024-01-08")
        
        elif analysis_type == "用户活跃度":
            st.markdown("#### 👥 用户活跃度分析")
            
            # 用户活跃度数据
            user_activity = {
                "高活跃": 45,
                "中活跃": 78,
                "低活跃": 23,
                "不活跃": 10
            }
            
            fig = px.pie(
                values=list(user_activity.values()),
                names=list(user_activity.keys()),
                title="用户活跃度分布",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # 活跃度统计
            st.markdown("#### 📊 活跃度统计")
            
            col1, col2, col3, col4 = st.columns(4)
            
            for i, (level, count) in enumerate(user_activity.items()):
                with [col1, col2, col3, col4][i]:
                    st.metric(level, count)
        
        elif analysis_type == "异常分析":
            st.markdown("#### ⚠️ 异常情况分析")
            
            # 异常类型统计
            anomaly_types = {
                "迟到": 15,
                "早退": 5,
                "缺勤": 8,
                "系统故障": 3,
                "位置异常": 2
            }
            
            fig = px.bar(
                x=list(anomaly_types.keys()),
                y=list(anomaly_types.values()),
                title="异常情况统计",
                labels={'x': '异常类型', 'y': '次数'},
                color=list(anomaly_types.values()),
                color_continuous_scale='Reds'
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # 异常趋势
            st.markdown("#### 📈 异常趋势")
            
            anomaly_dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='D')
            anomaly_counts = [3, 5, 2, 4, 6, 3, 2]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=anomaly_dates,
                y=anomaly_counts,
                mode='lines+markers',
                name='异常次数',
                line=dict(color='#dc3545', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="异常情况趋势",
                xaxis_title="日期",
                yaxis_title="异常次数",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif analysis_type == "课程对比":
            st.markdown("#### 📚 课程对比分析")
            
            # 课程出勤率对比
            course_comparison = {
                "数据结构": 92.5,
                "操作系统": 88.3,
                "计算机网络": 85.7,
                "数据库原理": 90.1,
                "软件工程": 87.2,
                "人工智能": 89.8
            }
            
            fig = px.bar(
                x=list(course_comparison.keys()),
                y=list(course_comparison.values()),
                title="各课程出勤率对比",
                labels={'x': '课程', 'y': '出勤率 (%)'},
                color=list(course_comparison.values()),
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # 课程统计
            st.markdown("#### 📊 课程统计")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("最高出勤率", "92.5%", "数据结构")
            
            with col2:
                st.metric("平均出勤率", "88.9%", "+2.1%")
            
            with col3:
                st.metric("最低出勤率", "85.7%", "计算机网络")

with tab5:
    st.markdown("### ⚙️ 系统设置")
    
    # 系统配置
    st.markdown("#### 🔧 系统配置")
    
    with st.form("system_config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**签到设置**")
            sign_in_timeout = st.number_input("签到超时时间(分钟)", min_value=1, max_value=60, value=5)
            location_range = st.number_input("位置签到范围(米)", min_value=100, max_value=2000, value=1000)
            qr_code_expiry = st.number_input("二维码有效期(分钟)", min_value=1, max_value=30, value=5)
        
        with col2:
            st.markdown("**通知设置**")
            email_notifications = st.checkbox("启用邮件通知", value=True)
            sms_notifications = st.checkbox("启用短信通知", value=False)
            push_notifications = st.checkbox("启用推送通知", value=True)
        
        if st.form_submit_button("💾 保存配置", type="primary"):
            st.success("系统配置保存成功！")
    
    # 系统监控
    st.markdown("#### 📊 系统监控")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("系统状态", "正常", "99.9%")
    
    with col2:
        st.metric("在线用户", "156", "+12")
    
    with col3:
        st.metric("数据库连接", "正常", "100%")
    
    with col4:
        st.metric("Redis连接", "正常", "100%")
    
    # 系统日志
    st.markdown("#### 📜 系统日志")
    
    # 模拟系统日志
    log_data = [
        {"time": "2024-01-15 10:30:00", "level": "INFO", "message": "用户登录成功", "user": "student001"},
        {"time": "2024-01-15 10:25:00", "level": "WARN", "message": "二维码过期", "user": "student002"},
        {"time": "2024-01-15 10:20:00", "level": "ERROR", "message": "位置签到失败", "user": "student003"},
        {"time": "2024-01-15 10:15:00", "level": "INFO", "message": "用户登出", "user": "teacher001"},
        {"time": "2024-01-15 10:10:00", "level": "INFO", "message": "系统启动", "user": "system"}
    ]
    
    df_logs = pd.DataFrame(log_data)
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(df_logs)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        
        # 设置列属性
        gb.configure_column("time", header_name="时间", width=150)
        gb.configure_column("level", header_name="级别", width=100)
        gb.configure_column("message", header_name="消息", width=200)
        gb.configure_column("user", header_name="用户", width=120)
        
        # 设置级别列的颜色
        def level_cell_renderer(params):
            level = params.value
            color_map = {
                "INFO": "#17a2b8",
                "WARN": "#ffc107",
                "ERROR": "#dc3545",
                "DEBUG": "#6c757d"
            }
            color = color_map.get(level, "#6c757d")
            return f'<span style="color: {color}; font-weight: bold;">{level}</span>'
        
        gb.configure_column("level", cellRenderer=level_cell_renderer)
        
        gridOptions = gb.build()
        
        AgGrid(df_logs, gridOptions=gridOptions, enable_enterprise_modules=True)
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(df_logs, use_container_width=True)
    
    # 系统维护
    st.markdown("#### 🔧 系统维护")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 重启系统", use_container_width=True):
            st.warning("系统重启功能开发中...")
    
    with col2:
        if st.button("🗑️ 清理缓存", use_container_width=True):
            st.success("缓存清理完成！")
    
    with col3:
        if st.button("📊 备份数据", use_container_width=True):
            st.info("数据备份功能开发中...")

# 侧边栏信息
with st.sidebar:
    st.markdown("### 👨‍💼 管理员信息")
    st.write(f"**姓名：** {user_info.get('name', '未知')}")
    st.write(f"**工号：** {user_info.get('admin_id', '未知')}")
    st.write(f"**权限：** {user_info.get('role', '未知')}")
    
    st.markdown("### 📊 系统概览")
    st.metric("总用户数", "1,256", "+23")
    st.metric("今日签到", "1,234", "+89")
    st.metric("系统状态", "正常", "99.9%")
    st.metric("异常预警", "3", "-1")
    
    st.markdown("### 🔧 操作")
    if st.button("🚪 退出登录", use_container_width=True):
        auth_manager.logout()
        st.rerun()
