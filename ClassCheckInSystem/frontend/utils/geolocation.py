"""
地理位置处理模块
"""

import streamlit as st  # pyright: ignore[reportMissingImports]
import folium  # pyright: ignore[reportMissingImports]
from folium import plugins  # pyright: ignore[reportMissingImports]
import streamlit.components.v1 as components  # pyright: ignore[reportMissingImports]
from typing import Dict, Optional, Tuple
import math

class LocationManager:
    """地理位置管理器"""
    
    def __init__(self):
        self.default_location = (39.9042, 116.4074)  # 北京坐标
    
    def get_current_location(self) -> Optional[Dict[str, float]]:
        """获取当前位置（模拟）"""
        # 在实际应用中，这里应该使用浏览器的Geolocation API
        # 由于Streamlit的限制，我们使用模拟数据
        
        # 模拟获取位置
        mock_location = {
            "lat": 39.9042 + (st.session_state.get("location_offset", 0) * 0.001),
            "lng": 116.4074 + (st.session_state.get("location_offset", 0) * 0.001),
            "accuracy": 10.0
        }
        
        # 更新偏移量以模拟不同位置
        if "location_offset" not in st.session_state:
            st.session_state["location_offset"] = 0
        else:
            st.session_state["location_offset"] += 1
        
        return mock_location
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """计算两点间距离（米）"""
        # 使用Haversine公式计算距离
        R = 6371000  # 地球半径（米）
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def is_within_range(self, current_lat: float, current_lng: float, 
                        target_lat: float, target_lng: float, 
                        max_distance: float = 1000) -> bool:
        """检查是否在指定范围内"""
        distance = self.calculate_distance(current_lat, current_lng, target_lat, target_lng)
        return distance <= max_distance
    
    def create_map(self, classroom_lat: float, classroom_lng: float, 
                   current_lat: Optional[float] = None, 
                   current_lng: Optional[float] = None) -> str:
        """创建地图"""
        # 创建地图
        m = folium.Map(
            location=[classroom_lat, classroom_lng],
            zoom_start=15,
            tiles='OpenStreetMap'
        )
        
        # 添加教室标记
        folium.Marker(
            [classroom_lat, classroom_lng],
            popup="教室位置",
            tooltip="教室",
            icon=folium.Icon(color='red', icon='graduation-cap', prefix='fa')
        ).add_to(m)
        
        # 添加签到范围圆圈
        folium.Circle(
            [classroom_lat, classroom_lng],
            radius=1000,  # 1公里
            popup="签到范围（1公里）",
            color='blue',
            fill=True,
            fillColor='lightblue',
            fillOpacity=0.2
        ).add_to(m)
        
        # 如果有当前位置，添加当前位置标记
        if current_lat and current_lng:
            folium.Marker(
                [current_lat, current_lng],
                popup="当前位置",
                tooltip="我的位置",
                icon=folium.Icon(color='green', icon='user', prefix='fa')
            ).add_to(m)
            
            # 添加从当前位置到教室的连线
            folium.PolyLine(
                [[current_lat, current_lng], [classroom_lat, classroom_lng]],
                color='green',
                weight=2,
                opacity=0.7
            ).add_to(m)
            
            # 计算并显示距离
            distance = self.calculate_distance(current_lat, current_lng, classroom_lat, classroom_lng)
            
            # 在连线中点添加距离标签
            mid_lat = (current_lat + classroom_lat) / 2
            mid_lng = (current_lng + classroom_lng) / 2
            
            folium.Marker(
                [mid_lat, mid_lng],
                icon=folium.DivIcon(
                    html=f'<div style="background: white; border: 1px solid black; padding: 2px; border-radius: 3px; font-size: 12px;">{distance:.0f}m</div>',
                    icon_size=(50, 20),
                    icon_anchor=(25, 10)
                )
            ).add_to(m)
        
        # 添加全屏控件
        plugins.Fullscreen().add_to(m)
        
        # 添加测量工具
        plugins.MeasureControl().add_to(m)
        
        # 返回HTML字符串
        return m._repr_html_()
    
    def get_location_info(self, lat: float, lng: float) -> Dict[str, str]:
        """获取位置信息（模拟）"""
        # 在实际应用中，这里应该调用地理编码API
        return {
            "address": f"纬度: {lat:.6f}, 经度: {lng:.6f}",
            "city": "北京市",
            "district": "朝阳区",
            "accuracy": "高精度"
        }
    
    def validate_coordinates(self, lat: float, lng: float) -> bool:
        """验证坐标是否有效"""
        return -90 <= lat <= 90 and -180 <= lng <= 180
    
    def format_coordinates(self, lat: float, lng: float, precision: int = 6) -> Tuple[str, str]:
        """格式化坐标显示"""
        return f"{lat:.{precision}f}", f"{lng:.{precision}f}"
    
    def get_nearby_locations(self, lat: float, lng: float, radius: float = 1000) -> list:
        """获取附近位置（模拟）"""
        # 模拟附近位置数据
        nearby = [
            {"name": "教学楼A", "lat": lat + 0.001, "lng": lng + 0.001, "distance": 150},
            {"name": "图书馆", "lat": lat - 0.001, "lng": lng + 0.002, "distance": 300},
            {"name": "食堂", "lat": lat + 0.002, "lng": lng - 0.001, "distance": 500},
            {"name": "体育馆", "lat": lat - 0.002, "lng": lng - 0.002, "distance": 800}
        ]
        
        return nearby
