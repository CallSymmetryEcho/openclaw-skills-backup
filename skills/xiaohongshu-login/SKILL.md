---
name: xiaohongshu-login
description: 小红书自动化登录和内容管理。使用Playwright进行浏览器自动化，支持登录、内容浏览、发布等操作。
---

# 小红书登录技能

## 概述

使用Playwright自动化工具实现小红书的登录和基本操作。支持：
- 自动化登录（账号密码）
- 验证码处理（需要用户协助）
- 内容浏览和截图
- 发布内容（可选）

## 依赖

- Playwright 1.58.2+
- Chromium浏览器
- 小红书账号和密码

## 配置文件

在`~/.openclaw/workspace/config/xiaohongshu_account.json`中存储账号信息：

```json
{
  "username": "your_username",
  "password": "your_password",
  "login_type": "phone|email",
  "remember_me": true
}
```

## 使用方法

### 1. 设置账号信息
```bash
./tools/xiaohongshu_login.sh setup
```

### 2. 测试登录
```bash
./tools/xiaohongshu_login.sh test
```

### 3. 登录并截图
```bash
./tools/xiaohongshu_login.sh login
```

### 4. 浏览主页
```bash
./tools/xiaohongshu_login.sh browse
```

### 5. 搜索内容
```bash
./tools/xiaohongshu_login.sh search "关键词"
```

## 脚本说明

### `xiaohongshu_login.py`
主脚本，包含完整的登录逻辑：
- 处理登录页面重定向
- 输入账号密码
- 处理验证码（如果需要）
- 保存登录状态（cookies）
- 错误处理和重试

### `xiaohongshu_login.sh`
命令行包装脚本，提供简单接口。

## Cookie方案（推荐）

由于小红书只支持手机号验证码登录，推荐使用Cookie方案：

### Cookie获取方法

#### 方法1: 手动提取（推荐）
```bash
./tools/xiaohongshu_cookie.sh extract
```
1. 脚本打开浏览器窗口
2. 手动完成小红书登录（手机号+验证码）
3. 脚本自动保存Cookie

#### 方法2: 从浏览器导出
1. 在Chrome/Firefox中登录小红书
2. 使用浏览器开发者工具导出Cookie
3. 保存到导出文件
4. 运行导入命令

#### 方法3: 使用已有Cookie文件
直接复制Cookie JSON文件到配置目录

### Cookie管理工具
```bash
# 查看指南
./tools/xiaohongshu_cookie.sh guide

# 手动提取Cookie
./tools/xiaohongshu_cookie.sh extract

# 测试Cookie
./tools/xiaohongshu_cookie.sh test

# 使用Cookie浏览
./tools/xiaohongshu_cookie.sh browse

# 使用Cookie搜索
./tools/xiaohongshu_cookie.sh search "关键词"
```

## 验证码处理（传统登录方案）

如果使用传统登录方案遇到验证码，脚本会：
1. 暂停并显示验证码图片
2. 等待用户输入验证码
3. 继续登录流程

## 安全注意事项

1. 账号密码存储在本地配置文件中
2. 建议使用应用专用密码（如果支持）
3. 定期更新密码
4. 不要分享配置文件

## 故障排除

### 常见问题
1. **登录失败**：检查账号密码，确认网络连接
2. **验证码无法识别**：需要手动输入
3. **页面加载超时**：增加等待时间或检查网络
4. **Playwright错误**：更新Playwright版本

### 调试模式
```bash
DEBUG=1 ./tools/xiaohongshu_login.sh login
```

## 扩展功能

未来可以扩展的功能：
- 自动发布内容
- 内容分析和统计
- 关注/取消关注
- 消息管理

## 更新日志

- 2026-03-03: 初始版本创建
- 支持基本登录功能
- 配置文件管理
- 验证码处理框架