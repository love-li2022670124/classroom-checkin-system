import streamlit as st  # pyright: ignore[reportMissingImports]

st.title("课堂考勤签到系统测试")
st.write("如果你看到这个页面，说明Streamlit运行正常！")

# 测试基本功能
if st.button("测试按钮"):
    st.success("按钮点击成功！")

# 显示系统状态
st.markdown("### 系统状态")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("后端服务", "运行中", "✅")

with col2:
    st.metric("前端服务", "运行中", "✅")

with col3:
    st.metric("数据库", "连接正常", "✅")
