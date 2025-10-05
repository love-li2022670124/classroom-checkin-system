"""
图表组件模块
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

def create_attendance_rate_chart(data: List[Dict[str, Any]], chart_type: str = "line") -> go.Figure:
    """创建出勤率图表"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    if chart_type == "line":
        fig = px.line(
            df, 
            x='date', 
            y='attendance_rate',
            title='出勤率趋势图',
            labels={'attendance_rate': '出勤率 (%)', 'date': '日期'}
        )
        
        # 添加平均线
        avg_rate = df['attendance_rate'].mean()
        fig.add_hline(
            y=avg_rate, 
            line_dash="dash", 
            line_color="red", 
            annotation_text=f"平均出勤率 ({avg_rate:.1f}%)"
        )
        
    elif chart_type == "bar":
        fig = px.bar(
            df,
            x='date',
            y='attendance_rate',
            title='出勤率柱状图',
            labels={'attendance_rate': '出勤率 (%)', 'date': '日期'}
        )
    
    elif chart_type == "pie":
        # 计算出勤率分布
        rate_ranges = {
            '90-100%': len(df[df['attendance_rate'] >= 90]),
            '80-89%': len(df[(df['attendance_rate'] >= 80) & (df['attendance_rate'] < 90)]),
            '70-79%': len(df[(df['attendance_rate'] >= 70) & (df['attendance_rate'] < 80)]),
            '<70%': len(df[df['attendance_rate'] < 70])
        }
        
        fig = px.pie(
            values=list(rate_ranges.values()),
            names=list(rate_ranges.keys()),
            title='出勤率分布'
        )
    
    fig.update_layout(height=400)
    return fig

def create_attendance_pie_chart(attended: int, absent: int, late: int = 0) -> go.Figure:
    """创建出勤饼图"""
    labels = ['正常签到', '迟到', '缺勤']
    values = [attended, late, absent]
    colors = ['#28a745', '#ffc107', '#dc3545']
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker_colors=colors,
        textinfo='label+percent',
        textfont_size=14
    ))
    
    # 计算总出勤率
    total = attended + late + absent
    attendance_rate = (attended + late) / total * 100 if total > 0 else 0
    
    fig.update_layout(
        title=f"出勤率分布 - {attendance_rate:.1f}%",
        showlegend=True,
        height=400,
        annotations=[dict(text=f'{attendance_rate:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    return fig

def create_user_activity_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """创建用户活跃度图表"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # 按日期分组统计活跃用户数
    daily_activity = df.groupby('date').size().reset_index(name='active_users')
    
    fig = px.line(
        daily_activity,
        x='date',
        y='active_users',
        title='用户活跃度趋势',
        labels={'active_users': '活跃用户数', 'date': '日期'}
    )
    
    fig.update_layout(height=400)
    return fig

def create_course_comparison_chart(course_data: Dict[str, float]) -> go.Figure:
    """创建课程对比图表"""
    if not course_data:
        return go.Figure()
    
    courses = list(course_data.keys())
    rates = list(course_data.values())
    
    fig = px.bar(
        x=courses,
        y=rates,
        title='各课程出勤率对比',
        labels={'x': '课程', 'y': '出勤率 (%)'},
        color=rates,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=400)
    return fig

def create_anomaly_analysis_chart(anomaly_data: Dict[str, int]) -> go.Figure:
    """创建异常分析图表"""
    if not anomaly_data:
        return go.Figure()
    
    anomaly_types = list(anomaly_data.keys())
    counts = list(anomaly_data.values())
    
    fig = px.bar(
        x=anomaly_types,
        y=counts,
        title='异常情况统计',
        labels={'x': '异常类型', 'y': '次数'},
        color=counts,
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=400)
    return fig

def create_time_series_chart(data: List[Dict[str, Any]], 
                           x_col: str, 
                           y_col: str, 
                           title: str,
                           color_col: Optional[str] = None) -> go.Figure:
    """创建时间序列图表"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    if color_col and color_col in df.columns:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title
        )
    else:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=title
        )
    
    fig.update_layout(height=400)
    return fig

def create_heatmap_chart(data: List[Dict[str, Any]], 
                        x_col: str, 
                        y_col: str, 
                        value_col: str,
                        title: str) -> go.Figure:
    """创建热力图"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # 创建数据透视表
    pivot_table = df.pivot_table(
        values=value_col,
        index=y_col,
        columns=x_col,
        aggfunc='mean',
        fill_value=0
    )
    
    fig = px.imshow(
        pivot_table,
        title=title,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=400)
    return fig

def create_dashboard_metrics(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """创建仪表板指标"""
    if not data:
        return []
    
    df = pd.DataFrame(data)
    
    metrics = []
    
    # 总签到次数
    total_sign_ins = len(df)
    metrics.append({
        "label": "总签到次数",
        "value": total_sign_ins,
        "delta": "+12"
    })
    
    # 平均出勤率
    if 'attendance_rate' in df.columns:
        avg_rate = df['attendance_rate'].mean()
        metrics.append({
            "label": "平均出勤率",
            "value": f"{avg_rate:.1f}%",
            "delta": "+3.2%"
        })
    
    # 异常次数
    if 'status' in df.columns:
        anomaly_count = len(df[df['status'].isin(['迟到', '缺勤', '早退'])])
        metrics.append({
            "label": "异常次数",
            "value": anomaly_count,
            "delta": "-5"
        })
    
    # 活跃用户
    if 'user_id' in df.columns:
        active_users = df['user_id'].nunique()
        metrics.append({
            "label": "活跃用户",
            "value": active_users,
            "delta": "+8"
        })
    
    return metrics

def create_trend_analysis(data: List[Dict[str, Any]], 
                         date_col: str, 
                         value_col: str,
                         title: str) -> go.Figure:
    """创建趋势分析图表"""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    df[date_col] = pd.to_datetime(df[date_col])
    
    # 按日期分组计算平均值
    daily_avg = df.groupby(df[date_col].dt.date)[value_col].mean().reset_index()
    
    fig = go.Figure()
    
    # 添加趋势线
    fig.add_trace(go.Scatter(
        x=daily_avg[date_col],
        y=daily_avg[value_col],
        mode='lines+markers',
        name='趋势',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    # 添加移动平均线
    if len(daily_avg) > 7:
        daily_avg['moving_avg'] = daily_avg[value_col].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=daily_avg[date_col],
            y=daily_avg['moving_avg'],
            mode='lines',
            name='7日移动平均',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="日期",
        yaxis_title=value_col,
        height=400
    )
    
    return fig

def create_comparison_chart(data1: List[Dict[str, Any]], 
                          data2: List[Dict[str, Any]],
                          x_col: str,
                          y_col: str,
                          title: str,
                          label1: str = "数据1",
                          label2: str = "数据2") -> go.Figure:
    """创建对比图表"""
    fig = go.Figure()
    
    if data1:
        df1 = pd.DataFrame(data1)
        fig.add_trace(go.Scatter(
            x=df1[x_col],
            y=df1[y_col],
            mode='lines+markers',
            name=label1,
            line=dict(color='#1f77b4', width=3)
        ))
    
    if data2:
        df2 = pd.DataFrame(data2)
        fig.add_trace(go.Scatter(
            x=df2[x_col],
            y=df2[y_col],
            mode='lines+markers',
            name=label2,
            line=dict(color='#ff7f0e', width=3)
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=400
    )
    
    return fig

def create_gauge_chart(value: float, 
                      max_value: float, 
                      title: str,
                      color: str = "blue") -> go.Figure:
    """创建仪表盘图表"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': max_value * 0.8},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value * 0.5], 'color': "lightgray"},
                {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def render_chart_with_controls(fig: go.Figure, chart_title: str = ""):
    """渲染带控件的图表"""
    if chart_title:
        st.markdown(f"#### {chart_title}")
    
    # 图表显示选项
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_legend = st.checkbox("显示图例", value=True)
    
    with col2:
        show_grid = st.checkbox("显示网格", value=True)
    
    with col3:
        chart_height = st.slider("图表高度", min_value=300, max_value=800, value=400)
    
    # 更新图表设置
    fig.update_layout(
        showlegend=show_legend,
        height=chart_height
    )
    
    if show_grid:
        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 图表操作
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 全屏查看"):
            st.plotly_chart(fig, use_container_width=True, height=600)
    
    with col2:
        if st.button("📥 下载图片"):
            st.info("图片下载功能开发中...")
    
    with col3:
        if st.button("🔄 刷新数据"):
            st.rerun()
