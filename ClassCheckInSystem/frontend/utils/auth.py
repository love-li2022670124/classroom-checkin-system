"""
认证管理模块
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
from typing import Dict, Optional, Any
import hashlib
import json
from datetime import datetime, timedelta

class AuthManager:
    """认证管理器"""
    
    def __init__(self):
        self.session_key = "user_session"
        self.user_info_key = "user_info"
    
    def is_logged_in(self) -> bool:
        """检查用户是否已登录"""
        return self.session_key in st.session_state and st.session_state[self.session_key] is not None
    
    def login(self, username: str, password: str, api_client) -> bool:
        """用户登录"""
        try:
            # 调用API进行登录
            result = api_client.login(username, password)
            
            if "error" not in result and ("access_token" in result or "token" in result):
                # 登录成功，保存会话信息
                token = result.get("access_token") or result.get("token")
                st.session_state[self.session_key] = token
                st.session_state[self.user_info_key] = result.get("user", {})
                
                # 设置API客户端的认证令牌
                api_client.set_auth_token(token)
                
                return True
            else:
                # 显示详细的错误信息
                error_msg = result.get("error", "未知错误")
                st.error(f"登录失败：{error_msg}")
                st.write("**调试信息：**")
                st.write(f"- API响应: {result}")
                st.write(f"- 用户名: {username}")
                st.write(f"- 密码长度: {len(password)}")
                return False
                
        except Exception as e:
            st.error(f"登录过程中发生错误：{str(e)}")
            return False
    
    def logout(self):
        """用户登出"""
        # 清除会话状态
        if self.session_key in st.session_state:
            del st.session_state[self.session_key]
        if self.user_info_key in st.session_state:
            del st.session_state[self.user_info_key]
        
        st.success("已成功登出")
        st.rerun()
    
    def get_user_info(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        if self.is_logged_in():
            return st.session_state.get(self.user_info_key, {})
        return {}
    
    def get_user_role(self) -> str:
        """获取当前用户角色"""
        user_info = self.get_user_info()
        return user_info.get("role", "student")
    
    def get_user_id(self) -> Optional[int]:
        """获取当前用户ID"""
        user_info = self.get_user_info()
        return user_info.get("id")
    
    def get_user_name(self) -> str:
        """获取当前用户名"""
        user_info = self.get_user_info()
        return user_info.get("name", "用户")
    
    def has_permission(self, required_role: str) -> bool:
        """检查用户是否有指定权限"""
        user_role = self.get_user_role()
        
        # 权限等级：admin > teacher > student
        role_levels = {
            "admin": 3,
            "teacher": 2,
            "student": 1
        }
        
        user_level = role_levels.get(user_role, 0)
        required_level = role_levels.get(required_role, 0)
        
        return user_level >= required_level
    
    def require_login(self):
        """要求用户登录（装饰器功能）"""
        if not self.is_logged_in():
            st.warning("请先登录")
            st.stop()
    
    def require_role(self, required_role: str):
        """要求特定角色权限"""
        self.require_login()
        
        if not self.has_permission(required_role):
            st.error(f"权限不足：需要{required_role}权限")
            st.stop()
    
    def get_auth_token(self) -> Optional[str]:
        """获取认证令牌"""
        if self.is_logged_in():
            return st.session_state.get(self.session_key)
        return None
    
    def refresh_user_info(self, api_client):
        """刷新用户信息"""
        if self.is_logged_in():
            try:
                result = api_client.get_user_info()
                if "error" not in result:
                    st.session_state[self.user_info_key] = result
                    return True
            except Exception as e:
                st.error(f"刷新用户信息失败：{str(e)}")
        return False
    
    def is_token_expired(self) -> bool:
        """检查令牌是否过期"""
        # 这里可以实现令牌过期检查逻辑
        # 目前简化处理，假设令牌不会过期
        return False
    
    def validate_session(self, api_client) -> bool:
        """验证会话有效性"""
        if not self.is_logged_in():
            return False
        
        if self.is_token_expired():
            self.logout()
            return False
        
        # 可以定期刷新用户信息
        return self.refresh_user_info(api_client)
