"""
表格组件模块
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
import pandas as pd
from typing import List, Dict, Any, Optional
import plotly.express as px  # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go  # pyright: ignore[reportMissingImports]

def render_data_table(data: List[Dict[str, Any]], 
                     columns: Optional[List[str]] = None,
                     editable: bool = False,
                     selectable: bool = False) -> pd.DataFrame:
    """渲染数据表格"""
    if not data:
        st.warning("暂无数据")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    
    if columns:
        df = df[columns]
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        
        if selectable:
            gb.configure_selection('multiple', use_checkbox=True)
        
        if editable:
            gb.configure_default_column(editable=True)
        
        gridOptions = gb.build()
        
        selected_rows = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
        
        return selected_rows['data'] if selectable else df
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        if editable:
            edited_df = st.data_editor(df, use_container_width=True)
            return edited_df
        else:
            st.dataframe(df, use_container_width=True)
            return df

def render_user_table(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """渲染用户表格"""
    if not users:
        st.warning("暂无用户数据")
        return []
    
    df = pd.DataFrame(users)
    
    # 设置列名
    column_mapping = {
        'id': 'ID',
        'username': '用户名',
        'name': '姓名',
        'email': '邮箱',
        'role': '角色',
        'status': '状态',
        'created_at': '创建时间',
        'last_login': '最后登录'
    }
    
    df = df.rename(columns=column_mapping)
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_selection('multiple', use_checkbox=True)
        
        # 设置列属性
        gb.configure_column("ID", width=80)
        gb.configure_column("用户名", width=120)
        gb.configure_column("姓名", width=120)
        gb.configure_column("邮箱", width=200)
        gb.configure_column("角色", width=100)
        gb.configure_column("状态", width=100)
        gb.configure_column("创建时间", width=150)
        gb.configure_column("最后登录", width=150)
        
        # 设置状态列的颜色
        def status_cell_renderer(params):
            status = params.value
            color_map = {
                "active": "#28a745",
                "inactive": "#dc3545",
                "pending": "#ffc107",
                "banned": "#6c757d"
            }
            color = color_map.get(status, "#6c757d")
            return f'<span style="color: {color}; font-weight: bold;">{status}</span>'
        
        gb.configure_column("状态", cellRenderer=status_cell_renderer)
        
        gridOptions = gb.build()
        
        selected_rows = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
        
        return selected_rows['data']
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(df, use_container_width=True)
        return []

def render_attendance_summary_table(attendance_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """渲染考勤汇总表格"""
    if not attendance_data:
        st.warning("暂无考勤数据")
        return pd.DataFrame()
    
    df = pd.DataFrame(attendance_data)
    
    # 按学生分组统计
    summary = df.groupby(['student_id', 'student_name']).agg({
        'attendance_date': 'count',
        'status': lambda x: (x == '正常').sum(),
        'late_count': lambda x: (x == '迟到').sum(),
        'absent_count': lambda x: (x == '缺勤').sum()
    }).reset_index()
    
    summary.columns = ['学生ID', '学生姓名', '总次数', '正常次数', '迟到次数', '缺勤次数']
    summary['出勤率'] = (summary['正常次数'] / summary['总次数'] * 100).round(1)
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(summary)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        
        # 设置列属性
        gb.configure_column("学生ID", width=100)
        gb.configure_column("学生姓名", width=120)
        gb.configure_column("总次数", width=100)
        gb.configure_column("正常次数", width=100)
        gb.configure_column("迟到次数", width=100)
        gb.configure_column("缺勤次数", width=100)
        gb.configure_column("出勤率", width=100)
        
        # 设置出勤率列的颜色
        def attendance_rate_cell_renderer(params):
            rate = params.value
            if rate >= 90:
                color = "#28a745"
            elif rate >= 80:
                color = "#ffc107"
            else:
                color = "#dc3545"
            return f'<span style="color: {color}; font-weight: bold;">{rate}%</span>'
        
        gb.configure_column("出勤率", cellRenderer=attendance_rate_cell_renderer)
        
        gridOptions = gb.build()
        
        AgGrid(summary, gridOptions=gridOptions, enable_enterprise_modules=True)
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(summary, use_container_width=True)
    
    return summary

def render_course_table(courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """渲染课程表格"""
    if not courses:
        st.warning("暂无课程数据")
        return []
    
    df = pd.DataFrame(courses)
    
    # 设置列名
    column_mapping = {
        'id': 'ID',
        'name': '课程名称',
        'code': '课程代码',
        'teacher': '授课教师',
        'schedule': '上课时间',
        'location': '上课地点',
        'credits': '学分',
        'status': '状态'
    }
    
    df = df.rename(columns=column_mapping)
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_selection('multiple', use_checkbox=True)
        
        # 设置列属性
        gb.configure_column("ID", width=80)
        gb.configure_column("课程名称", width=150)
        gb.configure_column("课程代码", width=120)
        gb.configure_column("授课教师", width=120)
        gb.configure_column("上课时间", width=150)
        gb.configure_column("上课地点", width=120)
        gb.configure_column("学分", width=80)
        gb.configure_column("状态", width=100)
        
        # 设置状态列的颜色
        def status_cell_renderer(params):
            status = params.value
            color_map = {
                "active": "#28a745",
                "inactive": "#dc3545",
                "pending": "#ffc107"
            }
            color = color_map.get(status, "#6c757d")
            return f'<span style="color: {color}; font-weight: bold;">{status}</span>'
        
        gb.configure_column("状态", cellRenderer=status_cell_renderer)
        
        gridOptions = gb.build()
        
        selected_rows = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
        
        return selected_rows['data']
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(df, use_container_width=True)
        return []

def render_feedback_table(feedback_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """渲染反馈表格"""
    if not feedback_data:
        st.warning("暂无反馈数据")
        return []
    
    df = pd.DataFrame(feedback_data)
    
    # 设置列名
    column_mapping = {
        'id': 'ID',
        'student_name': '学生姓名',
        'course_name': '课程名称',
        'feedback_type': '反馈类型',
        'content': '反馈内容',
        'priority': '优先级',
        'status': '状态',
        'submit_time': '提交时间',
        'handle_time': '处理时间'
    }
    
    df = df.rename(columns=column_mapping)
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_selection('multiple', use_checkbox=True)
        
        # 设置列属性
        gb.configure_column("ID", width=80)
        gb.configure_column("学生姓名", width=120)
        gb.configure_column("课程名称", width=150)
        gb.configure_column("反馈类型", width=120)
        gb.configure_column("反馈内容", width=200)
        gb.configure_column("优先级", width=100)
        gb.configure_column("状态", width=100)
        gb.configure_column("提交时间", width=150)
        gb.configure_column("处理时间", width=150)
        
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
        
        gb.configure_column("优先级", cellRenderer=priority_cell_renderer)
        
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
        
        gb.configure_column("状态", cellRenderer=status_cell_renderer)
        
        gridOptions = gb.build()
        
        selected_rows = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
        
        return selected_rows['data']
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(df, use_container_width=True)
        return []

def render_statistics_table(stats_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """渲染统计表格"""
    if not stats_data:
        st.warning("暂无统计数据")
        return pd.DataFrame()
    
    df = pd.DataFrame(stats_data)
    
    # 使用streamlit-aggrid显示表格
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder  # pyright: ignore[reportMissingImports]
        
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        
        gridOptions = gb.build()
        
        AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
        
    except ImportError:
        # 如果streamlit-aggrid不可用，使用默认表格
        st.dataframe(df, use_container_width=True)
    
    return df
