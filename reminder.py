"""
核心提醒逻辑
"""
import threading
import time
from datetime import datetime
from notifications import get_notifier


class ReminderManager:
    """提醒管理器 - 处理定时提醒逻辑"""
    
    def __init__(self, water_interval=30, eye_interval=45):
        """
        初始化提醒管理器
        
        Args:
            water_interval: 喝水提醒间隔（分钟）
            eye_interval: 眼睛放松提醒间隔（分钟）
        """
        self.water_interval = water_interval * 60  # 转换为秒
        self.eye_interval = eye_interval * 60      # 转换为秒
        self.notifier = get_notifier()
        
        self.is_running = False
        self.thread = None
        
        self.last_water_time = 0
        self.last_eye_time = 0
        
        # 回调函数
        self.on_water_reminder = None
        self.on_eye_reminder = None
        self.on_status_change = None
    
    def start(self):
        """启动提醒器"""
        if self.is_running:
            print("提醒器已在运行")
            return
        
        self.is_running = True
        self.last_water_time = time.time()
        self.last_eye_time = time.time()
        
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        self.notifier.notify_started()
        self._trigger_status_change("已启动")
        print(f"✅ 提醒器已启动 - 喝水间隔: {self.water_interval//60}分钟, 眼睛放松间隔: {self.eye_interval//60}分钟")
    
    def stop(self):
        """停止提醒器"""
        if not self.is_running:
            print("提醒器未运行")
            return
        
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        
        self.notifier.notify_stopped()
        self._trigger_status_change("已停止")
        print("❌ 提醒器已停止")
    
    def _run_loop(self):
        """主循环 - 检查是否需要发送提醒"""
        while self.is_running:
            current_time = time.time()
            
            # 检查喝水提醒
            if current_time - self.last_water_time >= self.water_interval:
                self._trigger_water_reminder()
                self.last_water_time = current_time
            
            # 检查眼睛放松提醒
            if current_time - self.last_eye_time >= self.eye_interval:
                self._trigger_eye_reminder()
                self.last_eye_time = current_time
            
            # 每秒检查一次
            time.sleep(1)
    
    def _trigger_water_reminder(self):
        """触发喝水提醒"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] 💧 喝水提醒")
        self.notifier.notify_water()
        if self.on_water_reminder:
            self.on_water_reminder()
    
    def _trigger_eye_reminder(self):
        """触发眼睛放松提醒"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] 👀 眼睛放松提醒")
        self.notifier.notify_eye_rest()
        if self.on_eye_reminder:
            self.on_eye_reminder()
    
    def _trigger_status_change(self, status):
        """触发状态变化回调"""
        if self.on_status_change:
            self.on_status_change(status)
    
    def update_intervals(self, water_interval, eye_interval):
        """更新提醒间隔"""
        self.water_interval = water_interval * 60
        self.eye_interval = eye_interval * 60
        print(f"⚙️  已更新配置 - 喝水间隔: {water_interval}分钟, 眼睛放松间隔: {eye_interval}分钟")
    
    def get_status(self):
        """获取当前状态"""
        if self.is_running:
            elapsed_water = time.time() - self.last_water_time
            elapsed_eye = time.time() - self.last_eye_time
            return {
                "status": "运行中",
                "next_water_in": max(0, int((self.water_interval - elapsed_water) / 60)),
                "next_eye_in": max(0, int((self.eye_interval - elapsed_eye) / 60))
            }
        else:
            return {"status": "已停止"}
