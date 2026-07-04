
import streamlit as st
import subprocess
import json
import tempfile
import os

st.set_page_config(page_title="网络药理学分析", page_icon="🧬")
st.title("🧬 网络药理学分析")
st.markdown("基于 TCMNPAS 进行方剂成分与疾病靶点的网络药理学分析[reference:5]")

# 输入区域
herbs_input = st.text_area(
    "请输入方剂组成（药材名称，用逗号分隔）",
    placeholder="例如：黄芪, 当归, 川芎, 白芍"
)

# 选择分析类型
analysis_type = st.selectbox(
    "选择分析类型",
    ["核心方剂挖掘", "靶点预测", "网络构建"]
)

if st.button("🔬 开始分析", type="primary"):
    if not herbs_input.strip():
        st.warning("请输入药材名称")
    else:
        with st.spinner("正在运行 TCMNPAS 分析，请稍候..."):
            try:
                # 构建临时 R 脚本
                r_script = f'''
                library(tcmnpas)
                
                # 解析输入的药材
                herbs <- strsplit("{herbs_input}", ",")[[1]]
                herbs <- trimws(herbs)
                
                # 执行分析（根据分析类型调用不同函数）
                # 此处为示例逻辑，实际需根据 TCMNPAS API 调整
                result <- list(
                    status = "success",
                    herbs = herbs,
                    analysis_type = "{analysis_type}",
                    message = paste("已分析", length(herbs), "味药材")
                )
                
                cat(jsonlite::toJSON(result))
                '''
                
                # 将 R 脚本写入临时文件
                with tempfile.NamedTemporaryFile(mode='w', suffix='.R', delete=False) as f:
                    f.write(r_script)
                    r_script_path = f.name
                
                # 调用 Rscript 执行[reference:6]
                result = subprocess.run(
                    ["Rscript", r_script_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                # 清理临时文件
                os.unlink(r_script_path)
                
                # 解析结果
                output = json.loads(result.stdout)
                
                st.success("✅ 分析完成！")
                st.json(output)
                
                # 显示结果摘要
                st.subheader("📊 分析结果摘要")
                st.write(f"- 分析类型：{output.get('analysis_type')}")
                st.write(f"- 药材数量：{len(output.get('herbs', []))} 味")
                st.write(f"- 状态：{output.get('message')}")
                
            except subprocess.CalledProcessError as e:
                st.error(f"R 脚本执行失败：{e.stderr}")
            except Exception as e:
                st.error(f"分析出错：{str(e)}")