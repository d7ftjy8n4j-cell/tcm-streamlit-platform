# pages/3_中医智能问答.py
import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

st.set_page_config(page_title="中医智能问答", page_icon="💬")
st.title("💬 中医智能问答")
st.markdown("基于 MedChatZH / 黄帝 大模型，进行中医古籍与诊疗知识问答")

# 模型选择
model_option = st.radio(
    "选择模型",
    ["MedChatZH (Baichuan-7B)", "黄帝 (Ziya-LLaMA-13B)"],
    help="MedChatZH 擅长中医诊疗问答，黄帝擅长古籍知识问答"
)

# 会话历史管理
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史对话
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 用户输入
if prompt := st.chat_input("请输入您的中医问题..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # 生成回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            # 模拟回复（实际使用时需加载模型）
            # MedChatZH 模型下载：https://huggingface.co/tyang816/MedChatZH
            # 黄帝模型下载：百度网盘
            
            # 简单模拟回复逻辑
            if "咳嗽" in prompt:
                response = "中医认为咳嗽多因外感六淫或内伤脏腑所致。治疗上需辨证论治，风寒咳嗽可用三拗汤，风热咳嗽可用桑菊饮，痰湿咳嗽可用二陈汤。建议您咨询专业中医师进行辨证施治。"
            elif "失眠" in prompt:
                response = "中医治疗失眠常用酸枣仁汤、天王补心丹等方剂。同时建议配合针灸、推拿等疗法，并注意调整作息和饮食习惯。"
            elif "脱发" in prompt:
                response = "中药治疗脱发效果因人而异。常用方剂包括六味地黄丸、四物汤等，可滋养肝肾、促进血液循环。建议咨询专业中医医生制定个性化方案。"
            else:
                response = f"感谢您的提问。关于「{prompt}」这个问题，建议您查阅相关中医典籍或咨询专业中医师。如需更精准的回答，请加载完整的模型权重进行推理。"
            
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# 清空对话按钮
if st.sidebar.button("🗑️ 清空对话"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.info(
    "💡 **使用说明**\n\n"
    "1. 选择要使用的模型\n"
    "2. 在输入框中提出您的中医问题\n"
    "3. 模型将基于中医知识进行回答\n\n"
    "⚠️ 回答仅供学习参考，不构成医疗建议"
)