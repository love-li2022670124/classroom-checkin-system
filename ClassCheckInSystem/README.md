# 课堂考勤签到系统

一个基于Streamlit的现代化课堂考勤签到系统，支持二维码签到、位置签到、实时统计等功能。

## 🚀 快速开始

### 本地运行

1. **安装依赖**
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

2. **启动后端服务**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 127.0.0.1 --port 5000
   ```

3. **启动前端服务**
   ```bash
   cd frontend
   streamlit run app.py
   ```

4. **访问应用**
   - 前端: http://127.0.0.1:8501
   - 后端API: http://127.0.0.1:5000

## 📱 功能特性

### 学生端
- 📱 二维码签到
- 📍 位置签到
- 📊 考勤记录查询
- 📝 异常反馈

### 教师端
- 📈 实时出勤率统计
- 🔄 补签管理
- 📋 反馈处理
- 📊 数据分析

### 管理员端
- 👥 用户管理
- 📚 课程管理
- 📊 报表查询
- ⚙️ 系统设置

## 🛠️ 技术栈

- **前端**: Streamlit, Plotly, Pandas
- **后端**: FastAPI, SQLAlchemy, Redis
- **数据库**: SQLite/PostgreSQL
- **认证**: JWT Token

## 📦 部署

### Streamlit Cloud
1. Fork 此仓库
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接GitHub仓库
4. 选择 `frontend/app.py` 作为主文件
5. 点击 Deploy

## 📄 许可证

MIT License
