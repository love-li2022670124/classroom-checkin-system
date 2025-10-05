# 课堂考勤签到系统 - Streamlit前端项目

## 🎯 项目概述

这是一个基于Streamlit框架构建的课堂考勤签到系统前端项目，与Flask后端无缝对接，提供完整的学生、教师、管理员三端功能。

## 📁 项目结构

```
frontend/
├── .streamlit/                 # Streamlit配置
│   └── config.toml            # 配置文件
├── pages/                      # 多页面应用
│   ├── 1_学生端.py            # 学生功能页面
│   ├── 2_教师端.py            # 教师功能页面
│   └── 3_管理员端.py           # 管理员功能页面
├── utils/                      # 工具函数
│   ├── __init__.py
│   ├── api_client.py          # Flask API客户端
│   ├── auth.py               # 认证管理
│   ├── qr_code.py            # 二维码生成
│   ├── geolocation.py        # 地理位置处理
│   └── charts.py             # 图表组件
├── components/                 # 通用组件
│   ├── __init__.py
│   ├── forms.py              # 表单组件
│   └── tables.py             # 表格组件
├── assets/                     # 静态资源
│   └── styles.css            # 自定义样式
├── app.py                     # 主应用入口
├── run.py                     # 启动脚本
├── requirements.txt           # 依赖包
└── README.md                  # 项目说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
# 方法1：使用启动脚本
python run.py

# 方法2：直接启动
streamlit run app.py
```

### 3. 访问应用

打开浏览器访问：http://127.0.0.1:8501

## 🎨 功能特性

### 学生端功能
- 🔐 **用户登录认证** - 安全的JWT认证系统
- 📱 **二维码签到** - 生成和扫描二维码进行签到
- 📍 **地理位置签到** - 基于GPS的位置签到（1公里范围）
- 📊 **个人考勤记录查询** - 查看个人出勤历史和统计
- 📝 **考勤异常反馈** - 提交考勤问题反馈

### 教师端功能
- 📈 **实时出勤率统计** - 实时监控课堂出勤情况
- ✏️ **手动补签管理** - 为学生进行补签操作
- 📋 **反馈处理** - 处理学生提交的考勤反馈
- 📊 **数据分析** - 出勤率趋势分析和课程对比

### 管理员端功能
- 👥 **用户管理** - 学生、教师、管理员的增删改查
- 📚 **课程管理** - 课程信息的创建和管理
- 📊 **报表查询** - 多维度考勤报表生成和导出
- 📈 **数据分析** - 全校出勤率趋势和异常分析
- ⚙️ **系统设置** - 系统配置和监控

## 🛠️ 技术栈

- **前端框架**: Streamlit 1.28+
- **后端对接**: Flask API
- **数据可视化**: Plotly, Streamlit-AgGrid
- **地图功能**: Folium, Geopy
- **二维码**: QRCode
- **样式美化**: Streamlit-Extras, 自定义CSS
- **状态管理**: Streamlit Session State
- **HTTP客户端**: Requests

## 🔧 配置说明

### 环境变量
```bash
# Flask后端API地址
FLASK_API_URL=http://localhost:5000

# 数据库配置
DB_URL=sqlite:///./dev.db

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT配置
JWT_SECRET=your-secret-key
```

### Streamlit配置
配置文件位于 `.streamlit/config.toml`：

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## 📡 API对接

### 主要API端点

#### 认证相关
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/user` - 获取用户信息

#### 学生端API
- `POST /api/student/sign/qrcode/generate` - 生成签到二维码
- `POST /api/student/sign/qrcode` - 二维码签到
- `POST /api/student/sign/location` - 位置签到
- `GET /api/student/attendance` - 获取考勤记录
- `POST /api/student/feedback` - 提交反馈

#### 教师端API
- `GET /api/teacher/attendance/rate` - 获取出勤率
- `POST /api/teacher/makeup` - 手动补签
- `GET /api/teacher/feedback/pending` - 获取待处理反馈
- `POST /api/teacher/feedback/handle` - 处理反馈

#### 管理员端API
- `GET /api/admin/users` - 获取用户列表
- `POST /api/admin/users` - 创建用户
- `PUT /api/admin/users/{id}` - 更新用户
- `DELETE /api/admin/users/{id}` - 删除用户
- `GET /api/admin/reports/attendance` - 获取考勤报表
- `GET /api/admin/reports/export` - 导出报表
- `GET /api/admin/analytics/trend` - 获取趋势数据

## 🎨 界面特色

### 精美设计
- 🎨 **现代化UI** - 使用渐变色彩和卡片设计
- 📱 **响应式布局** - 支持桌面和移动设备
- 🌈 **主题定制** - 可自定义颜色主题
- ✨ **动画效果** - 流畅的过渡动画

### 丰富组件
- 📊 **数据可视化** - Plotly图表和仪表盘
- 📋 **智能表格** - Streamlit-AgGrid高级表格
- 🗺️ **地图集成** - Folium地图组件
- 📱 **二维码** - 生成和识别二维码
- 📍 **地理位置** - GPS定位和距离计算

## 🔒 安全特性

- 🔐 **JWT认证** - 安全的令牌认证
- 🛡️ **权限控制** - 基于角色的访问控制
- 🔒 **数据加密** - 敏感数据加密传输
- 🚫 **CSRF保护** - 跨站请求伪造保护

## 📊 数据可视化

### 图表类型
- 📈 **趋势图** - 出勤率趋势分析
- 🥧 **饼图** - 出勤率分布
- 📊 **柱状图** - 课程对比分析
- 🌡️ **热力图** - 异常情况分析
- 📊 **仪表盘** - 实时指标监控

### 交互功能
- 🔍 **数据筛选** - 多维度数据筛选
- 📥 **报表导出** - Excel/CSV/PDF导出
- 🖨️ **打印支持** - 优化的打印样式
- 📱 **移动适配** - 响应式图表显示

## 🚀 部署说明

### 本地开发
```bash
# 克隆项目
git clone <repository-url>
cd frontend

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
streamlit run app.py
```

### 生产部署
```bash
# 使用Docker部署
docker build -t attendance-frontend .
docker run -p 8501:8501 attendance-frontend

# 使用Streamlit Cloud部署
# 将代码推送到GitHub，然后在Streamlit Cloud中部署
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 更新日志

### v1.0.0 (2024-01-15)
- ✨ 初始版本发布
- 🎨 完整的三端功能实现
- 📊 丰富的数据可视化
- 🔒 安全的认证系统
- 📱 响应式界面设计

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者: [Your Name]
- 邮箱: [your.email@example.com]
- 项目链接: [https://github.com/yourusername/attendance-system]

## 🙏 致谢

感谢以下开源项目的支持：
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Folium](https://python-visualization.github.io/folium/)
- [QRCode](https://github.com/lincolnloop/python-qrcode)