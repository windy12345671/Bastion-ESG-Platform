# Bastion ESG Platform - 部署指南

## 一、环境准备

### 1.1 硬件要求
- CPU: 2核+
- 内存: 4GB+
- 硬盘: 20GB+

### 1.2 软件要求
- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (本地开发)
- Python 3.11+ (本地开发)

---

## 二、本地开发部署

### 2.1 克隆代码
```bash
git clone https://github.com/YOUR_USERNAME/bastion-esg-platform.git
cd bastion-esg-platform
```

### 2.2 前端开发
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:3000
```

### 2.3 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
# API服务: http://localhost:5000
```

---

## 三、Docker部署

### 3.1 开发环境
```bash
docker-compose up -d
```
- 前端: http://localhost:3000
- 后端: http://localhost:5000
- Redis: localhost:6379

### 3.2 生产环境
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 四、云平台部署

### 4.1 前端 - Vercel
```bash
cd frontend
npm i -g vercel
vercel login
vercel --prod
```

### 4.2 后端 - Railway
1. 访问 https://railway.app
2. 连接GitHub仓库
3. 选择 backend 目录
4. 配置环境变量
5. 部署

### 4.3 数据库 - Supabase
1. 创建Supabase项目
2. 获取数据库URL和密钥
3. 配置到后端环境变量

---

## 五、环境变量配置

### 5.1 前端 (.env)
```env
VITE_API_URL=https://your-backend-url.railway.app
```

### 5.2 后端 (.env)
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgres://...
REDIS_URL=redis://...
```

---

## 六、GitHub Actions CI/CD

### 6.1 必需Secrets
在GitHub仓库 Settings > Secrets中配置:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `RAILWAY_TOKEN`
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

### 6.2 自动部署流程
1. 推送到main分支
2. 自动运行测试
3. 构建Docker镜像
4. 部署到Vercel (前端)
5. 部署到Railway (后端)

---

## 七、SSL证书配置

### Nginx反向代理
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # 前端
    location / {
        proxy_pass http://frontend:80;
    }

    # 后端API
    location /api {
        proxy_pass http://backend:5000;
    }
}
```

---

## 八、监控与日志

### 8.1 日志收集
```bash
docker-compose logs -f
```

### 8.2 性能监控
- 使用 Sentry 进行错误追踪
- 使用 Grafana + Prometheus 进行指标监控

---

## 九、故障排查

### 9.1 常见问题
1. **端口冲突**: 检查5000/3000端口占用
2. **数据库连接**: 验证环境变量配置
3. **构建失败**: 检查Node/Python版本

### 9.2 日志查看
```bash
docker-compose logs backend
docker-compose logs frontend
```

---

## 十、安全建议

1. 定期更新依赖包
2. 使用强密码和JWT密钥
3. 启用防火墙规则
4. 定期备份数据库
5. 启用HTTPS加密传输
