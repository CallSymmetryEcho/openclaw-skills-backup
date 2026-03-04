# 小红书扫码登录技能 - 完整工作流

## 功能概述
实现小红书扫码登录的完整工作流：
1. 获取登录二维码
2. 发送二维码图片到聊天框
3. 用户扫码登录
4. 自动检测登录状态
5. 保存Cookie供后续使用

## 技术实现

### 核心脚本
- `tools/xiaohongshu_qrcode.py` - 扫码登录主逻辑
- `tools/xiaohongshu_qrcode.sh` - 命令行封装
- `tools/run_qrcode_login.py` - OpenClaw集成脚本

### 工作流程

#### 步骤1: 获取二维码
```bash
# 在OpenClaw中执行
exec(command="cd ~/.openclaw/workspace/skills/xiaohongshu-login && python3 ./tools/xiaohongshu_qrcode.py qrcode")
```

#### 步骤2: 发送二维码到聊天框
```python
# 在OpenClaw中执行（需要二维码文件路径）
message(action="send", media="/path/to/qrcode.png", caption="请扫描二维码登录小红书")
```

#### 步骤3: 用户扫码
- 用户使用小红书APP扫码
- 在APP中确认登录

#### 步骤4: 检测登录状态
```bash
# 在OpenClaw中执行
exec(command="cd ~/.openclaw/workspace/skills/xiaohongshu-login && python3 ./tools/xiaohongshu_qrcode.py complete")
```

## OpenClaw集成示例

### 完整工作流脚本
```python
# 在OpenClaw会话中执行以下步骤：

# 1. 获取二维码
qrcode_result = exec(command="cd ~/.openclaw/workspace/skills/xiaohongshu-login && python3 ./tools/xiaohongshu_qrcode.py qrcode --json")

# 2. 解析结果，获取二维码路径
import json
result = json.loads(qrcode_result)
qrcode_path = result['qrcode_path']

# 3. 发送二维码到聊天框
message(action="send", media=qrcode_path, caption="请扫描二维码登录小红书")

# 4. 提示用户扫码
print("请使用小红书APP扫描上方二维码")

# 5. 等待用户扫码（可以设置定时器或手动触发）
# 6. 检测登录状态
login_result = exec(command="cd ~/.openclaw/workspace/skills/xiaohongshu-login && python3 ./tools/xiaohongshu_qrcode.py complete --json")

# 7. 显示结果
print(login_result)
```

### 简化版本（手动步骤）
```bash
# 步骤1: 获取二维码
exec(command="cd ~/.openclaw/workspace/skills/xiaohongshu-login && ./tools/xiaohongshu_qrcode.sh qrcode")

# 步骤2: 发送二维码（需要手动获取文件路径）
# 查看生成的二维码文件
exec(command="ls -la ~/.openclaw/workspace/config/qrcodes/")

# 步骤3: 发送图片到聊天框（示例）
message(action="send", media="~/.openclaw/workspace/config/qrcodes/xiaohongshu_qrcode_20260303_204500.png", caption="请扫描二维码登录小红书")

# 步骤4: 用户扫码后检测登录
exec(command="cd ~/.openclaw/workspace/skills/xiaohongshu-login && ./tools/xiaohongshu_qrcode.sh complete")
```

## 文件位置

### 配置文件
- `~/.openclaw/workspace/config/xiaohongshu_cookies.json` - Cookie存储
- `~/.openclaw/workspace/config/qrcodes/` - 二维码图片目录

### 二维码文件命名
- `xiaohongshu_qrcode_YYYYMMDD_HHMMSS.png` - 二维码截图
- `xiaohongshu_full_YYYYMMDD_HHMMSS.png` - 完整页面截图
- `xiaohongshu_home_YYYYMMDD_HHMMSS.png` - 主页截图

## 错误处理

### 常见问题
1. **二维码未出现**: 小红书登录页面可能更新，需要调整选择器
2. **登录超时**: 默认等待300秒，可调整timeout参数
3. **网络问题**: 确保可以访问小红书网站
4. **浏览器问题**: 确保Playwright和Chromium已安装

### 调试命令
```bash
# 测试小红书访问
./tools/xiaohongshu_qrcode.sh test

# 查看日志
tail -f ~/.openclaw/workspace/config/qrcodes/*.log

# 清理旧文件
rm -f ~/.openclaw/workspace/config/qrcodes/*.png
```

## 安全注意事项

1. **Cookie安全**: Cookie文件包含登录凭证，请妥善保管
2. **会话管理**: 登录会话有有效期，过期需要重新扫码
3. **隐私保护**: 二维码图片可能包含敏感信息，使用后建议删除

## 更新维护

### 选择器更新
如果小红书页面结构变化，需要更新以下选择器：
- 登录按钮选择器
- 二维码元素选择器
- 登录成功检测选择器

### 版本兼容
- Playwright版本: 1.58.0+
- Python版本: 3.8+
- 浏览器: Chromium 120+

## 使用建议

### 首次使用
1. 运行依赖安装: `./tools/install_deps.sh all`
2. 测试环境: `./tools/xiaohongshu_qrcode.sh test`
3. 获取二维码: `./tools/xiaohongshu_qrcode.sh qrcode`
4. 发送二维码到聊天框
5. 用户扫码后检测登录

### 日常使用
- 使用保存的Cookie进行浏览和搜索
- Cookie过期时重新扫码登录
- 定期清理旧的二维码图片

## 扩展功能

### 计划功能
1. 自动重试机制
2. 多账号支持
3. 登录状态监控
4. 定时刷新Cookie

### 集成选项
1. 与现有Cookie方案集成
2. 支持命令行参数配置
3. 提供API接口
4. 添加Webhook通知