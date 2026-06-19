# 小琪琪 - 水和眼睛放松提醒器 🌟

一个简单实用的桌面提醒应用，帮助你养成健康习惯：
- 💧 定期提醒喝水
- 👀 定期提醒放松眼睛
- 🔔 友好的提醒通知
- ⏰ 可自定义提醒间隔

## 功能特性

- **智能提醒**：定期交替提醒喝水和放松眼睛
- **灵活配置**：可自定义提醒频率
- **系统通知**：跨平台通知支持
- **简洁界面**：易于使用的用户界面

## 安装

```bash
git clone https://github.com/yaoxiaojing1982/xiaoqiqi.git
cd xiaoqiqi
pip install -r requirements.txt
```

## 使用

### 方式1：运行GUI应用
```bash
python main.py
```

### 方式2：命令行运行
```bash
python reminder_cli.py
```

## 配置

编辑 `config.json` 配置提醒间隔：

```json
{
  "water_interval_minutes": 30,
  "eye_rest_interval_minutes": 45,
  "show_duration_seconds": 5
}
```

## 项目结构

```
xiaoqiqi/
├── main.py                 # GUI 应用入口
├── reminder_cli.py         # 命令行应用入口
├── reminder.py             # 核心提醒逻辑
├── notifications.py        # 通知处理
├── config.json            # 配置文件
└── requirements.txt       # 依赖项
```

## 技术栈

- Python 3.8+
- tkinter（GUI）
- plyer（跨平台通知）

## 许可证

MIT
