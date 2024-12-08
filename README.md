# AI Utdanningsassistent for Barn

En intelligent utdanningsplattform basert på Grok, som tilbyr personlig læring og interaktiv underholdning for barn.

## Prosjektoversikt

Dette prosjektet har som mål å skape en barnevennlig, trygg og morsom AI-utdanningsplattform. Ved å kombinere Groks naturlige språkbehandlingsevner, tilbyr vi personlig læring, kunnskapsbaserte spørsmål og svar, og interaktiv underholdning for barn.

### Hovedfunksjoner

- 🤖 Intelligent Dialog: Barnevennlig samtaleinteraksjon basert på Groks naturlige språkforståelse
- 📚 Utdanningsmodul:
  - Språklæring (uttalekorrigering, grammatikkveiledning)
  - Matematikkspill (tilpasset vanskelighetsgrad)
  - Kunnskapsquiz (relatert til norsk kultur)
- 🎮 Underholdningsmodul:
  - Interaktiv historiegenerering
  - Morsomme gåter og logikkspill

## Teknisk Stack

### Backend
- Rammeverk: FastAPI
- Database: PostgreSQL
- AI-motor: Grok
- Oppgavekø: Celery

### Frontend
- Rammeverk: React
- Tilstandshåndtering: Redux/React Context
- UI-rammeverk: Tailwind CSS
- HTTP-klient: Axios

## Systemkrav

- Conda
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

## Installasjonsveiledning

### 1. Konfigurere Conda-miljø

1. Klon repository 


Miljø:
bash
Opprett conda-miljø
conda create -n kids python=3.8
conda activate kids
Installer grunnleggende avhengigheter
conda install -c conda-forge fastapi uvicorn sqlalchemy psycopg2 python-dotenv pydantic celery
npm install react-router-dom @types/react-router-do
eller bruk environment.yml-fil for å opprette miljø
conda env create -f environment.yml
conda activate children-ai

cd backend
pip install -r requirements.txt
bash
cd frontend
npm install
bash
cp .env.example .env
Rediger .env-filen, konfigurer nødvendige miljøvariabler
bash
Backend
cd backend
uvicorn main:app --reload
Frontend
cd frontend
npm start
yaml
name: children-ai
channels:
conda-forge
defaults
dependencies:
python=3.8
fastapi=0.68.0
uvicorn=0.15.0
sqlalchemy=1.4.23
psycopg2=2.9.1
python-dotenv=0.19.0
pydantic=1.8.2
celery=5.1.2
pip
pip:
python-multipart
python-jose[cryptography]
passlib[bcrypt]


barn-ai-assistant/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── core/
│ │ ├── models/
│ │ └── services/
│ ├── tests/
│ └── main.py
├── frontend/
│ ├── node_modules/
│ ├── public/
│ │ └── index.html
│ ├── src/
│ │ ���─ components/
│ │ │ └── Navbar.js
│ │ ├── pages/
│ │ │ ├── Home.js
│ │ │ ├── Education.js
│ │ │ └── Entertainment.js
│ │ ├── App.js
│ │ ├── index.js
│ │ └── index.css
│ ├── package.json
│ └── tailwind.config.js
└── README.md


Hovedoppdateringer inkluderer:
Lagt til Conda-miljøkonfigurasjon
Lagt til innhold i environment.yml-filen
Oppdaterer installasjonsveiledningen, legger til Conda-relaterte steg
Legger til Conda i systemkrav
Legger til environment.yml-filen i prosjektstrukturen
Du må også opprette environment.yml-filen i prosjektets rotkatalog, med innhold som vist ovenfor. Bruk Conda-miljø for bedre prosjektavhengighetshåndtering, unngå pakkekonflikter og lettere kopiere utviklingsmiljøer på forskjellige maskiner.

## Utviklingsveiledning

1. Sørg for at alle nødvendige avhengigheter er installert
2. Følg prosjektets kodekonvensjoner og arkitekturdesign
3. Test koden før du committer
4. Behold koden vedlikeholdbar og lesbar

## Bidragsveiledning

1. Fork prosjektet
2. Opprett en funksjonsgren (`git checkout -b feature/AmazingFeature`)
3. Commit endringer (`git commit -m 'Add some AmazingFeature'`)
4. Push til gren (`git push origin feature/AmazingFeature`)
5. Opprett en Pull Request

## 件���构说明

### 前端文件 (Frontend)

#### 核心文件
- `frontend/public/index.html`
  - 主HTML文件
  - 设置挪威语言标记 (lang="no")
  - 配置viewport和meta信息
  - 设置应用标题和描述

- `frontend/src/index.js`
  - React应用入口文件
  - 配置React根组件渲染
  - 引入全局样式

- `frontend/src/index.css`
  - 全局样式文件
  - 配置Tailwind CSS基础样式
  - 自定义全局样式定义

- `frontend/src/App.js`
  - 应用主组件
  - 配置路由系统
  - 整合导航栏和页面组件

#### 组件文件
- `frontend/src/components/Navbar.js`
  - 导航栏组件
  - 提供挪威语导航链接
  - 包含教育模块和娱乐模块入口

#### 页面文件
- `frontend/src/pages/Home.js`
  - 首页组件
  - 展示欢迎信息
  - 提供教育和娱乐模块概览
  - 使用挪威语展示内容

- `frontend/src/pages/Education.js`
  - 教育模块页面
  - 包含三个主要学习区域：
    - 语言学习 (Språklæring)
    - 数学游戏 (Matematikkspill)
    - 知识问答 (Kunnskapsquiz)
  - 每个区域都有详细的功能说明和开始按钮

- `frontend/src/pages/Entertainment.js`
  - 娱乐模块页面
  - 包含两个主要功能区：
    - 互动故事 (Interaktive Historier)
    - 智力游戏 (Hjernetrim)
  - 提供详细的功描述���交互按钮

#### 配置文件
- `frontend/package.json`
  - 项目依赖配置
  - 定义项目脚本
  - 配置开发工具

- `frontend/tailwind.config.js`
  - Tailwind CSS配置
  - 定义样式内容范围
  - 自定义主题设置

### 后端文件 (Backend)

#### 核心文件
- `backend/main.py`
  - FastAPI应用入口
  - CORS配置
  - 路由注册

- `backend/requirements.txt`
  - 后端依赖清单
  - 指定依赖版本
  - 包含所有必要的Python包

#### 配置文件
- `backend/.env`
  - 环境变量配置
  - 数据库连接信息
  - API密钥和其他敏感信息

#### 数据库相关
- `backend/app/core/database.py`
  - 数据库连接配置
  - Session管理
  - 数据库工具函数

#### API和模型
- `backend/app/api/chat.py`
  - 聊天功能API实现
  - 消息处理逻辑
  - 与Grok API交互

- `backend/app/models/user.py`
  - 用户模型定义
  - 数据库表结构
  - 用户相关字段定义

## 开发指南

### 前端开发
1. 确保Node.js环境已安装
2. 安装依赖：`npm install`
3. 启动开发服务器：`npm start`
4. 访问 `http://localhost:3000` 查看应用

### 后端开发
1. 激活Conda环境：`conda activate barn-ai`
2. 安装依赖：`pip install -r requirements.txt`
npm install react-router-dom @types/react-router-do
3. 启动FastAPI��务器：`uvicorn main:app --reload`
4. 访问 `http://localhost:8000/docs` 查看API文档

## 环境安装指南

### 1. 前端环境配置

### 教育模块功能说明

#### 1. 数学游戏模块 (Matematikkspill)

#### 1.1 功能概述
- 分年级教学（1-3年级）
- 自定义题目数量（1-100题）
- 实时评分系统
- 即时反馈机制
- 进度追踪
- 错误分析

#### 1.2 年级划分及内容
##### 1年级 (1. klasse)
- **数值范围**: 1-20
- **运算类型**: 
  - 加法 (Addisjon)
  - 减法 (Subtraksjon)
- **题目类型**:
  - 基础运算 (Grunnleggende regning)
  - 简单应用题 (Enkle tekstoppgaver)
  - 示例: "Per har 5 epler og får 3 til. Hvor mange epler har Per nå?"

##### 2年级 (2. klasse)
- **数值范围**: 1-100
- **运算类型**:
  - 加法 (Addisjon)
  - 减法 (Subtraksjon)
  - 乘法 (Multiplikasjon)
- **题目类型**:
  - 基础运算
  - 应用题
  - 示例: "Lisa har 3 grupper med 5 baller i hver. Hvor mange baller har hun totalt?"

##### 3年级 (3. klasse)
- **数值范围**: 1-1000
- **运算类型**:
  - 加法 (Addisjon)
  - 减法 (Subtraksjon)
  - 乘法 (Multiplikasjon)
  - 除法 (Divisjon)
- **题目类型**:
  - 基础运算
  - 应用题
  - 几何题 (Geometri)
  - 示例: "Hva er omkretsen av et kvadrat med sider på 6 cm?"

#### 1.3 技术实现

##### 前端实现 (Frontend)
1. **组件构**

### Grok AI 集成

#### 1. 配置
- 在 `.env` 文件中配置 Grok API 密钥和端点
- 创建 GrokClient 类处理与 Grok API 的交互
- 实现错误处理和备用逻辑

#### 2. 数学题目生成
- 使用 Grok 生成适合年级水平的题目
- 支持多种题型：
  - 基础运算
  - 应用题
  - 几何题
- 实现本地备用生成逻辑

#### 3. 答案验证
- 使用 Grok 验证复杂应用题的答案
- 本地验证基础运算答案
- 提供详细的错误分析和反馈

#### 4. 安全考虑
- API 密钥保护
- 请求限制
- 错误处理机制

#### 语音交互功能
- **文字转语音 (TTS)**
  - 自动朗读数学题目
  - 支持挪威语语音
  - 可重复播放问题

- **语音转文字 (STT)**
  - 支持语音输入答案
  - 自动识别数字
  - 挪威语语音识别

- **交互方式**
  - 朗读按钮：朗读当前问题
  - 语音输入按钮：开始/停止语音输入
  - 实时显示识别结果

## 项目开发进度

### 已完成功能

#### 1. 数学游戏模块 (Matematikkspill)
- [x] 基础框架搭建
- [x] 年级选择（1-3年级）
- [x] 题目数量自定义（1-100题）
- [x] 本地题目生成
- [x] Grok API集成
- [x] 答案验证系统
- [x] 语音朗读功能
- [x] 语音输���功能
- [x] 实时评分系统
- [x] 挪威语界面

#### 2. 基础架构
- [x] 前端路由系统
- [x] 后端API框架
- [x] 数据库连接
- [x] CORS配置
- [x] 错误处理机制
- [x] 日志系统

### 待开发功能

#### 1. 语言学习模块 (Språklæring)
- [ ] 拼音纠正功能
- [ ] 语法练习系统
- [ ] 词汇学习功能
- [ ] 语音识别评分
- [ ] 个性化学习路径

#### 2. 知识问答模块 (Kunnskapsquiz)
- [ ] 挪威文化题库
- [ ] 自然知识题库
- [ ] 科学探索题库
- [ ] 难度自适应系统
- [ ] 学习进度追踪

#### 3. 娱乐模块 (Underholdning)
- [ ] 互动故事生成
- [ ] 智力游戏系统
- [ ] 记忆力训练
- [ ] 创意写作辅助
- [ ] 游戏化学习元素

### 系统优化计划
- [ ] 用户认证系统
- [ ] 学习数据分析
- [ ] 性能优化
- [ ] 移动端适配
- [ ] 离线模式支持

### 已知问题
1. 语音识别准确度需要提升
2. Grok API偶尔响应较慢
3. 数学题目难度分布需要优化
4. 界面交互体验可以改进

### 近期开发计划

#### 第一阶段（优先级高）
1. 完善数学游戏模块
   - 添加更多题型
   - 优化难度算法
   - 改进反馈机制
   - 添加可视化解答

2. 开发语言学习基础功能
   - 实现基础词汇练习
   - 添加简单句训练
   - 集成发音评估
   - 建立学习进度跟踪

#### 第二阶段（优先级中）
1. 知识问答模块开发
   - 建立基础题库
   - 实现分类系统
   - 添加图片支持
   - 开发评分机制

2. 系统功能优化
   - 实现用户配置
   - 添加学习报告
   - 优化缓存策略
   - 改进错误处理

#### 第三阶段（优先级低）
1. 娱乐模块开发
   - 故事生成系统
   - 游戏化元素
   - 互动练习
   - 奖励机制

2. 高级功能实现
   - AI辅导功能
   - 个性化推荐
   - 社交学习功能
   - 家长监控界面

### 技术债务
1. 需要重构的部分
   - 状态管理优化
   - API响应缓存
   - 组件结构优化
   - 错误处理统一

2. 需要补充的文档
   - API文档完善
   - 组件使用说明
   - 部署指南
   - 测试用例

### 下一步开发重点
1. 完善数学模块的语音交互
2. 优化题目生成算法
3. 添加更多的反馈动画
4. 实现学习进度保存
5. 开发语言学习模块基础功能

## 版本更新记录

### v0.3.0 (2024-11-30)
#### 新特性
- 添加了完整的日志系统
  - 支持日志文件轮转
  - 可配置的日志级别
  - 详细的调试信息记录
- 改进了配置管理
  - 统一使用 .env 配置
  - 支持配置验证
  - 移除硬编码配置

#### 依��更新
- FastAPI 升级到 0.100.0+
- Pydantic 升级到 2.0.0+
- SQLAlchemy 升级到 1.4.41+
- 添加 pydantic-settings 支持

#### 技术栈
- **后端**
  - FastAPI 0.100.0+
  - SQLAlchemy 1.4.41+
  - Pydantic 2.0.0+
  - Python 3.8+

- **前端**
  - React 17+
  - TailwindCSS 2.2+
  - TypeScript 4.4+

#### 系统要求
- Python 3.8 或更高版本
- Node.js 14 或更高版本
- PostgreSQL 12 或更高版本

#### 配置说明
必需的环境变量：
```plaintext
# API Configuration
GROK_API_KEY=your_api_key
GROK_API_BASE=https://api.x.ai/v1/chat/completions

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/dbname

# CORS Settings
CORS_ORIGINS=http://localhost:3000

# Logging Configuration
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

#### 已知问题修复
- FastAPI 和 Pydantic 版本兼容性问题
- 日志配置不灵活的问题
- 配置管理混乱的问题
- 依赖版本过时的问题
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

### 2024-12-03 功能更新

#### 新增功能
- **应用题解释系统**
  - 核心数学概念讲解
  - 详细解题步骤说明
  - 针对性解题技巧
  - 相似题目示例

- **知识点展示优化**
  - 结构化的解释内容
  - 清晰的视层次
  - 交互式内容展示
  - 条件渲染逻辑

#### 技术改进
- 改进了数据类型处理
- 优化了条件渲染逻辑
- 添加了错误处理机制
- 改进了用户界面交互

## 版本更新

### 2024-12-08 版本
- **认证系统完善**
  - 完整的用户登录功能
  - 安全的令牌管理
  - 统一的错误处理

- **配置系统优化**
  - 环境变量配置
  - CORS 安全配置
  - 开发环境示例

- **技术栈更新**
  - FastAPI 0.100.0+
  - React 18.2.0+
  - SQLAlchemy 1.4.41+
  - JWT 认证

- **部署说明**
  ```bash
  # 后端启动
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # 前端启动
  npm start
  ```

- **环境要求**
  - Python 3.8+
  - Node.js 14+
  - PostgreSQL 12+
  - 环境变量配置

- **数学应用题生成优化**
  - 支持多种数字类型（整数、小数、分数）
  - 年龄分级的题目生成系统
  - 完善的验证规则机制
  - 优化的提示词系统

- **题目生成规则**
  ```python
  # 规则示例
  number_rules = [
      "Numbers can be:",
      "- Whole numbers between 0 and 1000",
      "- Decimals between 0.00 and 1000.00 (up to 2 decimal places)",
      "- Simple fractions (like 1/2, 1/3, 1/4, 2/3, 3/4)"
  ]
  ```

- **规则系统优化**
  - 支持自定义规则输入
  - 灵活的规则组合机制
  - 实时规则验证
  - 示例：
    ```javascript
    // 规则处理示例
    const rulesArray = customRules
        ? customRules.split('\n').filter(rule => rule.trim())
        : null;
    ```

- **用户界面改进**
  - 添加规则输入界面
  - 优化规则显示格式
  - 提供规则输入指导
  - 支持规则实时预览

