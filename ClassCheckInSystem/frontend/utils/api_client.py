"""
API客户端 - 用于与Flask后端通信
"""

import requests
import json
import streamlit as st  # pyright: ignore[reportMissingImports]
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class APIClient:
    """Flask后端API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        # 从环境变量或Streamlit secrets获取API地址
        try:
            import os
            self.base_url = os.getenv('BACKEND_API_URL', base_url).rstrip('/')
        except:
            self.base_url = base_url.rstrip('/')
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # 检查是否为离线模式 - 强制启用离线模式用于演示
        self.offline_mode = True  # 强制启用离线模式
    
    def set_auth_token(self, token: str):
        """设置认证令牌"""
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """用户登录"""
        # 添加调试信息
        st.write(f"🔍 调试信息:")
        st.write(f"- API地址: {self.base_url}")
        st.write(f"- 离线模式: {self.offline_mode}")
        st.write(f"- 用户名: {username}")
        st.write(f"- 密码长度: {len(password)}")
        
        # 离线模式 - 使用模拟数据
        if self.offline_mode:
            # 模拟用户数据
            mock_users = {
                "admin": {"password": "admin123", "role": "admin", "name": "管理员", "id": 1},
                "teacher": {"password": "teacher123", "role": "teacher", "name": "张老师", "id": 2},
                "student": {"password": "student123", "role": "student", "name": "李同学", "id": 3}
            }
            
            st.write(f"📋 可用用户: {list(mock_users.keys())}")
            
            if username in mock_users and mock_users[username]["password"] == password:
                user_data = mock_users[username]
                st.success("✅ 离线登录成功！")
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
            else:
                st.error("❌ 用户名或密码错误")
                return {"error": "用户名或密码错误"}
        
        # 在线模式 - 调用真实API
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"登录失败: {str(e)}")
            return {"error": str(e)}
    
    def get_user_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        try:
            response = self.session.get(f"{self.base_url}/api/auth/user")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"获取用户信息失败: {str(e)}")
            return {"error": str(e)}
    
    # 学生端API
    def generate_qr_code(self, course_id: int) -> Dict[str, Any]:
        """生成签到二维码"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/student/sign/qrcode/generate",
                json={"course_id": course_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"生成二维码失败: {str(e)}")
            return {"error": str(e)}
    
    def qr_sign_in(self, qr_token: str, course_id: int) -> Dict[str, Any]:
        """二维码签到"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/student/sign/qrcode",
                json={"qr_token": qr_token, "course_id": course_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"二维码签到失败: {str(e)}")
            return {"error": str(e)}
    
    def location_sign_in(self, course_id: int, latitude: float, longitude: float) -> Dict[str, Any]:
        """位置签到"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/student/sign/location",
                json={
                    "course_id": course_id,
                    "latitude": latitude,
                    "longitude": longitude
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"位置签到失败: {str(e)}")
            return {"error": str(e)}
    
    def get_student_attendance(self, student_id: int, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """获取学生考勤记录"""
        try:
            params = {"student_id": student_id}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            
            response = self.session.get(
                f"{self.base_url}/api/student/attendance",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"获取考勤记录失败: {str(e)}")
            return {"error": str(e)}
    
    def submit_feedback(self, attendance_id: int, feedback_content: str) -> Dict[str, Any]:
        """提交考勤异常反馈"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/student/feedback",
                json={
                    "attendance_id": attendance_id,
                    "feedback_content": feedback_content
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"提交反馈失败: {str(e)}")
            return {"error": str(e)}
    
    # 教师端API
    def get_attendance_rate(self, course_id: int) -> Dict[str, Any]:
        """获取课程出勤率"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/teacher/attendance/rate",
                params={"course_id": course_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"获取出勤率失败: {str(e)}")
            return {"error": str(e)}
    
    def manual_makeup(self, student_id: int, course_id: int, reason: str) -> Dict[str, Any]:
        """手动补签"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/teacher/makeup",
                json={
                    "student_id": student_id,
                    "course_id": course_id,
                    "reason": reason
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"手动补签失败: {str(e)}")
            return {"error": str(e)}
    
    def get_pending_feedback(self) -> Dict[str, Any]:
        """获取待处理反馈"""
        try:
            response = self.session.get(f"{self.base_url}/api/teacher/feedback/pending")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"获取待处理反馈失败: {str(e)}")
            return {"error": str(e)}
    
    def handle_feedback(self, feedback_id: int, action: str, response_content: str = None) -> Dict[str, Any]:
        """处理反馈"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/teacher/feedback/handle",
                json={
                    "feedback_id": feedback_id,
                    "action": action,
                    "response_content": response_content
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"处理反馈失败: {str(e)}")
            return {"error": str(e)}
    
    # 管理员端API
    def get_users(self, user_type: str = None, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """获取用户列表"""
        try:
            params = {"page": page, "per_page": per_page}
            if user_type:
                params["user_type"] = user_type
            
            response = self.session.get(
                f"{self.base_url}/api/admin/users",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"获取用户列表失败: {str(e)}")
            return {"error": str(e)}
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/admin/users",
                json=user_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"创建用户失败: {str(e)}")
            return {"error": str(e)}
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户信息"""
        try:
            response = self.session.put(
                f"{self.base_url}/api/admin/users/{user_id}",
                json=user_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"更新用户失败: {str(e)}")
            return {"error": str(e)}
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """删除用户"""
        try:
            response = self.session.delete(f"{self.base_url}/api/admin/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"删除用户失败: {str(e)}")
            return {"error": str(e)}
    
    def get_attendance_report(self, start_date: str, end_date: str, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """获取考勤报表"""
        try:
            params = {"start_date": start_date, "end_date": end_date}
            if filters:
                params.update(filters)
            
            response = self.session.get(
                f"{self.base_url}/api/admin/reports/attendance",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"获取考勤报表失败: {str(e)}")
            return {"error": str(e)}
    
    def export_report(self, report_type: str, start_date: str, end_date: str, filters: Dict[str, Any] = None) -> bytes:
        """导出报表"""
        try:
            params = {
                "report_type": report_type,
                "start_date": start_date,
                "end_date": end_date
            }
            if filters:
                params.update(filters)
            
            response = self.session.get(
                f"{self.base_url}/api/admin/reports/export",
                params=params
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            st.error(f"导出报表失败: {str(e)}")
            return b""
    
    def get_attendance_trend(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """获取出勤率趋势"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/admin/analytics/trend",
                params={"start_date": start_date, "end_date": end_date}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"获取出勤率趋势失败: {str(e)}")
            return {"error": str(e)}
    
    def get_anomaly_alerts(self) -> Dict[str, Any]:
        """获取异常预警"""
        try:
            response = self.session.get(f"{self.base_url}/api/admin/alerts/anomaly")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"获取异常预警失败: {str(e)}")
            return {"error": str(e)}
