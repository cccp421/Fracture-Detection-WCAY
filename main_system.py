import sys
import cv2
import threading
import warnings
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QListWidget, QFileDialog,
    QTextEdit, QLineEdit, QSpinBox, QComboBox, QSplitter
)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
from ultralytics import YOLO
from annotation_tool_new import AnnotationWidget

warnings.filterwarnings("ignore")


def cvimg_to_qpixmap(cv_img):
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    return QPixmap.fromImage(QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888))


# ==========================================
# 模块 1：临床诊断推理界面 (Clinical Widget)
# ==========================================
class ClinicalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.image = None
        self.model = None
        self.init_ui()

    def init_ui(self):
        # 图像展示区
        self.label_src = QLabel("原始影像区");
        self.label_src.setStyleSheet("border: 1px solid gray;")
        self.label_pred = QLabel("智能检测结果");
        self.label_pred.setStyleSheet("border: 1px solid gray;")

        img_layout = QHBoxLayout()
        img_layout.addWidget(self.label_src)
        img_layout.addWidget(self.label_pred)

        # 控制区
        btn_layout = QHBoxLayout()
        self.btn_load_img = QPushButton("加载 X光影像")
        self.btn_load_model = QPushButton("加载 WCAY 模型")
        self.btn_infer = QPushButton("智能辅助检测")

        btn_layout.addWidget(self.btn_load_img)
        btn_layout.addWidget(self.btn_load_model)
        btn_layout.addWidget(self.btn_infer)

        self.log = QTextEdit();
        self.log.setReadOnly(True);
        self.log.setFixedHeight(100)

        layout = QVBoxLayout()
        layout.addLayout(img_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.log)
        self.setLayout(layout)

        # 绑定事件
        self.btn_load_img.clicked.connect(self.load_image)
        self.btn_load_model.clicked.connect(self.load_model)
        self.btn_infer.clicked.connect(self.run_inference)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择X光图像", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image = cv2.imread(path)
            self.label_src.setPixmap(cvimg_to_qpixmap(self.image).scaled(self.label_src.size(), Qt.KeepAspectRatio))
            self.log.append(f"已加载图像: {path}")

    def load_model(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择YOLO模型", "", "YOLO Model (*.pt)")
        if path:
            self.model = YOLO(path)
            self.log.append(f"模型加载成功: {path}")

    def run_inference(self):
        if self.image is None or self.model is None:
            self.log.append("请先加载图像和模型！")
            return
        self.log.append("开始推理...")
        results = self.model(self.image, conf=0.20, iou=0.45, verbose=False)
        result = results[0]
        draw_img = self.image.copy()

        if len(result.boxes) == 0:
            self.log.append("未检测到骨折")
        else:
            self.log.append(f"检测到 {len(result.boxes)} 处疑似骨折")
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(draw_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(draw_img, f"Fracture {float(box.conf[0]):.2f}", (x1, y1 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        self.label_pred.setPixmap(cvimg_to_qpixmap(draw_img).scaled(self.label_pred.size(), Qt.KeepAspectRatio))
        self.log.append("推理完成\n")


# ==========================================
# 模块 2：科研训练界面 (Training Widget - ★包含冻结策略)
# ==========================================
class TrainingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 路径配置区 (简化展示)
        self.edit_data = QLineEdit();
        self.btn_data = QPushButton("选择数据集(yaml)")
        row_data = QHBoxLayout();
        row_data.addWidget(QLabel("数据集:"));
        row_data.addWidget(self.edit_data);
        row_data.addWidget(self.btn_data)

        self.edit_weight = QLineEdit("../weights/WCAY.pt")  # 默认加载预训练权重
        self.btn_weight = QPushButton("选择预训练权重")
        row_weight = QHBoxLayout();
        row_weight.addWidget(QLabel("初始权重:"));
        row_weight.addWidget(self.edit_weight);
        row_weight.addWidget(self.btn_weight)

        # ★ 核心：训练策略选择
        self.combo_strategy = QComboBox()
        self.combo_strategy.addItems(["全参数微调 (Full Fine-tuning)", "极少样本冻结策略 (冻结主干 [0-10] 层)"])
        row_strategy = QHBoxLayout();
        row_strategy.addWidget(QLabel("训练策略:"));
        row_strategy.addWidget(self.combo_strategy)

        # 参数区
        self.spin_epoch = QSpinBox();
        self.spin_epoch.setRange(1, 1000);
        self.spin_epoch.setValue(100)
        row_param = QHBoxLayout();
        row_param.addWidget(QLabel("Epochs:"));
        row_param.addWidget(self.spin_epoch)

        self.btn_train = QPushButton("一键启动科研训练")
        self.btn_train.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.log = QTextEdit();
        self.log.setReadOnly(True)

        layout.addLayout(row_data);
        layout.addLayout(row_weight);
        layout.addLayout(row_strategy)
        layout.addLayout(row_param);
        layout.addWidget(self.btn_train);
        layout.addWidget(self.log)
        self.setLayout(layout)

        self.btn_train.clicked.connect(self.start_train)
        self.btn_data.clicked.connect(
            lambda: self.edit_data.setText(QFileDialog.getOpenFileName(self, "选择yaml", "", "YAML (*.yaml)")[0]))
        self.btn_weight.clicked.connect(self.select_weight)

    def start_train(self):
        t = threading.Thread(target=self.run_train)
        t.start()

    def run_train(self):
        self.log.append("初始化 WCAY 训练引擎...")
        model = YOLO("yolov8n.yaml")  # 替换为你的 WCAY 结构
        if self.edit_weight.text():
            model.load(self.edit_weight.text())
            self.log.append("已加载自监督 (BYOL) 预训练权重。")

        # ★ 核心逻辑：获取当前选择的策略
        strategy_idx = self.combo_strategy.currentIndex()
        freeze_layers = None
        if strategy_idx == 1:
            freeze_layers = 11  # 在 YOLOv8 架构中，0-10 层通常代表整个 Backbone。freeze=11 意味着冻结前 11 层。
            self.log.append(">>> 已启用【极少样本冻结策略】: 锁定主干网络 (第0至10层)，保护解剖学先验特征！")
        else:
            self.log.append(">>> 已启用【全参数微调】。")

        self.log.append("开始训练...")

        # 启动训练
        model.train(
            data=self.edit_data.text(),
            epochs=self.spin_epoch.value(),
            freeze=freeze_layers,  # ★ 将冻结策略传入引擎
            project="runs/train",
            name="wca_fracture_exp"
        )
        self.log.append("训练圆满完成！")

    def select_weight(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择预训练权重",
            "",
            "PyTorch Weights (*.pt)"
        )
        if path:
            self.edit_weight.setText(path)
            self.log.append(f"已选择权重: {path}")

# ==========================================
# 主窗口：导航栏 + 多页面路由
# ==========================================
class MainSystemWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("医疗骨折影像辅助诊断与科研迭代系统")
        self.resize(1280, 800)

        # 核心：使用 QSplitter 分割左右区域
        splitter = QSplitter(Qt.Horizontal)

        # 左侧：功能导航栏
        self.nav_list = QListWidget()
        self.nav_list.setSpacing(20)  # 项之间间距
        self.nav_list.setUniformItemSizes(True)
        for i in range(self.nav_list.count()):
            item = self.nav_list.item(i)
            item.setSizeHint(item.sizeHint().expandedTo(item.sizeHint()))
            item.setSizeHint(item.sizeHint().grownBy(Qt.QMargins(0, 20, 0, 20)))

        self.nav_list.setFixedWidth(200)
        self.nav_list.setFont(QFont("Microsoft YaHei", 12))
        self.nav_list.addItems(["🩺 临床辅助诊断", "🏷️ 影像数据标注", "🧪 科研模型训练"])
        self.nav_list.currentRowChanged.connect(self.switch_page)
        self.nav_list.setStyleSheet("""
        QListWidget {
            background-color: #f5f7fa;
            border: none;
        }

        QListWidget::item {
            height: 80px;
            padding-left: 20px;
            border-radius: 10px;
            margin: 5px;
        }

        QListWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }

        QListWidget::item:hover {
            background-color: #e6f2ff;
        }
        """)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        self.nav_list.setMinimumWidth(220)
        self.nav_list.setMaximumWidth(260)
        self.nav_list.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))


        # 右侧：多页面堆叠容器
        self.stacked_widget = QStackedWidget()

        # 页面 1：临床诊断
        self.page_clinical = ClinicalWidget()
        # 页面 2：数据标注
        self.page_annotation = AnnotationWidget()
        # 页面 3：科研训练
        self.page_training = TrainingWidget()

        self.stacked_widget.addWidget(self.page_clinical)
        self.stacked_widget.addWidget(self.page_annotation)
        self.stacked_widget.addWidget(self.page_training)

        splitter.addWidget(self.nav_list)
        splitter.addWidget(self.stacked_widget)

        self.setCentralWidget(splitter)
        self.nav_list.setCurrentRow(0)  # 默认打开诊断界面

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainSystemWindow()
    win.show()
    sys.exit(app.exec_())