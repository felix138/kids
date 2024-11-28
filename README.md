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
│ │ ├── components/
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

## 文件结构说明

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
  - 提供详细的功能描述和交互按钮

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
3. 启动FastAPI服务器：`uvicorn main:app --reload`
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
- [x] 语音输入功能
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
   - 添加简单句型训练
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

## 开发日志

### 2024-11-27 更新 (下午)

#### 1. 修复问题
- **答案验证系统修复**
  - 修复了正确答案被判定为错误的问题
  - 改进了挪威语数字格式处理（支持逗号小数点）
  - 优化了答案解析逻辑
  - 修复了grade/age字段不一致问题

- **API响应修复**
  - 修复了数学解释API的422错误
  - 统一使用age替代grade字段
  - 改进了请求参数验证
  - 完善了错误处理机制

- **数据模型优化**
  - 更新了MathProblem模型定义
  - 添加了ExplanationRequest模型
  - 统一了年龄相关字段
  - 改进了数据验证逻辑

#### 2. 功能改进
- **答案处理优化**
  - 增强了数字格式解析能力
  - 支持多种答案格式（整数、小数、分数）
  - 改进了答案比较逻辑
  - 添加了详细的解答说明

- **错误处理增强**
  - 添加了更详细的日志记录
  - 改进了错误提示信息
  - 优化了异常处理流程
  - 增加了备用逻辑

#### 3. 代码重构
- **后端优化**
  - 重构了grok_client中的解析逻辑
  - 统一了API响应格式
  - 改进了缓存机制
  - 优化了代码结构

- **前端改进**
  - 更新了答案提交逻辑
  - 改进了错误提示显示
  - 优化了用户体验
  - 完善了状态管理

### 已知问题
1. ~~答案验证bug~~ (已修复)
2. ~~数字格式问题~~ (已修复)
3. ~~API响应错误~~ (已修复)
4. ~~字段不一致问题~~ (已修复)

### 下一步计划
1. 继续完善语言学习模块
2. 添加更多交互动画
3. 优化题目生成算法
4. 添加学习进度追踪
5. 实现个性化推荐

### 2024-11-27 更新 (晚间补充3)

#### 1. 数学应用题优化
- **题型扩展**
  - 添加购物计算题
  - 添加分享分配题
  - 添加时间计算题
  - 添加测量计算题

- **题目生成改进**
  - 根据年龄调整题型
  - 优化数字范围
  - 添加题目去重机制
  - 改进答案验证

#### 2. 题目模板系统
- **购物题型**
  - 商品购买计算
  - 余额计算
  - 数量计算

- **分享题型**
  - 平均分配
  - 组合分配
  - 数量分配

- **时间题型**
  - 时间间隔计算
  - 起止时间计算
  - 持续时间计算

- **测量题型**
  - 面积计算
  - 长度分割
  - 数量计算

#### 3. 本地化改进
- **挪威语支持**
  - 添加挪威语名字库
  - 本地化物品名称
  - 本地化地点名称
  - 完善反馈信息

#### 4. 系统优化
- **缓存管理**
  - 改进问题缓存
  - 优化ID管理
  - 添加哈希去重
  - 完善清理机制

### 已知问题
1. ~~答案验证bug~~ (已修复)
2. ~~数字格式问题~~ (已修复)
3. ~~API响应错误~~ (已修复)
4. ~~字段不一致问题~~ (已修复)
5. ~~缓存同步问题~~ (已修复)
6. ~~语音识别显示问题~~ (已修复)
7. ~~应用题生成问题~~ (已修复)

### 下一步计划
1. 继续完善语言学习模块
2. 添加更多交互动画
3. 优化题目生成算法
4. 添加学习进度追踪
5. 实现个性化推荐
6. 改进性能监控
7. 优化用户体验
8. 扩展语音识别功能
9. 完善多语言支持
10. 添加更多应用题类型

## 环境配置说明

### 1. 环境变量设置
1. 复制环境变量示例文件：
```bash
cp backend/.env.example backend/.env
```

2. 更新环境变量：
   - 在 backend/.env 中设置你的 GROK_API_KEY
   - 配置其他必要的环境变量

3. 环境变量说明：
   - GROK_API_KEY: Grok API密钥（必需）
   - GROK_API_BASE: Grok API基础URL
   - DATABASE_URL: 数据库连接URL
   - CORS_ORIGINS: CORS允许的源

### 2. 开发环境准备
1. 安装依赖：
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

2. 启动服务：
```bash
# 启动后端
cd backend
uvicorn main:app --reload

# 启动前端
cd frontend
npm start
```

### 3. 注意事项
- 确保 .env 文件不被提交到Git
- 保持 .env.example 文件更新
- 定期检查环境变量配置
- 注意API密钥的安全性

## 环境配置

1. 复制环境变量示例文件：
```bash
cp backend/.env
```