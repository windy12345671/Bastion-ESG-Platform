# Bastion ESG Intelligence Platform

<p align="center">
  <img src="public/bastion-logo.svg" width="120" alt="Bastion Logo">
</p>

<p align="center">
  <strong>武汉Bastion信息科技有限公司</strong>
  <br>
  智能ESG评估平台 - 连接资本与责任，科技与可持续发展
</p>

<p align="center">
  <a href="#功能特点">功能</a> •
  <a href="#技术栈">技术栈</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#API文档">API</a> •
  <a href="#部署">部署</a>
</p>

---

## 🌟 项目简介

Bastion ESG Intelligence Platform 是一款面向企业和金融机构的智能ESG评估系统。平台整合AI大模型与多源数据，为企业提供自动化的ESG报告生成服务，同时为银行等金融机构提供深度的ESG风险评估支持。

### 核心功能

- 🔍 **企业ESG评估** - 输入企业名称或上传ESG报告，自动生成专业评估结果
- 📊 **智能报告生成** - 支持多种模板，一键生成PDF/Word/HTML格式报告
- 🏆 **ESG排名分析** - 全行业ESG排名追踪，趋势分析
- 📰 **ESG资讯聚合** - 实时追踪政策法规、市场动态
- 🔐 **数据安全保障** - 全链密钥加密，差分隐私技术

## ✨ 功能特点

### ESG评分引擎
- 基于随机森林+XGBoost+LGBM混合模型
- 整合1000+数据点，覆盖16个核心议题和150+精细指标
- 行业差异化评价体系
- PDP+Knee拐点权重优化

### 报告生成
- 模块化报告生成技术
- 支持上市公司、中小企业、金融机构等多场景
- 自动行业对比分析
- 多格式导出支持

### 技术亮点
- AI+遥感数据融合
- SiameseLink融资智能匹配
- 全链密钥加密算法
- 响应式Web界面

## 🛠 技术栈

### 后端
- **框架**: Flask 3.0 / Django
- **数据库**: PostgreSQL, MongoDB, Redis
- **NLP**: Hugging Face Transformers, BERT
- **ML**: scikit-learn, XGBoost, LightGBM

### 前端
- **框架**: React 18 + TypeScript
- **UI**: Tailwind CSS, shadcn/ui
- **可视化**: Recharts, D3.js, Three.js
- **动画**: Framer Motion

### 部署
- **容器化**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **托管**: Vercel, Railway

## 🚀 快速开始

### 环境要求
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose (可选)

### 1. 克隆项目
```bash
git clone https://github.com/your-username/bastion-esg-platform.git
cd bastion-esg-platform
```

### 2. 前端启动
```bash
cd frontend
npm install
npm run dev
```
访问 http://localhost:3000

### 3. 后端启动
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```
API服务将运行在 http://localhost:5000

### 4. Docker部署
```bash
docker-compose up -d
```

## 📡 API文档

### 认证接口
```
POST /api/auth/register     - 用户注册
POST /api/auth/login        - 用户登录
POST /api/auth/refresh      - 刷新Token
```

### 企业接口
```
GET  /api/companies         - 企业列表
GET  /api/companies/{id}    - 企业详情
POST /api/companies/search  - 企业搜索
POST /api/companies/import  - 批量导入
```

### 评估接口
```
POST /api/assessment/start  - 启动评估
GET  /api/assessment/{id}   - 获取评估结果
GET  /api/assessment/{id}/report - 生成报告
GET  /api/assessment/{id}/score - 获取评分详情
```

### 报告接口
```
POST /api/report/generate   - 生成报告
GET  /api/report/{id}       - 获取报告
GET  /api/report/{id}/download - 下载报告
```

### 数据接口
```
GET  /api/data/industry/{id} - 行业数据
GET  /api/data/trends       - ESG趋势
GET  /api/data/ranking      - 排名数据
POST /api/data/comparison   - 对比分析
```

## 📁 项目结构

```
bastion-esg-platform/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API路由
│   │   ├── ml/                # 机器学习模块
│   │   └── services/          # 业务逻辑
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/        # React组件
│   │   ├── pages/            # 页面
│   │   └── styles/           # 样式
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── docs/                       # 文档
├── docker-compose.yml          # Docker编排
└── README.md                   # 项目说明
```

## 🔒 ESG评分体系

### 评分维度
| 维度 | 权重 | 核心议题 |
|------|------|----------|
| 环境 (E) | 35% | 气候变化、资源利用、污染治理、生态保护 |
| 社会 (S) | 35% | 员工权益、供应链责任、社区参与、产品责任 |
| 治理 (G) | 30% | 公司治理、商业道德、风险管理 |

### 评级标准
| 评级 | 分数范围 | 说明 |
|------|----------|------|
| AAA | 900-1000 | 卓越 |
| AA | 800-899 | 优秀 |
| A | 700-799 | 良好 |
| BBB | 600-699 | 尚可 |
| BB | 500-599 | 一般 |
| B | 400-499 | 较差 |

## 🌐 部署指南

### Vercel部署前端
```bash
cd frontend
vercel
```

### Railway部署后端
```bash
cd backend
railway up
```

### Docker生产环境
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- **公司**: 武汉Bastion信息科技有限公司
- **邮箱**: contact@bastion-esg.com
- **网站**: https://bastion-esg.com

---

<p align="center">
  Made with ❤️ by <a href="#">Bastion Team</a>
</p>
