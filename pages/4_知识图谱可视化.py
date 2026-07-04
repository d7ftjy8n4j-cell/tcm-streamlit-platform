# pages/4_知识图谱可视化.py
import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
from pyvis.network import Network
import tempfile

st.set_page_config(page_title="知识图谱可视化", page_icon="🕸️")
st.title("🕸️ 中医药知识图谱可视化")
st.markdown("基于 Neo4j 展示方剂-药材-靶点-疾病的关系网络")

# Neo4j 连接配置
with st.sidebar:
    st.subheader("🔌 数据库连接")
    neo4j_uri = st.text_input("Neo4j URI", value="bolt://localhost:7687")
    neo4j_user = st.text_input("用户名", value="neo4j")
    neo4j_password = st.text_input("密码", type="password")
    
    if st.button("连接数据库"):
        try:
            driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                st.session_state.neo4j_driver = driver
                st.success("✅ 连接成功！")
        except Exception as e:
            st.error(f"连接失败：{e}")

# 查询区域
st.subheader("🔍 查询知识图谱")

query_type = st.selectbox(
    "选择查询类型",
    ["方剂-药材关系", "药材-靶点关系", "靶点-疾病关系", "自定义查询"]
)

if query_type == "方剂-药材关系":
    formula_name = st.text_input("输入方剂名称", placeholder="例如：四君子汤")
    if st.button("查询") and "neo4j_driver" in st.session_state:
        driver = st.session_state.neo4j_driver
        with driver.session() as session:
            # Cypher 查询
            result = session.run(
                "MATCH (f:Formula {name: $name})-[:CONTAINS]->(h:Herb) RETURN f, h",
                name=formula_name
            )
            records = list(result)
            if records:
                st.success(f"找到 {len(records)} 味药材")
                # 构建 PyVis 网络图
                net = Network(height="500px", width="100%", notebook=False)
                net.add_node(formula_name, label=formula_name, color="#ff7f0e")
                for record in records:
                    herb = record["h"]
                    net.add_node(herb["name"], label=herb["name"], color="#1f77b4")
                    net.add_edge(formula_name, herb["name"])
                
                # 显示图谱
                with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
                    net.save_graph(f.name)
                    st.components.v1.html(open(f.name, 'r').read(), height=550)
            else:
                st.warning("未找到该方剂")
elif query_type == "自定义查询":
    cypher_query = st.text_area("输入 Cypher 查询语句", height=100)
    if st.button("执行查询") and "neo4j_driver" in st.session_state:
        driver = st.session_state.neo4j_driver
        with driver.session() as session:
            result = session.run(cypher_query)
            data = [record.data() for record in result]
            st.json(data)
else:
    st.info("请先连接 Neo4j 数据库并选择查询类型")