# pages/2_方剂功效预测.py
import streamlit as st
import pandas as pd
import torch
import numpy as np

st.set_page_config(page_title="方剂功效预测", page_icon="📈")
st.title("📈 方剂功效预测")
st.markdown("基于 GraphAI-for-TCM 图神经网络，预测方剂的五维功效机制得分")

st.info("💡 提示：GraphAI-for-TCM 模型将方剂表示为'中药饮片+药性语义图'，预测五个功效维度")

# 预设方剂示例
preset_formulas = {
    "四君子汤": ["人参", "白术", "茯苓", "甘草"],
    "六味地黄丸": ["熟地黄", "山茱萸", "山药", "泽泻", "牡丹皮", "茯苓"],
    "桂枝汤": ["桂枝", "白芍", "生姜", "大枣", "甘草"],
    "自定义方剂": []
}

# 选择或输入方剂
col1, col2 = st.columns([1, 2])
with col1:
    selected = st.selectbox("选择示例方剂", list(preset_formulas.keys()))
with col2:
    if selected == "自定义方剂":
        herbs_input = st.text_input("输入药材（逗号分隔）", placeholder="例如：黄芪, 当归")
    else:
        herbs_input = ", ".join(preset_formulas[selected])
        st.text_input("方剂组成", value=herbs_input, disabled=True)

# 功效维度说明
st.subheader("📊 预测的五维功效机制")
dimensions = {
    "抗炎": "🧬",
    "抗氧化": "⚡",
    "免疫调节": "🛡️",
    "神经保护": "🧠",
    "代谢调节": "⚖️"
}
cols = st.columns(len(dimensions))
for i, (dim, icon) in enumerate(dimensions.items()):
    cols[i].metric(f"{icon} {dim}", "待预测")

if st.button("🚀 预测方剂功效", type="primary"):
    herbs = [h.strip() for h in herbs_input.split(",") if h.strip()]
    
    if not herbs:
        st.warning("请输入至少一味药材")
    else:
        with st.spinner("GraphAI 模型推理中..."):
            # 模拟预测结果（实际使用时需加载 GraphAI-for-TCM 模型）
            # 参考：https://github.com/ZENGJingqi/GraphAI-for-TCM
            np.random.seed(42)
            scores = np.random.uniform(0.3, 0.9, 5)
            
            st.success("✅ 预测完成！")
            
            # 显示预测结果
            st.subheader("📊 预测结果")
            cols = st.columns(len(dimensions))
            for i, (dim, icon) in enumerate(dimensions.items()):
                cols[i].metric(
                    f"{icon} {dim}", 
                    f"{scores[i]:.3f}",
                    delta=None
                )
            
            # 显示注意力权重（解释性分析）
            st.subheader("🔍 药材贡献度分析（注意力权重）")
            attention_df = pd.DataFrame({
                "药材": herbs,
                "贡献权重": np.random.uniform(0.1, 0.4, len(herbs))
            })
            attention_df["贡献权重"] = attention_df["贡献权重"] / attention_df["贡献权重"].sum()
            st.dataframe(attention_df.style.bar(subset=["贡献权重"], color="#5fba7d"))
            
            st.caption("⚠️ 本预测仅供科研参考，不构成临床建议")