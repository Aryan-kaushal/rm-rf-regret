#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox,
    QAction, QTabWidget, QSplitter, QAbstractItemView
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Constants
HOME = str(Path.home())
TRASH_DIR = Path(HOME) / '.rm-rf-regret' / 'trash'
LOG_FILE = Path(HOME) / '.rm-rf-regret' / 'log.txt'
TRASH_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE.touch(exist_ok=True)

# File categories
FILE_CATEGORIES = {
    'Images': ['.jpg', '.png', '.gif'],
    'Documents': ['.pdf', '.txt', '.doc', '.docx'],
    'Videos': ['.mp4', '.avi', '.mov'],
    'Audio': ['.mp3', '.wav'],
    'Archives': ['.zip', '.tar', '.gz'],
    'Junk': ['.tmp', '.log', '~'],
    'Others': []
}
CATEGORY_COLORS = {
    'Images': QtGui.QColor('#5a9aff'),
    'Documents': QtGui.QColor('#5aff5a'),
    'Videos': QtGui.QColor('#ff9f1a'),
    'Audio': QtGui.QColor('#d65cff'),
    'Archives': QtGui.QColor('#ff5a5a'),
    'Junk': QtGui.QColor('#777777'),
    'Others': QtGui.QColor('#cccccc')
}

# Styles
DARK_STYLE = '''
QWidget { background: #121212; color: #e0e0e0; }
QPushButton { background: #1f1f1f; border: 1px solid #333; padding: 6px; }
QTreeWidget { background: #1e1e1e; color: #e0e0e0; }
QTabBar::tab:selected { background: #3a6ff3; }
'''

LIGHT_STYLE = '''
QWidget { background: #fafafa; color: #333; }
QPushButton { background: #e0e0e0; border: 1px solid #ccc; padding: 6px; }
QTreeWidget { background: #fff; color: #333; }
QTabBar::tab:selected { background: #6c8cd5; }
'''

HACKER_STYLE = '''
QWidget { background: #000; color: #0f0; font-family: Courier; font-weight: bold; }
QPushButton { background: #001100; border: 1px solid #0f0; padding: 6px; font-weight: bold; }
QTreeWidget { background: #000; color: #0f0; font-weight: bold; }
QTabBar::tab:selected { background: #0f0; }
'''
STYLE_LIST = [DARK_STYLE, LIGHT_STYLE, HACKER_STYLE]


def sh(cmd):
    subprocess.run(cmd, shell=True, check=True)

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_dir = Path.home()
        self.init_ui()
        self.populate_dirs(self.current_dir, self.dir_tree.invisibleRootItem())
        root = self.dir_tree.topLevelItem(0)
        if root:
            self.dir_tree.setCurrentItem(root)
            self.load_files(self.current_dir)

    def init_ui(self):
        layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()
        self.btn_delete = QPushButton('Delete Selected')
        self.btn_delete.clicked.connect(self.delete_selected)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        splitter = QSplitter(QtCore.Qt.Horizontal)
        self.dir_tree = QTreeWidget()
        self.dir_tree.setHeaderHidden(True)
        self.dir_tree.itemClicked.connect(self.on_dir_clicked)
        splitter.addWidget(self.dir_tree)

        right_splitter = QSplitter(QtCore.Qt.Vertical)
        self.file_list = QTreeWidget()
        self.file_list.setHeaderLabels(['Name', 'Size', 'Modified'])
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        right_splitter.addWidget(self.file_list)

        chart_widget = QWidget()
        chart_layout = QVBoxLayout(chart_widget)
        self.figure = Figure(figsize=(5,3), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas)
        right_splitter.addWidget(chart_widget)

        splitter.addWidget(right_splitter)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,3)
        layout.addWidget(splitter)

    def populate_dirs(self, path, parent):
        try:
            for p in sorted(path.iterdir()):
                if p.is_dir():
                    item = QTreeWidgetItem(parent, [p.name])
                    item.setData(0, QtCore.Qt.UserRole, str(p))
                    self.populate_dirs(p, item)
        except PermissionError:
            pass

    def on_dir_clicked(self, item, _):
        self.current_dir = Path(item.data(0, QtCore.Qt.UserRole))
        self.load_files(self.current_dir)

    def load_files(self, directory):
        self.file_list.clear()
        names, sizes = [], []
        for f in sorted(directory.iterdir(), key=lambda x: x.stat().st_size, reverse=True)[:10]:
            if f.is_file():
                size_kb = f.stat().st_size / 1024
                names.append(f.name)
                sizes.append(size_kb)
                item = QTreeWidgetItem([
                    f.name,
                    f"{size_kb:.1f} KB",
                    datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                ])
                cat = next((c for c, exts in FILE_CATEGORIES.items() if f.suffix.lower() in exts), 'Others')
                item.setForeground(0, QtGui.QBrush(CATEGORY_COLORS[cat]))
                self.file_list.addTopLevelItem(item)
        self.figure.clear()
        if sizes and sum(sizes) > 0:
            ax1 = self.figure.add_subplot(121)
            ax1.barh(range(len(sizes)), sizes)
            ax1.invert_yaxis()
            ax1.set_yticks(range(len(names)))
            ax1.set_yticklabels(names, fontsize=8)
            ax1.set_title('Big Files')
            ax2 = self.figure.add_subplot(122)
            ax2.pie(sizes, labels=names, autopct='%1.1f%%')
            ax2.set_title('Size Distribution')
        else:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No files to display', ha='center', va='center')
            ax.axis('off')
        self.canvas.draw()

    def delete_selected(self):
        items = self.file_list.selectedItems()
        if not items:
            QMessageBox.information(self, 'Delete', 'No files selected')
            return
        if QMessageBox.question(self, 'Delete', f'Delete {len(items)} files?') != QMessageBox.Yes:
            return
        for item in items:
            name = item.text(0)
            src = self.current_dir / name
            sh(f'mv "{src}" "{TRASH_DIR}/"')
            ts = datetime.now().strftime('%F %T')
            sh(f'echo "{ts} Removed: {src}" >> "{LOG_FILE}"')
            meta = TRASH_DIR / f"{name}.meta"
            sh(f'echo "{src.parent}" > "{meta}"')
        self.load_files(self.current_dir)

class RecycleBinPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()
        self.btn_restore = QPushButton('Restore Selected')
        self.btn_delete = QPushButton('Delete Permanently')
        self.btn_refresh = QPushButton('Refresh')
        self.btn_restore.clicked.connect(self.restore)
        self.btn_delete.clicked.connect(self.delete_permanently)
        self.btn_refresh.clicked.connect(self.load)
        btn_layout.addWidget(self.btn_restore)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)
        layout.addLayout(btn_layout)
        self.tbl = QTreeWidget()
        self.tbl.setHeaderLabels(['Name', 'Size', 'Deleted', 'Original'])
        self.tbl.setSelectionMode(QAbstractItemView.ExtendedSelection)
        layout.addWidget(self.tbl)
        self.load()

    def load(self):
        self.tbl.clear()
        for f in sorted(TRASH_DIR.iterdir()):
            if f.is_file() and not f.name.endswith('.meta'):
                deleted = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                size = f.stat().st_size
                size_str = f"{size//1024} KB" if size < 1024**2 else f"{size//1024**2} MB"
                meta = TRASH_DIR / f"{f.name}.meta"
                orig_path = meta.read_text().strip() if meta.exists() else str(Path.home())
                item = QTreeWidgetItem([f.name, size_str, deleted, orig_path])
                self.tbl.addTopLevelItem(item)

    def restore(self):
        items = self.tbl.selectedItems()
        if not items:
            QMessageBox.information(self, 'Restore', 'No items selected')
            return
        for item in items:
            name = item.text(0)
            meta = TRASH_DIR / f"{name}.meta"
            dest = Path(meta.read_text().strip()) if meta.exists() else Path.home()
            sh(f'mv "{TRASH_DIR / name}" "{dest / name}"')
        self.load()

    def delete_permanently(self):
        items = self.tbl.selectedItems()
        if not items:
            QMessageBox.information(self, 'Delete', 'No items selected')
            return
        if QMessageBox.question(self, 'Delete', f'Permanently delete {len(items)} files?') != QMessageBox.Yes:
            return
        for item in items:
            name = item.text(0)
            sh(f'rm -f "{TRASH_DIR / name}"')
            sh(f'rm -f "{TRASH_DIR / name}.meta"')
        self.load()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('rm-rf-regret')
        self.theme_index = 0
        toolbar = self.addToolBar('Main')
        toolbar.addAction(QAction('Refresh', self, triggered=self.refresh))
        toolbar.addAction(QAction('Toggle Theme', self, triggered=self.toggle_theme))
        tabs = QTabWidget()
        tabs.addTab(DashboardPage(), 'Dashboard')
        tabs.addTab(RecycleBinPage(), 'Recycle Bin')
        self.setCentralWidget(tabs)
        self.apply_theme()

    def apply_theme(self):
        self.setStyleSheet(STYLE_LIST[self.theme_index])

    def refresh(self):
        w = self.centralWidget().currentWidget()
        if hasattr(w, 'load_files'):
            w.load_files(w.current_dir)
        else:
            w.load()

    def toggle_theme(self):
        self.theme_index = (self.theme_index + 1) % len(STYLE_LIST)
        self.apply_theme()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
