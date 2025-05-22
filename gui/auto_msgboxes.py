from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap

class AutoCloseInfoBox(QDialog):
      """
        AutoCloseInfoBox is a subclass of QDialog that displays an information box with an icon and text.
        This class is used to display an information box that automatically closes after a specified timeout.
      """
      def __init__(self, parent, title, text, icon_path, timeout_ms=3000):
         super().__init__(parent)
         self.setWindowTitle(title)
         self.setWindowFlags(self.windowFlags() | Qt.WindowType.Tool)
         layout = QVBoxLayout(self)
         icon_label = QLabel()
         icon_label.setPixmap(QPixmap(icon_path).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
         icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
         layout.addWidget(icon_label)
         # Add a small vertical space between icon and text
         spacer = QLabel()
         spacer.setFixedHeight(10)
         layout.addWidget(spacer)
         text_label = QLabel(text)
         text_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
         layout.addWidget(text_label)
         self.setLayout(layout)
         QTimer.singleShot(timeout_ms, self.accept)