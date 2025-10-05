"""
学生端功能页面
包含：二维码签到、位置签到、考勤记录查询、异常反馈
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
import streamlit.components.v1 as components  # pyright: ignore[reportMissingImports]
import qrcode  # pyright: ignore[reportMissingImports, reportMissingModuleSource]
import io
import base64
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go  # pyright: ignore[reportMissingImports]
from streamlit_extras.colored_header import colored_header  # pyright: ignore[reportMissingImports]
from streamlit_extras.metric_cards import style_metric_cards  # pyright: ignore[reportMissingImports]

from utils.auth import AuthManager
from utils.api_client import APIClient
from utils.qr_code import QRCodeGenerator
from utils.geolocation import LocationManager

# 页面配置
st.set_page_config(
    page_title="学生端 - 课堂考勤签到系统",
    page_icon="👨‍🎓",
    layout="wide"
)

# 初始化组件
@st.cache_resource
def init_components():
    auth_manager = AuthManager()
    api_client = APIClient()
    qr_generator = QRCodeGenerator()
    location_manager = LocationManager()
    return auth_manager, api_client, qr_generator, location_manager

auth_manager, api_client, qr_generator, location_manager = init_components()

# 检查登录状态
if not auth_manager.is_logged_in():
    st.warning("请先登录")
    st.stop()

user_info = auth_manager.get_user_info()
user_id = auth_manager.get_user_id()

# 页面标题
colored_header(
    label=f"👨‍🎓 学生端 - 欢迎，{user_info.get('name', '学生')}",
    description="课堂考勤签到系统",
    color_name="blue-70"
)

# 创建选项卡
tab1, tab2, tab3, tab4 = st.tabs(["📱 二维码签到", "📍 位置签到", "📊 考勤记录", "📝 异常反馈"])

with tab1:
    st.markdown("### 📱 二维码签到")
    
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
            key="qr_course_select"
        )
        course_id = course_options[selected_course]
    
    with col2:
        if st.button("🔄 生成二维码", type="primary", use_container_width=True):
            # 生成二维码
            qr_data = {
                "course_id": course_id,
                "student_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "type": "attendance"
            }
            
            qr_image = qr_generator.generate_qr_code(qr_data)
            
            if qr_image:
                st.session_state["qr_code_generated"] = True
                st.session_state["qr_code_data"] = qr_data
                st.session_state["qr_code_image"] = qr_image
                st.success("二维码生成成功！")
    
    # 显示二维码
    if st.session_state.get("qr_code_generated", False):
        st.markdown("### 📱 签到二维码")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 显示二维码图片
            qr_image = st.session_state.get("qr_code_image")
            if qr_image:
                st.image(qr_image, caption="扫描此二维码进行签到", use_column_width=True)
        
        with col2:
            st.markdown("#### 📋 签到信息")
            qr_data = st.session_state.get("qr_code_data", {})
            
            st.info(f"""
            **课程：** {selected_course}
            
            **学生ID：** {user_id}
            
            **生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            **有效期：** 5分钟
            """)
            
            # 下载二维码
            if st.button("📥 下载二维码"):
                qr_bytes = qr_generator.get_qr_bytes(qr_data)
                st.download_button(
                    label="下载二维码图片",
                    data=qr_bytes,
                    file_name=f"attendance_qr_{course_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )
    
    # 二维码扫描签到
    st.markdown("### 📷 扫描签到")
    
    uploaded_file = st.file_uploader(
        "上传二维码图片进行签到",
        type=['png', 'jpg', 'jpeg'],
        help="请上传包含二维码的图片文件"
    )
    
    if uploaded_file is not None:
        # 这里可以实现二维码识别逻辑
        st.image(uploaded_file, caption="上传的二维码图片", use_column_width=True)
        
        if st.button("🔍 识别并签到", type="primary"):
            # 模拟二维码识别和签到
            with st.spinner("正在识别二维码..."):
                # 这里应该调用实际的二维码识别API
                st.success("二维码识别成功！签到完成。")
                
                # 记录签到信息
                attendance_record = {
                    "course": selected_course,
                    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "method": "二维码",
                    "status": "正常"
                }
                
                if "attendance_records" not in st.session_state:
                    st.session_state["attendance_records"] = []
                
                st.session_state["attendance_records"].append(attendance_record)

with tab2:
    st.markdown("### 📍 位置签到")
    
    # 课程选择
    course_options = {
        "数据结构": {"id": 1, "location": {"lat": 39.9042, "lng": 116.4074}},
        "操作系统": {"id": 2, "location": {"lat": 39.9042, "lng": 116.4074}},
        "计算机网络": {"id": 3, "location": {"lat": 39.9042, "lng": 116.4074}},
        "数据库原理": {"id": 4, "location": {"lat": 39.9042, "lng": 116.4074}}
    }
    
    selected_course = st.selectbox(
        "选择课程",
        options=list(course_options.keys()),
        key="location_course_select"
    )
    
    course_info = course_options[selected_course]
    course_id = course_info["id"]
    classroom_location = course_info["location"]
    
    # 显示教室位置信息
    st.info(f"""
    **课程：** {selected_course}
    
    **教室位置：** 纬度 {classroom_location['lat']}, 经度 {classroom_location['lng']}
    
    **签到范围：** 1公里以内
    """)
    
    # 获取当前位置
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("📍 获取当前位置", type="primary", use_container_width=True):
            # 获取用户位置
            current_location = location_manager.get_current_location()
            
            if current_location:
                st.session_state["current_location"] = current_location
                st.success("位置获取成功！")
            else:
                st.error("无法获取当前位置，请检查浏览器权限设置")
    
    with col2:
        if st.button("🗺️ 显示地图", use_container_width=True):
            st.session_state["show_map"] = True
    
    # 显示当前位置
    if "current_location" in st.session_state:
        current_location = st.session_state["current_location"]
        
        st.markdown("#### 📍 当前位置信息")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("纬度", f"{current_location['lat']:.6f}")
        
        with col2:
            st.metric("经度", f"{current_location['lng']:.6f}")
        
        with col3:
            distance = location_manager.calculate_distance(
                current_location['lat'], current_location['lng'],
                classroom_location['lat'], classroom_location['lng']
            )
            st.metric("距离教室", f"{distance:.0f}米")
        
        # 距离检查
        if distance <= 1000:
            st.success("✅ 您在签到范围内，可以进行位置签到")
            
            if st.button("✅ 确认位置签到", type="primary", use_container_width=True):
                # 执行位置签到
                with st.spinner("正在处理签到..."):
                    # 这里应该调用API进行位置签到
                    st.success("位置签到成功！")
                    
                    # 记录签到信息
                    attendance_record = {
                        "course": selected_course,
                        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "method": "位置",
                        "status": "正常",
                        "distance": f"{distance:.0f}米"
                    }
                    
                    if "attendance_records" not in st.session_state:
                        st.session_state["attendance_records"] = []
                    
                    st.session_state["attendance_records"].append(attendance_record)
        else:
            st.error(f"❌ 您距离教室 {distance:.0f}米，超出签到范围（1公里）")
    
    # 显示地图
    if st.session_state.get("show_map", False):
        st.markdown("#### 🗺️ 位置地图")
        
        # 创建地图
        map_data = location_manager.create_map(
            classroom_location['lat'], classroom_location['lng'],
            st.session_state.get("current_location", {}).get('lat'),
            st.session_state.get("current_location", {}).get('lng')
        )
        
        components.html(map_data, height=400)

with tab3:
    st.markdown("### 📊 考勤记录查询")
    
    # 查询条件
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start_date = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=30),
            key="attendance_start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "结束日期",
            value=datetime.now(),
            key="attendance_end_date"
        )
    
    with col3:
        course_filter = st.selectbox(
            "课程筛选",
            options=["全部"] + list(course_options.keys()),
            key="attendance_course_filter"
        )
    
    # 查询按钮
    if st.button("🔍 查询考勤记录", type="primary"):
        # 模拟查询考勤记录
        with st.spinner("正在查询考勤记录..."):
            # 这里应该调用API查询考勤记录
            attendance_data = [
                {
                    "date": "2024-01-15",
                    "course": "数据结构",
                    "time": "09:00:00",
                    "method": "二维码",
                    "status": "正常"
                },
                {
                    "date": "2024-01-14",
                    "course": "操作系统",
                    "time": "14:05:00",
                    "method": "位置",
                    "status": "迟到"
                },
                {
                    "date": "2024-01-13",
                    "course": "计算机网络",
                    "time": "10:30:00",
                    "method": "二维码",
                    "status": "正常"
                },
                {
                    "date": "2024-01-12",
                    "course": "数据库原理",
                    "time": "16:00:00",
                    "method": "位置",
                    "status": "正常"
                }
            ]
            
            st.session_state["attendance_data"] = attendance_data
    
    # 显示考勤记录
    if "attendance_data" in st.session_state:
        attendance_data = st.session_state["attendance_data"]
        
        # 统计信息
        st.markdown("#### 📈 考勤统计")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_records = len(attendance_data)
        normal_count = len([r for r in attendance_data if r["status"] == "正常"])
        late_count = len([r for r in attendance_data if r["status"] == "迟到"])
        absent_count = len([r for r in attendance_data if r["status"] == "缺勤"])
        
        with col1:
            st.metric("总记录数", total_records)
        
        with col2:
            st.metric("正常签到", normal_count)
        
        with col3:
            st.metric("迟到次数", late_count)
        
        with col4:
            attendance_rate = (normal_count / total_records * 100) if total_records > 0 else 0
            st.metric("出勤率", f"{attendance_rate:.1f}%")
        
        # 考勤记录表格
        st.markdown("#### 📋 详细记录")
        
        df = pd.DataFrame(attendance_data)
        
        # 使用streamlit-aggrid显示表格
        try:
            from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
            
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_side_bar()
            gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
            gridOptions = gb.build()
            
            AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
        except ImportError:
            # 如果streamlit-aggrid不可用，使用默认表格
            st.dataframe(df, use_container_width=True)
        
        # 出勤率趋势图
        st.markdown("#### 📊 出勤率趋势")
        
        # 按日期统计出勤率
        df['date'] = pd.to_datetime(df['date'])
        daily_stats = df.groupby('date').agg({
            'status': lambda x: (x == '正常').sum() / len(x) * 100
        }).reset_index()
        daily_stats.columns = ['date', 'attendance_rate']
        
        fig = px.line(
            daily_stats, 
            x='date', 
            y='attendance_rate',
            title='每日出勤率趋势',
            labels={'attendance_rate': '出勤率 (%)', 'date': '日期'}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### 📝 异常反馈")
    
    # 选择要反馈的考勤记录
    if "attendance_data" in st.session_state:
        attendance_data = st.session_state["attendance_data"]
        
        st.markdown("#### 📋 选择考勤记录")
        
        # 创建选择框
        record_options = []
        for i, record in enumerate(attendance_data):
            option_text = f"{record['date']} - {record['course']} - {record['status']}"
            record_options.append((option_text, i))
        
        selected_record_idx = st.selectbox(
            "选择要反馈的考勤记录",
            options=[i for _, i in record_options],
            format_func=lambda x: record_options[x][0],
            key="feedback_record_select"
        )
        
        selected_record = attendance_data[selected_record_idx]
        
        # 显示选中的记录
        st.info(f"""
        **选中的记录：**
        
        - 日期：{selected_record['date']}
        - 课程：{selected_record['course']}
        - 时间：{selected_record['time']}
        - 状态：{selected_record['status']}
        - 签到方式：{selected_record['method']}
        """)
        
        # 反馈表单
        st.markdown("#### 📝 反馈内容")
        
        feedback_type = st.selectbox(
            "反馈类型",
            options=["签到异常", "时间错误", "位置错误", "其他问题"],
            key="feedback_type"
        )
        
        feedback_content = st.text_area(
            "详细描述问题",
            placeholder="请详细描述您遇到的问题...",
            height=100,
            key="feedback_content"
        )
        
        # 上传相关文件（可选）
        uploaded_files = st.file_uploader(
            "上传相关文件（可选）",
            type=['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'],
            accept_multiple_files=True,
            help="可以上传截图、文档等作为证据"
        )
        
        if uploaded_files:
            st.info(f"已上传 {len(uploaded_files)} 个文件")
        
        # 提交反馈
        if st.button("📤 提交反馈", type="primary"):
            if feedback_content.strip():
                # 提交反馈
                with st.spinner("正在提交反馈..."):
                    # 这里应该调用API提交反馈
                    st.success("反馈提交成功！我们会尽快处理您的问题。")
                    
                    # 记录反馈
                    feedback_record = {
                        "record_id": selected_record_idx,
                        "type": feedback_type,
                        "content": feedback_content,
                        "files": len(uploaded_files) if uploaded_files else 0,
                        "submit_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "status": "待处理"
                    }
                    
                    if "feedback_records" not in st.session_state:
                        st.session_state["feedback_records"] = []
                    
                    st.session_state["feedback_records"].append(feedback_record)
            else:
                st.error("请填写反馈内容")
    
    else:
        st.warning("请先查询考勤记录")
    
    # 显示历史反馈
    if "feedback_records" in st.session_state and st.session_state["feedback_records"]:
        st.markdown("#### 📜 历史反馈")
        
        feedback_df = pd.DataFrame(st.session_state["feedback_records"])
        
        # 状态颜色映射
        status_colors = {
            "待处理": "orange",
            "已处理": "green",
            "已关闭": "gray"
        }
        
        for _, feedback in feedback_df.iterrows():
            with st.expander(f"反馈 #{feedback.name + 1} - {feedback['type']} ({feedback['status']})"):
                st.write(f"**提交时间：** {feedback['submit_time']}")
                st.write(f"**反馈类型：** {feedback['type']}")
                st.write(f"**反馈内容：** {feedback['content']}")
                st.write(f"**附件数量：** {feedback['files']}")
                st.write(f"**处理状态：** {feedback['status']}")

# 侧边栏信息
with st.sidebar:
    st.markdown("### 👤 用户信息")
    st.write(f"**姓名：** {user_info.get('name', '未知')}")
    st.write(f"**学号：** {user_info.get('student_id', '未知')}")
    st.write(f"**班级：** {user_info.get('class', '未知')}")
    
    st.markdown("### 📊 今日统计")
    st.metric("今日签到", "3", "100%")
    st.metric("本月出勤", "28", "93.3%")
    
    st.markdown("### 🔧 操作")
    if st.button("🚪 退出登录", use_container_width=True):
        auth_manager.logout()
        st.rerun()
