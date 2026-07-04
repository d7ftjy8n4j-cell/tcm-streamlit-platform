#!/bin/bash
set -e  # 遇到错误立即退出

echo "=== 更新系统软件源 ==="
apt-get update

echo "=== 安装 R 及系统依赖 ==="
apt-get install -y --no-install-recommends \
    r-base \
    r-base-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    git \
    wget

echo "=== 安装 R 包（jsonlite, igraph, visNetwork, devtools） ==="
Rscript -e "install.packages(c('jsonlite', 'igraph', 'visNetwork', 'devtools'), repos='https://cloud.r-project.org/')"

echo "=== 安装 TCMNPAS（从 GitHub） ==="
Rscript -e "devtools::install_github('yangpluszhu/tcmnpas')"

echo "=== 安装 Python 依赖 ==="
# 如果仓库根目录有 requirements.txt，则用它安装
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    # 否则安装常用包
    pip install streamlit neo4j pandas pyvis torch transformers numpy
fi

echo "=== 环境安装完成！==="
