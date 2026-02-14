import socket
import threading
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor

HOST= '127.0.0.1'
PORT = 5555

class Comm(QObject):
    msg = pyqtSignal(str)
    disc = pyqtSignal()

class ChatWin(QMainWindow):
    def __init__(self, user, sock):
        super().__init__()
        self.user, self.sock, self.c = user, sock, Comm()
        self.c.msg.connect(self.add_msg)
        self.c.disc.connect(lambda: self.add_msg('⚠️ Disconnected'))
        self.setWindowTitle('PyChat')
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("""
            QMainWindow{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #667eea,stop:1 #764ba2)}
            QLabel{color:white;font-size:16px;font-weight:bold;padding:10px;background:rgba(255,255,255,0.1);border-radius:10px}
            QTextEdit{background:rgba(255,255,255,0.95);border:2px solid rgba(255,255,255,0.3);border-radius:15px;padding:15px;font-size:13px;color:#333}
            QLineEdit{background:rgba(255,255,255,0.95);border:2px solid rgba(255,255,255,0.5);border-radius:20px;padding:12px 20px;font-size:13px;color:#333}
            QLineEdit:focus{border:2px solid #4CAF50}
            QPushButton{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #56CCF2,stop:1 #2F80ED);color:white;border:none;border-radius:20px;padding:12px 30px;font-size:14px;font-weight:bold}
            QPushButton:hover{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #2F80ED,stop:1 #56CCF2)}
            QPushButton#q{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #f093fb,stop:1 #f5576c)}
        """)
        w = QWidget()
        self.setCentralWidget(w)
        l = QVBoxLayout(w)
        l.setSpacing(15)
        l.setContentsMargins(20, 20, 20, 20)
        l.addWidget(QLabel(f'🟢 Connected as: {user}'))
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        l.addWidget(self.chat)
        h = QHBoxLayout()
        self.inp = QLineEdit()
        self.inp.setPlaceholderText('Type your message...')
        self.inp.returnPressed.connect(self.send)
        sb = QPushButton('Send ✉')
        sb.clicked.connect(self.send)
        sb.setFixedWidth(120)
        qb = QPushButton('Quit')
        qb.setObjectName('q')
        qb.clicked.connect(self.close)
        qb.setFixedWidth(100)
        h.addWidget(self.inp)
        h.addWidget(sb)
        h.addWidget(qb)
        l.addLayout(h)
        threading.Thread(target=self.recv, daemon=True).start()
    
    def recv(self):
        try:
            while True:
                d = self.sock.recv(4096)
                if not d: break
                self.c.msg.emit(d.decode('utf-8'))
        except: pass
        self.c.disc.emit()
    
    def add_msg(self, m):
        if m.startswith('You:') or m.startswith('You ('):
            m = f'<span style="color:#2F80ED;font-weight:bold">{m}</span>'
        elif '@' in m or 'private' in m.lower():
            m = f'<span style="color:#9C27B0;font-style:italic">{m}</span>'
        elif 'joined' in m.lower() or 'left' in m.lower():
            m = f'<span style="color:#FF9800;font-weight:bold">{m}</span>'
        self.chat.append(m)
        self.chat.moveCursor(QTextCursor.End)
    
    def send(self):
        t = self.inp.text().strip()
        if not t: return
        try:
            self.sock.sendall(t.encode('utf-8'))
            self.add_msg(f'You: {t}' if not t.startswith('@') else f'You (private): {t}')
            self.inp.clear()
        except: self.add_msg('❌ Send failed')
    
    def closeEvent(self, e):
        try: self.sock.sendall('/quit'.encode('utf-8'))
        except: pass
        try: self.sock.close()
        except: pass

def start(user):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        s.sendall(user.encode('utf-8'))
        w = ChatWin(user, s)
        w.show()
    except Exception as e:
        QMessageBox.critical(None, 'Error', f'Connection failed:\n{e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    user, ok = QInputDialog.getText(None, 'Username', 'Enter username:')
    if ok and user and user.strip():
        start(user.strip())
        sys.exit(app.exec_())
    else:
        QMessageBox.warning(None, 'Error', 'Username required')