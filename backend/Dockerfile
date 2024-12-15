# 后端 Dockerfile
FROM python:3.8-slim

WORKDIR /app

# 安装 PostgreSQL 开发包
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 修改 requirements.txt 中的 psycopg2 为 psycopg2-binary
RUN sed -i 's/psycopg2>=2.9.6/psycopg2-binary>=2.9.6/g' requirements.txt

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
