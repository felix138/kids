# 前端 Dockerfile
FROM node:14-alpine

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制前端代码
COPY . .

# 构建生产版本
RUN npm run build

# 使用 nginx 服务静态文件
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d/default.conf  # 暂时注释掉这行
EXPOSE 80
