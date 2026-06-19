"""
图形界面主应用
"""
import tkinter as tk
from tkinter import ttk
import json
import os
from reminder import ReminderManager


class ReminderApp:
    """提醒器GUI应用"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("小琪琪 - 水和眼睛放松提醒器")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 加载配置
        self.config = self.load_config()
        
        # 初始化提醒管理器
        self.reminder = ReminderManager(
            water_interval=self.config["water_interval_minutes"],
            eye_interval=self.config["eye_rest_interval_minutes"]
        )
        self.reminder.on_water_reminder = self.on_water_reminder
        self.reminder.on_eye_reminder = self.on_eye_reminder
        self.reminder.on_status_change = self.on_status_change
        
        # 创建GUI
        self.create_widgets()
        
        # 如果配置启用自动启动，则启动提醒器
        if self.config["start_on_launch"]:
            self.root.after(500, self.start_reminder)
    
    def load_config(self):
        """加载配置文件"""
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
    
    def save_config(self):
        """保存配置文件"""
        config = {
            "water_interval_minutes": self.water_interval_var.get(),
            "eye_rest_interval_minutes": self.eye_interval_var.get(),
            "show_duration_seconds": self.config["show_duration_seconds"],
            "start_on_launch": self.config["start_on_launch"],
            "notifications_enabled": self.config["notifications_enabled"]
        }
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        self.config = config
    
    def create_widgets(self):
        """创建UI组件"""
        # 标题
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(title_frame, text="小琪琪提醒器", font=("Arial", 24, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="保持健康的好习惯 💪", font=("Arial", 10))
        subtitle_label.pack()
        
        # 状态显示
        self.status_frame = ttk.LabelFrame(self.root, text="状态", padding=15)
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ttk.Label(self.status_frame, text="已停止", font=("Arial", 12, "bold"), foreground="red")
        self.status_label.pack()
        
        self.next_reminder_label = ttk.Label(self.status_frame, text="", font=("Arial", 10))
        self.next_reminder_label.pack()
        
        # 配置区域
        config_frame = ttk.LabelFrame(self.root, text="配置", padding=15)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        # 喝水间隔
        water_frame = ttk.Frame(config_frame)
        water_frame.pack(fill="x", pady=8)
        ttk.Label(water_frame, text="喝水提醒间隔 (分钟):").pack(side="left")
        self.water_interval_var = tk.IntVar(value=self.config["water_interval_minutes"])
        water_spin = ttk.Spinbox(water_frame, from_=5, to=120, textvariable=self.water_interval_var, width=10)
        water_spin.pack(side="right")
        
        # 眼睛放松间隔
        eye_frame = ttk.Frame(config_frame)
        eye_frame.pack(fill="x", pady=8)
        ttk.Label(eye_frame, text="眼睛放松提醒间隔 (分钟):").pack(side="left")
        self.eye_interval_var = tk.IntVar(value=self.config["eye_rest_interval_minutes"])
        eye_spin = ttk.Spinbox(eye_frame, from_=5, to=120, textvariable=self.eye_interval_var, width=10)
        eye_spin.pack(side="right")
        
        # 按钮区域
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="▶ 启动", command=self.start_reminder, width=12)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹ 停止", command=self.stop_reminder, width=12, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        self.apply_btn = ttk.Button(button_frame, text="💾 保存配置", command=self.apply_config, width=12)
        self.apply_btn.pack(side="left", padx=5)
        
        # 更新状态显示
        self.update_status_display()
    
    def start_reminder(self):
        """启动提醒器"""
        self.reminder.update_intervals(self.water_interval_var.get(), self.eye_interval_var.get())
        self.reminder.start()
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
    
    def stop_reminder(self):
        """停止提醒器"""
        self.reminder.stop()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
    
    def apply_config(self):
        """应用配置"""
        self.save_config()
        if self.reminder.is_running:
            self.reminder.update_intervals(self.water_interval_var.get(), self.eye_interval_var.get())
        self.update_status_display()
    
    def on_water_reminder(self):
        """喝水提醒回调"""
        self.update_status_display()
    
    def on_eye_reminder(self):
        """眼睛放松提醒回调"""
        self.update_status_display()
    
    def on_status_change(self, status):
        """状态变化回调"""
        self.update_status_display()
    
    def update_status_display(self):
        """更新状态显示"""
        status_info = self.reminder.get_status()
        
        if status_info["status"] == "运行中":
            self.status_label.config(text="✅ 运行中", foreground="green")
            next_text = f"下次喝水提醒: {status_info['next_water_in']} 分钟后\n下次眼睛放松提醒: {status_info['next_eye_in']} 分钟后"
            self.next_reminder_label.config(text=next_text)
        else:
            self.status_label.config(text="❌ 已停止", foreground="red")
            self.next_reminder_label.config(text="")
        
        # 每秒更新一次状态
        if self.reminder.is_running:
            self.root.after(1000, self.update_status_display)


def main():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
