import sys
import os
import cv2
from PyQt5.QtWidgets import (
    QLabel, QPushButton,
    QFileDialog, QTextEdit, QWidget, QVBoxLayout,
    QHBoxLayout, QComboBox
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect

def cvimg_to_qpixmap(cv_img):
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    return QPixmap.fromImage(
        QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
    )


class AnnotateLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_win = parent

        self.start_point = None
        self.end_point = None
        self.drawing = False

        # 现在每个框都带 class_id
        self.boxes = []  # [(x1,y1,x2,y2,class_id)]

        # 映射参数
        self.img_w = None
        self.img_h = None
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        self.setMouseTracking(True)

    # ---------- 坐标映射 ----------
    def set_image_info(self, img_w, img_h):
        self.img_w = img_w
        self.img_h = img_h
        lw, lh = self.width(), self.height()
        self.scale = min(lw / img_w, lh / img_h)
        self.offset_x = (lw - img_w * self.scale) / 2
        self.offset_y = (lh - img_h * self.scale) / 2

    def label_to_image(self, x, y):
        ix = (x - self.offset_x) / self.scale
        iy = (y - self.offset_y) / self.scale
        ix = max(0, min(ix, self.img_w))
        iy = max(0, min(iy, self.img_h))
        return int(ix), int(iy)

    # ---------- 右键删除 ----------
    def delete_box_at(self, img_x, img_y):
        for i in reversed(range(len(self.boxes))):
            x1, y1, x2, y2, _ = self.boxes[i]
            if x1 <= img_x <= x2 and y1 <= img_y <= y2:
                del self.boxes[i]
                self.update()
                return

    # ---------- 撤销 ----------
    def undo_last_box(self):
        if self.boxes:
            self.boxes.pop()
            self.update()

    # ---------- 鼠标事件 ----------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.drawing = True

        elif event.button() == Qt.RightButton:
            x_img, y_img = self.label_to_image(event.x(), event.y())
            self.delete_box_at(x_img, y_img)

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False

            x1i, y1i = self.label_to_image(
                self.start_point.x(), self.start_point.y()
            )
            x2i, y2i = self.label_to_image(
                self.end_point.x(), self.end_point.y()
            )

            x1, x2 = sorted([x1i, x2i])
            y1, y2 = sorted([y1i, y2i])

            if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                # ★ 核心：在此刻绑定类别
                cid = int(self.parent_win.class_combo.currentText())
                self.boxes.append((x1, y1, x2, y2, cid))

            self.update()

    # ---------- 绘制 ----------
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        for x1, y1, x2, y2, cid in self.boxes:
            color = self.parent_win.class_colors.get(cid, Qt.red)
            painter.setPen(QPen(color, 2))

            xl = x1 * self.scale + self.offset_x
            yl = y1 * self.scale + self.offset_y
            wl = (x2 - x1) * self.scale
            hl = (y2 - y1) * self.scale

            painter.drawRect(
                int(xl), int(yl), int(wl), int(hl)
            )

        if self.drawing and self.start_point and self.end_point:
            painter.setPen(QPen(Qt.white, 1, Qt.DashLine))
            painter.drawRect(QRect(self.start_point, self.end_point))


class AnnotationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.images = []
        self.index = 0
        self.image = None
        self.image_dir = None
        self.label_dir = None
        self.demo_window = None

        # 类别 → 颜色
        self.class_colors = {
            0: Qt.red,
            1: Qt.green,
            2: Qt.blue,
            3: Qt.yellow
        }

        self.init_ui()

    def init_ui(self):
        self.label = AnnotateLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border:1px solid gray;")
        self.label.setMinimumSize(900, 550)

        self.class_combo = QComboBox()
        self.class_combo.addItems(["0", "1", "2", "3"])
        self.class_combo.setFixedWidth(80)

        self.btn_prev = QPushButton("上一张")
        self.btn_next = QPushButton("下一张")
        self.btn_save = QPushButton("保存标注")
        self.btn_load_dir = QPushButton("加载图片文件夹")

        self.btn_prev.clicked.connect(self.prev_image)
        self.btn_next.clicked.connect(self.next_image)
        self.btn_save.clicked.connect(self.save_annotation)
        self.btn_load_dir.clicked.connect(self.load_image_dir)
        # self.btn_back.clicked.connect(self.back_to_demo)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(90)

        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("类别ID:"))
        ctrl.addWidget(self.class_combo)
        ctrl.addWidget(self.btn_prev)
        ctrl.addWidget(self.btn_next)
        ctrl.addWidget(self.btn_save)
        ctrl.addWidget(self.btn_load_dir)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(ctrl)
        layout.addWidget(self.log)

        w = QWidget()
        self.setLayout(layout)


    # ---------- 快捷键 ----------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.label.undo_last_box()
            self.log.append("撤销上一标注")

    # ---------- 文件夹 ----------
    def load_image_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择 images 文件夹")
        if not folder:
            return

        self.image_dir = folder
        self.label_dir = os.path.join(os.path.dirname(folder), "labels")
        os.makedirs(self.label_dir, exist_ok=True)

        self.images = sorted([
            f for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ])

        self.index = 0
        self.load_current_image()
        self.log.append(f"加载完成，共 {len(self.images)} 张图片")

    def load_current_image(self):
        img_path = os.path.join(self.image_dir, self.images[self.index])
        self.image = cv2.imread(img_path)
        self.label.boxes.clear()

        h, w, _ = self.image.shape
        self.label.set_image_info(w, h)

        self.label.setPixmap(
            cvimg_to_qpixmap(self.image).scaled(
                self.label.size(), Qt.KeepAspectRatio
            )
        )

        self.log.append(
            f"{self.images[self.index]} ({self.index+1}/{len(self.images)})"
        )

    def prev_image(self):
        if self.index > 0:
            self.index -= 1
            self.load_current_image()

    def next_image(self):
        if self.index < len(self.images) - 1:
            self.index += 1
            self.load_current_image()

    def save_annotation(self):
        if self.image is None or not self.label.boxes:
            self.log.append("当前无标注")
            return

        h, w, _ = self.image.shape
        name = os.path.splitext(self.images[self.index])[0]
        path = os.path.join(self.label_dir, name + ".txt")

        with open(path, "w") as f:
            for x1, y1, x2, y2, cid in self.label.boxes:
                xc = ((x1 + x2) / 2) / w
                yc = ((y1 + y2) / 2) / h
                bw = (x2 - x1) / w
                bh = (y2 - y1) / h
                f.write(f"{cid} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

        self.log.append(f"保存完成: labels/{name}.txt")



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = AnnotationWindow()
#     win.show()
#     sys.exit(app.exec_())
