import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog)
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QPoint
from PyQt6.QtGui import QGuiApplication, QPainter, QPen, QColor, QFont, QLinearGradient, QPixmap, QImage, QBitmap, QBrush
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np

class AppCore(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MedInsight')
        screen_ref = QGuiApplication.primaryScreen()
        size_s = screen_ref.size()
        size_x = size_s.width() * 0.8
        size_y = size_s.height() * 0.8
        self.setGeometry((size_s.width() - size_x)/2, (size_s.height() - size_y)/2, size_x, size_y)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.central_layout.setContentsMargins(40,40,40,40)
        self.central_layout.setSpacing(30)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setting_ui()

    # UI da aplicação
    def setting_ui(self):
        layout_left = QVBoxLayout()
        self.layout_right = QVBoxLayout()
        self.layout_analisys = QVBoxLayout()
        layout_title = QVBoxLayout()
        
        # janela do processamento de imagem
        self.layout_right.setContentsMargins(20,20,20,20)
        self.widget_analise = LocalStylus()
        self.widget_analise.setLayout(self.layout_analisys)
        self.widget_analise.setFixedSize(self.width() * 0.38, self.height() * 0.18)
        self.widget_layout_right = QWidget()
        self.widget_layout_right.setFixedSize(self.width() * 0.48, self.height() * 0.80)
        self.widget_layout_right.setLayout(self.layout_right)

        self.load_image = ImgLoad(rounded_x=10,rounded_y=10)
        self.button_identify = LabelButton('Identify',rounded_x=10, rounded_y=10)
        button_export = LabelButton('Export', rounded_x=10, rounded_y=10)

        self.button_identify.setFixedHeight(self.widget_analise.height() * 0.5)
        button_export.setFixedHeight(self.widget_analise.height() * 0.5)
        self.label_info = QLabel()
        self.label_info.setFixedHeight(30)
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_setting = QFont()
        font_setting.setPixelSize(30)
        font_setting.setBold(True)
        self.label_info.setFont(font_setting)
        self.label_info.setHidden(True)

        self.button_identify.target_ui = lambda: self.identify_img()

        self.layout_analisys.addWidget(self.label_info)
        self.layout_analisys.addWidget(self.load_image)
        self.layout_analisys.addWidget(self.button_identify)
        self.layout_analisys.addWidget(button_export)

        self.options_01 = LabelButton('Load Image', 1)
        self.options_02 = LabelButton('Analyze X-ray')
        self.options_03 = LabelButton('Diagnosis History')
        self.options_04 = LabelButton('Close',2)

        self.options_01.target_ui = lambda: self.active_analisys()
        self.options_02.target_ui = lambda: self.normal_ui()
        self.options_03.target_ui = lambda: self.normal_ui()
        self.options_04.target_ui = lambda: self.close()

        button_export.target_ui = lambda: self.normal_ui()

        self.width_pattern = self.width() * 0.38
        self.height_pattern = self.height() * 0.18

        self.options_01.setFixedSize(self.width_pattern, self.height_pattern)
        self.options_02.setFixedSize(self.width_pattern, self.height_pattern)
        self.options_03.setFixedSize(self.width_pattern, self.height_pattern)
        self.options_04.setFixedSize(self.width_pattern, self.height_pattern)

        layout_left.addWidget(self.options_01)
        layout_left.addWidget(self.options_02)
        layout_left.addWidget(self.options_03)
        layout_left.addWidget(self.options_04)

        label_title = QLabel('MedInsight')
        label_title.setStyleSheet('color: #00aeef')
        font_title = QFont()
        font_title.setPixelSize(80)
        font_title.setFamily('Roboto')
        label_title.setFont(font_title)
        layout_title.addWidget(label_title)

        label_subtitle = QLabel('Illuminating Health, Empowering Decisions.')
        label_subtitle.setStyleSheet('color: #00aeef')
        font_subtitle = QFont()
        font_subtitle.setPixelSize(19)
        font_subtitle.setFamily('Roboto')
        label_subtitle.setFont(font_subtitle)
        layout_title.addWidget(label_subtitle)

        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        self.layout_right.addLayout(layout_title)
        self.central_layout.addLayout(layout_left)
        self.central_layout.addWidget(self.widget_layout_right)
        self.central_layout.addWidget(self.widget_analise)

        label_bottom = QLabel('All rights reserved.')
        label_bottom.setFixedHeight(20)
        label_bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_right.addWidget(label_bottom)

        self.widget_analise.hide()


    def identify_img(self):
        self.label_info.setText(self.options_01.predict())
        self.label_info.setHidden(False)
        

    def active_analisys(self):
        self.widget_layout_right.hide()
        self.widget_analise.show()
        self.central_layout.setContentsMargins(40,40,40,40)
        self.central_layout.setSpacing(30)
        self.load_image.update_image(self.options_01.get_path_file())

    def normal_ui(self):
        self.widget_analise.hide()
        self.widget_layout_right.show()
        self.central_layout.setContentsMargins(40,40,40,40)
        self.central_layout.setSpacing(30)
        

    def update_size(self):
        self.width_pattern = self.width() * 0.38
        self.height_pattern = self.height() * 0.18
        self.widget_analise.setFixedSize(self.width() * 0.48, self.height() * 0.87)

        self.options_01.update()
        self.options_02.update()
        self.options_03.update()
        self.options_04.update()

        self.options_01.setFixedSize(self.width_pattern, self.height_pattern)
        self.options_02.setFixedSize(self.width_pattern, self.height_pattern)
        self.options_03.setFixedSize(self.width_pattern, self.height_pattern)
        self.options_04.setFixedSize(self.width_pattern, self.height_pattern)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_pos:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)  
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None  

    def resizeEvent(self, event):
        self.update_size()
        super().resizeEvent(event)

    def paintEvent(self, event):
        grad = QLinearGradient(0,0,self.width()/2,0)
        painter = QPainter(self)
        grad.setColorAt(0, QColor(255,255,255))
        grad.setColorAt(1, QColor(240,240,240))
        painter.setBrush(grad)
        painter.fillRect(self.rect(), grad)

class ImgLoad(QWidget):
    def __init__(self, path_img='', rounded_x=20, rounded_y=20):
        super().__init__()
        self.path_img = path_img
        self.rounded_x = rounded_x
        self.rounded_y = rounded_y

    def update_image(self, input_path):
        self.path_img = input_path
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawRoundedRect(0,0,self.width()-1,self.height()-1,self.rounded_x, self.rounded_y)
        pixmap = QPixmap(self.path_img)
        pixmap = pixmap.scaled(self.width() * 0.7, self.height() * 0.7)
        painter.drawPixmap((self.width() - (self.width() * 0.7))/2, (self.height() - (self.height() * 0.7))/2, pixmap)

        
class LocalStylus(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        grad = QLinearGradient(0,0,self.width(),0)
        grad.setColorAt(1, QColor(0, 170, 255,2))
        grad.setColorAt(0, QColor(20, 120, 235,5))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(89, 149, 150,50))
        painter.drawRoundedRect(0,0,self.width(), self.height(), 10, 10)
        painter.setBrush(grad)
        painter.drawRoundedRect(0,0,self.width() - 2, self.height() - 2, 10, 10) 

class LabelButton(QLabel):
    target_ui = None
    def __init__(self, text_message='', index_func=0, rounded_x=50, rounded_y=50):
        super().__init__()
        self.rounded_x = rounded_x
        self.rounded_y = rounded_y
        self.text_message = text_message
        self.index_func = index_func
        self.path_returned = ''
        self.color_text = QPen(QColor(255,255,255))

        self.grad = QLinearGradient(0,0,self.width(),0)
        self.grad.setColorAt(1, QColor(0, 174, 239))
        self.grad.setColorAt(0, QColor(13, 110, 189))

    def clicked_function(self):
        self.load_image_file()

    def load_image_file(self):
        if self.index_func == 1:
            file_path,_ = QFileDialog.getOpenFileName(
                self,
                'Select an image',
                '',
                'Image (*.jpg *.png *.bmp *.jpeg *.gif);;JPG (*.jpg);;JPEG (*.jpeg);;PNG (*.png);;Bitmap (*.bmp)'
            )
            self.path_returned = file_path
        self.target_ui()

    def get_path_file(self):
        return self.path_returned

    def predict(self):
        image = load_img(self.get_path_file(), target_size=(128, 128))
        image_array = img_to_array(image) / 255
        image_array = np.expand_dims(image_array, axis=0)
        model = load_model('model/xray_model.h5')
        pred = model.predict(image_array)
        label_names = ['Glioma','Meningioma','Notumor','Pituitary']
        get_index = np.argmax(pred[0], axis=0)
        return label_names[get_index]

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.grad.setColorAt(1, QColor(235, 235, 255))
            self.grad.setColorAt(0, QColor(240, 240, 240))
            self.color_text.setColor(QColor(0, 174, 239))
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.grad.setColorAt(1, QColor(0, 144, 189))
        self.grad.setColorAt(0, QColor(12, 100, 179))
        self.color_text.setColor(QColor(255, 255, 255))
        self.clicked_function()
        self.update()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        self.grad.setColorAt(1, QColor(0, 144, 189))
        self.grad.setColorAt(0, QColor(12, 100, 179))
        self.color_text = QPen(QColor(255,255,255))
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.grad.setColorAt(1, QColor(0, 174, 239))
        self.grad.setColorAt(0, QColor(13, 110, 189))
        self.color_text = QPen(QColor(255,255,255))
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(self.grad)
        fonte = QFont()
        fonte.setPixelSize((self.height() + self.width()) * 0.05)
        painter.setFont(fonte)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.drawRoundedRect(QRect(0,0,self.width(),self.height()), self.rounded_x, self.rounded_y)

        painter.setPen(Qt.GlobalColor.white)
        painter.setPen(self.color_text)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text_message)


if __name__ == '__main__':
    app = QApplication([])
    window = AppCore()
    window.show()
    sys.exit(app.exec())