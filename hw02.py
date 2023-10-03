import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem
#from PyQt5.QtWidgets import *
import pymorphy2


class ParsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Морфопарсинг')
        self.setGeometry(200, 200, 500, 500)
        
        self.morph_app()
        
    def morph_app(self):

        layout = QVBoxLayout()
        
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        
        self.parse_button = QPushButton('parse')
        self.parse_button.clicked.connect(self.parse_text)
        layout.addWidget(self.parse_button)
        
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Словоформа', 'Лемма, лексема', 'Часть речи'])
        layout.addWidget(self.table_widget)
        
        self.setLayout(layout)
        
    def parse_text(self):

        text = self.text_edit.toPlainText()
        
        morph = pymorphy2.MorphAnalyzer()
        words = text.split()  

        parsed_text = morph.parse(text)
        
        self.table_widget.setRowCount(len(words))
        
        for i, word in enumerate(words):
            parse_result = morph.parse(word)
            lemma = parse_result[0].normal_form
            pos = parse_result[0].tag.POS

            item_word = QTableWidgetItem(word)
            self.table_widget.setItem(i, 0, item_word)
            
            item_lemma = QTableWidgetItem(lemma)
            self.table_widget.setItem(i, 1, item_lemma)
            
            item_pos = QTableWidgetItem(str(pos))
            self.table_widget.setItem(i, 2, item_pos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    win = ParsApp()
    win.show()
    
    sys.exit(app.exec_())


#  https://habr.com/ru/articles/651093/