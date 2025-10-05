# 生产环境部署说明

## 🚀 Streamlit Cloud 部署 (推荐)

### 1. 准备代码
- 确保所有代码都在GitHub仓库中
- 检查 `requirements.txt` 包含所有依赖

### 2. 部署步骤
1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 点击 "New app"
3. 连接你的GitHub仓库
4. 选择 `frontend/app.py` 作为主文件
5. 点击 "Deploy"

### 3. 环境变量设置
在Streamlit Cloud的Secrets页面设置：
```
BACKEND_API_URL = "https://your-backend-url.com"
JWT_SECRET = "your-production-secret"
```

## 🌐 其他部署方案

### Heroku 部署
1. 创建 `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. 创建 `runtime.txt`:
   ```
   python-3.11.0
   ```

### VPS 部署
1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 使用systemd服务:
   ```bash
   sudo systemctl enable streamlit-app
   sudo systemctl start streamlit-app
   ```

3. 配置Nginx反向代理

## 🔧 生产环境优化

### 1. 后端部署
- 使用PostgreSQL替代SQLite
- 配置Redis缓存
- 设置环境变量

### 2. 安全配置
- 使用HTTPS
- 设置CORS策略
- 配置防火墙

### 3. 监控和日志
- 添加日志记录
- 设置健康检查
- 配置监控告警

## 📱 访问方式
部署完成后，用户可以通过以下方式访问：
- **Web浏览器**: 访问部署的URL
- **移动端**: 支持响应式设计
- **API**: 后端API可供其他应用调用
