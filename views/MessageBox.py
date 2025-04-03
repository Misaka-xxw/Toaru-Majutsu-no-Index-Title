from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect

# 🎨 浅色调主题配置
THEME_COLORS = {
    "success": "#e6f7e6",  # 浅绿
    "error": "#ffebee",  # 浅红
    "info": "#e3f2fd",  # 浅蓝
    "warning": "#fff8e1"  # 浅黄
}


class MessageBox(QWidget):
    def __init__(self, message, msg_type='success', duration=2500, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.duration = duration

        # 🎭 动画与透明效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        # 📬 消息内容
        emoji = {
            "success": "✅",
            "error": "❌",
            "info": "ℹ️",
            "warning": "⚠️"
        }.get(msg_type, "")
        misaka_speak = {
            "success": "do，御坂开心地喊道。",
            "error": "do，御坂有些沮丧地说道。",
            "info": "do，御坂认真地说道。",
            "warning": "do，御坂严肃地提醒道。"
        }.get(msg_type, "")
        styled_text = f"<p style='margin:0;font-size: 14px;'>{emoji} {message}</p><p style='margin:0;color: #AAAAAA;font-size: 9px;'>{misaka_speak}</p>"
        self.label = QLabel(styled_text, self)
        self.label.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)

        self.label.setStyleSheet(f"""
            QLabel {{
                color: #333333;
                background-color: {THEME_COLORS[msg_type]};
                border-radius: 12px;
                padding: 10px;
            }}
        """)

        self.adjustSize()
        self.setMaximumWidth(self.width())

        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out.finished.connect(self.close)

        self._position_notification()

        self.show()
        self.fade_in.start()
        QTimer.singleShot(self.duration, self.fade_out.start)

    def _position_notification(self):
        """内部方法，用于定位通知到右下角"""
        app = QApplication.instance()
        if app is not None:
            active_window = app.activeWindow()
            if active_window is not None:
                parent_rect = active_window.rect()
                notif_size = self.sizeHint()
                x = parent_rect.right() - notif_size.width() - 20
                y = parent_rect.bottom() - notif_size.height() - 20
                self.move(x, y)
                return

        # 如果没有父窗口，定位到屏幕右下角
        screen_geometry = app.primaryScreen().availableGeometry()
        notif_size = self.sizeHint()
        x = screen_geometry.right() - notif_size.width() - 20
        y = screen_geometry.bottom() - notif_size.height() - 20
        self.move(x, y)
