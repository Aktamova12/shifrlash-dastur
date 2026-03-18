import sys
import re
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTextEdit, QLabel, QGridLayout, QFrame)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class PlayfairCipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Asosiy oyna sozlamalari
        self.setWindowTitle('Playfair Professional Cipher - 2026 Edition')
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("background-color: #f8f9fa;")

        main_layout = QHBoxLayout()

        # --- CHAP PANEL: KIRITISH VA BOSHQARUV ---
        left_panel = QVBoxLayout()
        
        header = QLabel("Playfair Algoritmi")
        header.setFont(QFont('Segoe UI', 22, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        left_panel.addWidget(header)

        # Kalit so'z
        left_panel.addWidget(QLabel("Kalit so'z (Key):"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Masalan: MONARCHY")
        self.key_input.setStyleSheet("padding: 12px; border: 2px solid #dee2e6; border-radius: 8px; font-size: 14px;")
        left_panel.addWidget(self.key_input)

        # Matn kiritish
        left_panel.addWidget(QLabel("Kiruvchi Matn:"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Shifrlash yoki deşifrlash uchun matn kiriting...")
        self.text_input.setStyleSheet("padding: 10px; border: 2px solid #dee2e6; border-radius: 8px; font-size: 14px;")
        self.text_input.setFixedHeight(150)
        left_panel.addWidget(self.text_input)

        # Tugmalar paneli
        btn_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton("🔒 SHIFRLASH")
        self.encrypt_btn.setStyleSheet("""
            QPushButton { background-color: #28a745; color: white; padding: 15px; font-weight: bold; border-radius: 8px; font-size: 14px; }
            QPushButton:hover { background-color: #218838; }
        """)
        self.encrypt_btn.clicked.connect(self.process_encrypt)
        
        self.decrypt_btn = QPushButton("🔓 DESHIFRLASH")
        self.decrypt_btn.setStyleSheet("""
            QPushButton { background-color: #007bff; color: white; padding: 15px; font-weight: bold; border-radius: 8px; font-size: 14px; }
            QPushButton:hover { background-color: #0069d9; }
        """)
        self.decrypt_btn.clicked.connect(self.process_decrypt)
        
        btn_layout.addWidget(self.encrypt_btn)
        btn_layout.addWidget(self.decrypt_btn)
        left_panel.addLayout(btn_layout)

        # Natija
        left_panel.addWidget(QLabel("Natija:"))
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setStyleSheet("background-color: #ffffff; border: 2px solid #28a745; border-radius: 8px; font-size: 16px; font-weight: bold; color: #155724;")
        self.result_output.setFixedHeight(120)
        left_panel.addWidget(self.result_output)

        # --- O'NG PANEL: JADVAL VA LOG ---
        right_panel = QVBoxLayout()
        
        right_panel.addWidget(QLabel("5x5 Playfair Jadvali (Tahlil):"))
        self.grid_frame = QFrame()
        self.grid_frame.setStyleSheet("background-color: #ffffff; border-radius: 12px; border: 1px solid #ced4da;")
        self.grid_layout = QGridLayout(self.grid_frame)
        self.matrix_labels = []
        self.create_grid()
        right_panel.addWidget(self.grid_frame)

        # Log tahlili
        right_panel.addWidget(QLabel("Jarayon bosqichlari:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #1e1e1e; color: #dcdcdc; font-family: 'Consolas'; font-size: 12px; border-radius: 8px;")
        right_panel.addWidget(self.log_output)

        main_layout.addLayout(left_panel, 3)
        main_layout.addLayout(right_panel, 2)
        self.setLayout(main_layout)

    def create_grid(self):
        for i in range(5):
            for j in range(5):
                lbl = QLabel("-")
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(65, 65)
                lbl.setFont(QFont('Arial', 16, QFont.Bold))
                lbl.setStyleSheet("border: 1px solid #e9ecef; border-radius: 5px; background-color: #f8f9fa; color: #adb5bd;")
                self.grid_layout.addWidget(lbl, i, j)
                self.matrix_labels.append(lbl)

    def prepare_matrix(self, key):
        # 1. I va J ni birlashtirish, faqat harflarni qoldirish
        key = key.upper().replace('J', 'I')
        key = re.sub(r'[^A-Z]', '', key)
        
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        combined = ""
        for char in key + alphabet:
            if char not in combined:
                combined += char
        
        matrix = [list(combined[i:i+5]) for i in range(0, 25, 5)]
        
        # Jadvalni vizual yangilash
        for idx, char in enumerate(combined):
            self.matrix_labels[idx].setText(char)
            self.matrix_labels[idx].setStyleSheet("background-color: #e7f3ff; border: 2px solid #007bff; color: #007bff; font-weight: bold; border-radius: 5px;")
        
        return matrix

    def prepare_text(self, text, encrypt=True):
        # Tozalash
        text = text.upper().replace('J', 'I')
        text = re.sub(r'[^A-Z]', '', text)
        
        if not text: return ""

        prepared = ""
        i = 0
        while i < len(text):
            a = text[i]
            if (i + 1) < len(text):
                b = text[i+1]
                if a == b and encrypt:
                    prepared += a + 'X' # Juft harflarni ajratish
                    i += 1
                else:
                    prepared += a + b
                    i += 2
            else:
                prepared += a + 'X' # Toq bo'lsa to'ldirish
                i += 1
        return prepared

    def find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return 0, 0

    def playfair_logic(self, text, matrix, mode='enc'):
        res = ""
        step = 1 if mode == 'enc' else -1
        pairs = [text[i:i+2] for i in range(0, len(text), 2)]
        
        self.log_output.append(f"--- {mode.upper()} BOSHLANDI ---")
        self.log_output.append(f"Juftliklar: {' '.join(pairs)}")

        for p in pairs:
            r1, c1 = self.find_position(matrix, p[0])
            r2, c2 = self.find_position(matrix, p[1])

            if r1 == r2: # Bitta qator
                res += matrix[r1][(c1 + step) % 5] + matrix[r2][(c2 + step) % 5]
            elif c1 == c2: # Bitta ustun
                res += matrix[(r1 + step) % 5][c1] + matrix[(r2 + step) % 5][c2]
            else: # To'rtburchak
                res += matrix[r1][c2] + matrix[r2][c1]
        
        return res

    def process_encrypt(self):
        self.log_output.clear()
        key = self.key_input.text()
        text = self.text_input.toPlainText()
        if not key or not text: return

        matrix = self.prepare_matrix(key)
        prepared = self.prepare_text(text, True)
        self.log_output.append(f"Tayyorlangan: {prepared}")
        
        encrypted = self.playfair_logic(prepared, matrix, 'enc')
        self.result_output.setText(encrypted)

    def process_decrypt(self):
        self.log_output.clear()
        key = self.key_input.text()
        text = self.text_input.toPlainText()
        if not key or not text: return

        matrix = self.prepare_matrix(key)
        prepared = self.prepare_text(text, False) # Deshifrlashda X qo'shilmaydi
        
        decrypted = self.playfair_logic(prepared, matrix, 'dec')
        self.result_output.setText(decrypted)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlayfairCipherApp()
    window.show()
    sys.exit(app.exec_())
