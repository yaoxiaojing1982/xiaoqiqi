"""
处理系统通知的模块
"""
import platform
from plyer import notification


class Notifier:
    """系统通知管理器"""
    
    def __init__(self):
        self.app_name = "小琪琪提醒器"
        self.platform = platform.system()
    
    def notify_water(self):
        """发送喝水提醒通知"""
        self._show_notification(
            title="💧 喝水提醒",
            message="该喝水了！补充一下水分，保持身体健康。",
            timeout=5
        )
    
    def notify_eye_rest(self):
        """发送眼睛放松提醒通知"""
        self._show_notification(
            title="👀 眼睛放松提醒",
            message="眼睛该放松一下了！看看远处，眨眨眼睛，保护视力。",
            timeout=5
        )
    
    def notify_started(self):
        """发送启动提醒通知"""
        self._show_notification(
            title="小琪琪已启动",
            message="提醒器已开始工作，祝你健康！",
            timeout=3
        )
    
    def notify_stopped(self):
        """发送停止提醒通知"""
        self._show_notification(
            title="小琪琪已停止",
            message="提醒器已关闭。",
            timeout=3
        )
    
    def _show_notification(self, title, message, timeout=5):
        """显示系统通知"""
        try:
            notification.notify(
                title=title,
                message=message,
                app_name=self.app_name,
                timeout=timeout,
            )
        except Exception as e:
            print(f"通知显示失败: {e}")


class MockNotifier:
    """测试用的虚拟通知器（当通知库不可用时使用）"""
    
    def notify_water(self):
        print("💧 [提醒] 该喝水了！")
    
    def notify_eye_rest(self):
        print("👀 [提醒] 眼睛该放松一下了！")
    
    def notify_started(self):
        print("✅ [提醒] 小琪琪已启动")
    
    def notify_stopped(self):
        print("❌ [提醒] 小琪琪已停止")


def get_notifier():
    """获取合适的通知器"""
    try:
        return Notifier()
    except Exception:
        print("使用虚拟通知器（console输出）")
        return MockNotifier()
