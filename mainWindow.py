import sys

from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QRadioButton, QVBoxLayout,
    QHBoxLayout, QPushButton, QColorDialog, QFileDialog, QButtonGroup, QFrame,
    QGroupBox,QHBoxLayout
)


class CustomColorDialog(QColorDialog):
    """自定义颜色选择器，预设一些喜欢的颜色，并显示颜色名称"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择颜色")
        self.custom_colors = [
            ("魔法", "#00008a"), ("科学", "#8a0000"), ("魔禁", "#3d83bc"), ("超炮", "#ea4729"), ("科方", "#808080"),
            ("偶方", "#dcdcdc")
        ]
        for i, (name, color) in enumerate(self.custom_colors):
            self.setCustomColor(i, QColor(color))
        self.currentColorChanged.connect(self.show_color_name)

    def show_color_name(self, color):
        for name, hex_color in self.custom_colors:
            if color.name().upper() == hex_color.upper():
                self.setWindowTitle(f"选择颜色 - {name}")
                return
        self.setWindowTitle("选择颜色")

    @staticmethod
    def getColor(initial=QColor("#FFFFFF"), parent=None):
        dlg = CustomColorDialog(parent)
        dlg.setCurrentColor(initial)
        if dlg.exec():
            return dlg.currentColor()
        return initial


from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF, QRectF, QTimer
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QMouseEvent

class GradientSlider(QWidget):
    """
    自定义渐变滑条：
      - 显示一个横向渐变条
      - 显示颜色停靠点（指针），左键短按打开调色盘修改颜色，
        左键长按可拖动修改位置，右键点击删除停靠点（至少保留两个）
      - 点击空白区域添加新停靠点（默认颜色取当前渐变处的颜色）
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(50)
        self.setMinimumWidth(300)
        # 初始有两个停靠点（位置, QColor），位置为 0.0 与 1.0
        self.stops = [(0.0, QColor("#0E0C68")), (1.0, QColor("#64B1D5"))]
        self.selected_index = None
        self.dragging = False
        self.long_press_timer = None
        self.press_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        # 绘制渐变背景
        gradient = QLinearGradient(QPointF(rect.topLeft()), QPointF(rect.topRight()))
        for pos, color in self.stops:
            gradient.setColorAt(pos, color)
        painter.fillRect(rect, gradient)
        # 绘制边框
        painter.setPen(Qt.GlobalColor.black)
        painter.drawRect(rect.adjusted(0, 0, -1, -1))
        # 绘制停靠点（指针），绘制为小圆圈
        for i, (pos, color) in enumerate(self.stops):
            x = rect.left() + pos * rect.width()
            y = rect.center().y()
            marker_rect = QRectF(x - 6, y - 6, 12, 12)
            painter.setPen(Qt.GlobalColor.white)
            painter.setBrush(color)
            painter.drawEllipse(marker_rect)

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.position() if hasattr(event, "position") else event.posF()
        clicked_index = self._find_stop_at(pos)
        # 右键点击直接删除（如果停靠点数大于2）
        if event.button() == Qt.MouseButton.RightButton:
            if clicked_index is not None and len(self.stops) > 2:
                self.delete_stop(clicked_index)
            return

        if event.button() == Qt.MouseButton.LeftButton:
            if clicked_index is not None:
                self.selected_index = clicked_index
                self.press_pos = pos
                # 启动长按计时器，300ms后认为开始拖动
                self.long_press_timer = QTimer(self)
                self.long_press_timer.setSingleShot(True)
                self.long_press_timer.timeout.connect(self.start_dragging)
                self.long_press_timer.start(300)
            else:
                # 点击空白区域添加新停靠点
                rel_pos = (pos.x() - self.rect().left()) / self.rect().width()
                new_color = self._color_at(rel_pos)
                self.stops.append((rel_pos, new_color))
                self.stops.sort(key=lambda s: s[0])
                self.update()

    def start_dragging(self):
        # 长按触发拖动
        self.dragging = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.selected_index is not None and self.dragging:
            pos = event.position() if hasattr(event, "position") else event.posF()
            rel_pos = (pos.x() - self.rect().left()) / self.rect().width()
            rel_pos = max(0.0, min(1.0, rel_pos))
            color = self.stops[self.selected_index][1]
            self.stops[self.selected_index] = (rel_pos, color)
            self.stops.sort(key=lambda s: s[0])
            self.selected_index = self._find_stop_at(
                QPointF(self.rect().left() + rel_pos * self.rect().width(), self.rect().center().y()))
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.long_press_timer and self.long_press_timer.isActive():
            # 如果计时器仍在运行，则视为短按，停止计时器并打开调色盘
            self.long_press_timer.stop()
            if self.selected_index is not None:
                new_color = CustomColorDialog.getColor(self.stops[self.selected_index][1], self)
                self.stops[self.selected_index] = (self.stops[self.selected_index][0], new_color)
            self.dragging = False
            self.selected_index = None
            self.update()
        else:
            # 已经在拖动中，结束拖动
            self.dragging = False
            self.selected_index = None

    def _find_stop_at(self, pos: QPointF):
        """查找在 pos 附近的停靠点，返回索引，否则返回 None"""
        rect = self.rect()
        for i, (p, color) in enumerate(self.stops):
            x = rect.left() + p * rect.width()
            y = rect.center().y()
            marker_rect = QRectF(x - 6, y - 6, 12, 12)
            if marker_rect.contains(pos):
                return i
        return None

    def _color_at(self, pos: float) -> QColor:
        """根据 pos (0-1) 计算渐变颜色，线性插值"""
        stops = sorted(self.stops, key=lambda s: s[0])
        if pos <= stops[0][0]:
            return stops[0][1]
        if pos >= stops[-1][0]:
            return stops[-1][1]
        for i in range(1, len(stops)):
            if pos < stops[i][0]:
                p0, c0 = stops[i - 1]
                p1, c1 = stops[i]
                ratio = (pos - p0) / (p1 - p0)
                r = c0.red() + (c1.red() - c0.red()) * ratio
                g = c0.green() + (c1.green() - c0.green()) * ratio
                b = c0.blue() + (c1.blue() - c0.blue()) * ratio
                return QColor(int(r), int(g), int(b))
        return QColor("#FFFFFF")

    def delete_stop(self, index):
        if len(self.stops) > 2:
            del self.stops[index]
            self.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("某系列字体生成")
        self.setGeometry(100, 100, 900, 700)

        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()

        # 文本输入框
        self.label0 = QLabel("文本")
        left_layout.addWidget(self.label0)
        text_layout=QHBoxLayout()
        self.label1 = QLabel("とある")
        self.text_input1 = QLineEdit()
        self.text_input1.setPlaceholderText("魔法")

        self.label2 = QLabel("の")
        self.text_input2 = QLineEdit()
        self.text_input2.setPlaceholderText("禁书目录")

        text_layout.addWidget(self.label1)
        text_layout.addWidget(self.text_input1)
        text_layout.addWidget(self.label2)
        text_layout.addWidget(self.text_input2)
        left_layout.addLayout(text_layout)
        # 背景选项
        self.bg_label = QLabel("背景选项")
        self.bg_group = QButtonGroup()
        self.bg_transparent = QRadioButton("透明底")
        self.bg_white_text = QRadioButton("透明底白字")
        self.bg_outline = QRadioButton("透明底描边")
        self.bg_soft_outline = QRadioButton("透明底柔和描边")
        self.bg_solid_color = QRadioButton("纯色背景")
        self.bg_custom_image = QRadioButton("自定义图片背景")
        left_layout.addWidget(self.bg_label)
        for btn in [self.bg_transparent, self.bg_white_text, self.bg_outline,
                    self.bg_soft_outline, self.bg_solid_color, self.bg_custom_image]:
            self.bg_group.addButton(btn)
            left_layout.addWidget(btn)

        self.color_button = QPushButton("选择纯色背景")
        self.color_button.setVisible(False)
        self.color_button.clicked.connect(self.select_color)
        left_layout.addWidget(self.color_button)

        self.image_button = QPushButton("选择图片背景")
        self.image_button.setVisible(False)
        self.image_button.clicked.connect(self.select_image)
        left_layout.addWidget(self.image_button)

        self.bg_solid_color.toggled.connect(lambda checked: self.color_button.setVisible(checked))
        self.bg_custom_image.toggled.connect(lambda checked: self.image_button.setVisible(checked))

        # 类型选项
        self.type_label = QLabel("颜色选项")
        self.type_group = QButtonGroup()
        self.type_magic = QRadioButton("魔法")
        self.type_science = QRadioButton("科学")
        self.type_custom = QRadioButton("自定义")

        left_layout.addWidget(self.type_label)
        for btn in [self.type_magic, self.type_science, self.type_custom]:
            self.type_group.addButton(btn)
            left_layout.addWidget(btn)

        # 自定义区域（仅在选择“自定义”时显示）
        self.custom_group = QGroupBox("自定义渐变设置")
        self.custom_group.setVisible(False)
        custom_layout = QVBoxLayout()
        # 在这里放置渐变滑条
        self.gradient_slider = GradientSlider()
        custom_layout.addWidget(self.gradient_slider)
        self.custom_group.setLayout(custom_layout)
        left_layout.addWidget(self.custom_group)

        # 监听类型选项变化，控制自定义区域显示
        self.type_custom.toggled.connect(lambda checked: self.custom_group.setVisible(checked))

        # 右侧图片预览区域
        self.image_preview = QLabel("图片预览")
        self.image_preview.setFrameStyle(QFrame.Shape.Box)
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setFixedSize(500, 500)
        self.image_preview.setAcceptDrops(True)
        self.image_preview.dragEnterEvent = self.dragEnterEvent
        self.image_preview.dropEvent = self.dropEvent

        form_layout.addLayout(left_layout)
        form_layout.addWidget(self.image_preview)
        main_layout.addLayout(form_layout)

        # 底部按钮
        bottom_layout = QHBoxLayout()
        self.generate_button = QPushButton("生成字体")
        self.save_button = QPushButton("保存图片")
        self.generate_button.clicked.connect(self.generate_font)
        self.save_button.clicked.connect(self.save_image)
        bottom_layout.addWidget(self.generate_button)
        bottom_layout.addWidget(self.save_button)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def select_color(self):
        color = CustomColorDialog.getColor()
        if color.isValid():
            self.color_button.setStyleSheet(f"background-color: {color.name()}")

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择背景图片", "", "Images (*.png *.jpg)")
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_preview.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage() or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.load_image(file_path)

    def generate_font(self):
        print("生成字体逻辑")

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "Images (*.png *.jpg)")
        if file_path:
            print("保存图片到", file_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
