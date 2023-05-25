from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys

class ImageWindow(QDialog):
    def __init__(self, image_path):
        super().__init__()
        
        # Load the image using QPixmap
        pixmap = QPixmap(image_path)
        
        # Create a QLabel to display the image
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        
        # Create a QScrollArea and set the image label as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidget(image_label)
        
        # Set the layout for the window
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        
        # Set the window properties
        self.setWindowTitle('Sentiment Report')
        self.resize(1920,1080)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_path = r'temp\graph_reliance.png'  # Replace with your image path
    window = ImageWindow(image_path)
    window.show()
    sys.exit(app.exec_())
