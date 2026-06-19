"""
命令行版本的提醒器
"""
import json
import os
import time
import sys
from reminder import ReminderManager


class CLIReminder:
    """命令行提醒器"""
    
    def __init__(self):
        self.config = self.load_config()
        self.reminder = ReminderManager(
            water_interval=self.config["water_interval_minutes"],
            eye_interval=self.config["eye_rest_interval_minutes"]
        )
        self.reminder.on_water_reminder = self.on_reminder
        self.reminder.on_eye_reminder = self.on_reminder
    
    def load_config(self):
        """加载配置"""
        if os.path.exists("config.json"):
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "water_interval_minutes": 30,
            "eye_rest_interval_minutes": 45,
            "show_duration_seconds": 5,
            "start_on_launch": True,
            "notifications_enabled": True
        }
    
    def on_reminder(self):
        """提醒回调"""
        pass
    
    def run(self):
        """运行提醒器"""
        print("=" * 50)
        print("🌟 小琪琪 - 水和眼睛放松提醒器")
        print("=" * 50)
        print(f"喝水提醒间隔: {self.config['water_interval_minutes']} 分钟")
        print(f"眼睛放松提醒间隔: {self.config['eye_rest_interval_minutes']} 分钟")
        print("\n按 Ctrl+C 停止提醒器\n")
        print("=" * 50)
        
        self.reminder.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n停止提醒器...")
            self.reminder.stop()
            print("再见！👋")
            sys.exit(0)


def main():
    app = CLIReminder()
    app.run()


if __name__ == "__main__":
    main()
