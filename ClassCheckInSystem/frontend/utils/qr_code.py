"""
二维码生成和处理模块
"""

import qrcode  # pyright: ignore[reportMissingModuleSource]
import io
import base64
from typing import Dict, Any, Optional
import streamlit as st  # pyright: ignore[reportMissingImports]

class QRCodeGenerator:
    """二维码生成器"""
    
    def __init__(self):
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    
    def generate_qr_code(self, data: Dict[str, Any]) -> Optional[bytes]:
        """生成二维码图片"""
        try:
            # 将数据转换为JSON字符串
            import json
            qr_data_str = json.dumps(data, ensure_ascii=False)
            
            # 生成二维码
            self.qr.clear()
            self.qr.add_data(qr_data_str)
            self.qr.make(fit=True)
            
            # 创建二维码图片
            img = self.qr.make_image(fill_color="black", back_color="white")
            
            # 转换为字节
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
            
            return img_bytes
            
        except Exception as e:
            st.error(f"生成二维码失败: {str(e)}")
            return None
    
    def get_qr_bytes(self, data: Dict[str, Any]) -> bytes:
        """获取二维码字节数据"""
        return self.generate_qr_code(data)
    
    def generate_qr_base64(self, data: Dict[str, Any]) -> Optional[str]:
        """生成二维码的base64编码"""
        img_bytes = self.generate_qr_code(data)
        if img_bytes:
            return base64.b64encode(img_bytes).decode()
        return None
    
    def create_attendance_qr(self, course_id: int, student_id: int, expiry_minutes: int = 5) -> Dict[str, Any]:
        """创建考勤二维码数据"""
        from datetime import datetime, timedelta
        
        qr_data = {
            "type": "attendance",
            "course_id": course_id,
            "student_id": student_id,
            "timestamp": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(minutes=expiry_minutes)).isoformat(),
            "version": "1.0"
        }
        
        return qr_data
    
    def validate_qr_data(self, qr_data: Dict[str, Any]) -> bool:
        """验证二维码数据"""
        required_fields = ["type", "course_id", "student_id", "timestamp"]
        
        for field in required_fields:
            if field not in qr_data:
                return False
        
        # 检查过期时间
        if "expires_at" in qr_data:
            from datetime import datetime
            try:
                expires_at = datetime.fromisoformat(qr_data["expires_at"])
                if datetime.now() > expires_at:
                    return False
            except ValueError:
                return False
        
        return True
    
    def parse_qr_data(self, qr_string: str) -> Optional[Dict[str, Any]]:
        """解析二维码字符串"""
        try:
            import json
            data = json.loads(qr_string)
            
            if self.validate_qr_data(data):
                return data
            else:
                st.error("二维码数据无效或已过期")
                return None
                
        except json.JSONDecodeError:
            st.error("无法解析二维码数据")
            return None
        except Exception as e:
            st.error(f"解析二维码时发生错误: {str(e)}")
            return None
