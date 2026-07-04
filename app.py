# app.py
import streamlit as st

# 设置页面配置
st.set_page_config(page_title="TCM 智能分析平台", page_icon="🏥", layout="wide")

# 定义各个页面（自动读取 pages/ 目录下的文件）
# Streamlit 会自动识别 pages/ 目录中的 .py 文件并生成导航[reference:1]
# 也可以手动定义更精细的导航[reference:2]

# 如果 pages/ 目录存在，Streamlit 会自动在侧边栏生成导航
# 只需要在 app.py 中写一些欢迎内容即可
st.title("🏥 中医药智能分析平台")
st.markdown("""
欢迎使用中医药智能分析平台！请从左侧导航栏选择功能模块：

- **网络药理学分析**：基于 TCMNPAS 进行方剂成分与靶点分析
- **方剂功效预测**：基于 GraphAI-for-TCM 图神经网络预测方剂功效
- **中医智能问答**：基于 MedChatZH / 黄帝 大模型进行古籍问答
- **知识图谱可视化**：基于 Neo4j 展示方剂-药材-靶点关系图
""")