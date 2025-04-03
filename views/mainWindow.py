import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QRadioButton, QVBoxLayout,
    QPushButton, QFileDialog, QButtonGroup, QFrame,
    QGroupBox, QHBoxLayout, QSlider, QWidget
)

from resource_path import resource_path
from titleGenerator import generate_font_image
from views.ColorWidget import GradientSlider, CustomColorDialog
from views.MessageBox import MessageBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        from PIL.Image import Image
        self.img: Image = None
        self.setWindowTitle("某学都的标题工房")
        self.setGeometry(100, 100, 900, 700)

        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()

        # 文本输入框
        self.text_group_box = QGroupBox("文本")
        text_layout = QHBoxLayout()
        self.label1 = QLabel("とある")
        self.text_input1 = QLineEdit()
        self.text_input1.setPlaceholderText("魔法")
        self.label2 = QLabel("の")
        self.text_input2 = QLineEdit()
        self.text_input2.setPlaceholderText("禁书目录")
        self.text_input3 = QLineEdit()
        self.text_input3.setPlaceholderText("小字部分")
        text_layout.addWidget(self.label1)
        text_layout.addWidget(self.text_input1)
        text_layout.addWidget(self.label2)
        text_layout.addWidget(self.text_input2)
        text_layout.addWidget(self.text_input3)
        self.text_group_box.setLayout(text_layout)
        left_layout.addWidget(self.text_group_box)
        # 背景选项
        self.bg_group_box = QGroupBox("背景色")
        bg_layout = QVBoxLayout()
        self.bg_group = QButtonGroup()
        self.bg_transparent = QRadioButton("透明")  # 透明背景
        self.bg_solid_color = QRadioButton("纯色")  # 纯色背景
        self.bg_custom_image = QRadioButton("自定义图片背景")  # 自定义背景
        self.bg_transparent.setChecked(True)
        for btn in [self.bg_transparent, self.bg_solid_color, self.bg_custom_image]:
            self.bg_group.addButton(btn)
            bg_layout.addWidget(btn)
        self.bg_group_box.setLayout(bg_layout)
        # 纯色背景
        self.color_button = QPushButton("选择纯色背景")
        self.color_button.setVisible(False)
        self.color_button.clicked.connect(self.select_color)
        bg_layout.addWidget(self.color_button)
        # 图片背景
        self.image_button = QPushButton("选择图片背景")
        self.image_button.setVisible(False)
        self.image_button.clicked.connect(self.select_image)
        bg_layout.addWidget(self.image_button)
        self.bg_solid_color.toggled.connect(lambda checked: self.color_button.setVisible(checked))
        self.bg_custom_image.toggled.connect(lambda checked: self.image_button.setVisible(checked))
        left_layout.addWidget(self.bg_group_box)
        # 颜色选项
        self.color_group_box = QGroupBox("文字颜色")
        color_layout = QVBoxLayout()
        self.color_group = QButtonGroup()
        self.color_magic = QRadioButton("魔法")
        self.color_science = QRadioButton("科学")
        self.color_custom = QRadioButton("自定义")
        self.color_magic.setChecked(True)
        for btn in [self.color_magic, self.color_science, self.color_custom]:
            self.color_group.addButton(btn)
            color_layout.addWidget(btn)
        self.color_group_box.setLayout(color_layout)
        left_layout.addWidget(self.color_group_box)

        # 自定义区域（仅在选择“自定义”时显示）
        self.custom_group = QGroupBox("自定义渐变设置")
        self.custom_group.setVisible(False)
        custom_layout = QVBoxLayout()
        # 在这里放置渐变滑条
        self.gradient_slider = GradientSlider()
        custom_layout.addWidget(self.gradient_slider)
        # 角度滑条与角度输入框
        self.angle_label = QLabel("角度")
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("0-360")
        self.angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.angle_slider.setRange(0, 360)
        self.angle_slider.setValue(0)
        self.angle_slider.setSingleStep(1)
        # 滑条和输入框绑定
        self.angle_slider.valueChanged.connect(lambda value: self.angle_input.setText(str(value)))
        self.angle_input.textChanged.connect(lambda text: self.angle_slider.setValue(int(text)))
        angle_layout = QHBoxLayout()
        angle_layout.addWidget(self.angle_label)
        angle_layout.addWidget(self.angle_input)
        angle_layout.addWidget(self.angle_slider)
        custom_layout.addLayout(angle_layout)
        self.custom_group.setLayout(custom_layout)
        color_layout.addWidget(self.custom_group)
        # 监听类型选项变化，控制自定义区域显示
        self.color_custom.toggled.connect(lambda checked: self.custom_group.setVisible(checked))
        # 文字描边
        self.outfit_group_box = QGroupBox("文字描边")
        outfit_layout = QVBoxLayout()
        self.outfit_group = QButtonGroup()
        self.outfit_alpha = QRadioButton("透明")
        self.outfit_fill = QRadioButton("填充")
        self.outfit_hard = QRadioButton("填充+描边")
        self.outfit_fill.setChecked(True)
        for btn in [self.outfit_alpha, self.outfit_fill, self.outfit_hard]:
            self.outfit_group.addButton(btn)
            outfit_layout.addWidget(btn)
        self.outfit_group_box.setLayout(outfit_layout)
        left_layout.addWidget(self.outfit_group_box)
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

    def pil2pixmap(self):
        """将 Pillow 的 Image 转换为 QPixmap"""
        # 如果图像不是RGBA模式，则转换成RGBA模式
        if not self.img:
            return
        if self.img.mode != "RGBA":
            self.img = self.img.convert("RGBA")
        # 将 PIL Image 保存到 BytesIO 中
        data = self.img.tobytes("raw", "RGBA")
        q_image = QImage(data, self.img.width, self.img.height, QImage.Format.Format_RGBA8888)
        self.image_preview.setPixmap(QPixmap.fromImage(q_image).scaled(450, 450, Qt.AspectRatioMode.KeepAspectRatio))

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.image_preview.setPixmap(pixmap.scaled(450, 450, Qt.AspectRatioMode.KeepAspectRatio))

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
        try:
            angle = 155
            if self.color_science.isChecked():
                from titleGenerator import science_color
                color = science_color
            elif self.color_custom.isChecked():
                color = self.gradient_slider.get_color_stops()
                print(color)
                angle = self.angle_slider.value()
            else:
                from titleGenerator import magic_color
                color = magic_color
            self.img = generate_font_image(text1=self.text_input1.text(), text2=self.text_input2.text(),
                                           text3=self.text_input3.text(),
                                           font_path=resource_path("fonts/XiaoMingChaoPro-B-6.otf"),
                                           small_font_path="", angle=angle,
                                           colors=color)
            self.pil2pixmap()
            MessageBox("生成成功", "success",parent=self)
        except Exception as e:
            print(e.args)

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "Images (*.png *.jpg)")
        if file_path:
            if self.img:
                try:
                    self.img.save(file_path)
                    print("保存图片到", file_path)
                    MessageBox("保存成功", "success",parent=self)
                except Exception as e:
                    print(e.args)
                    MessageBox(f"错误:{e.args}", "error", parent=self)
                    return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
