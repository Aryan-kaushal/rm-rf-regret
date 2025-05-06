#!/usr/bin/env python3
import sys
import shutil
from pathlib import Path
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox,
    QAction, QTabWidget, QSplitter
)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Constants
TRASH_DIR = Path.home() / '.rm_rf_trash'
TRASH_DIR.mkdir(exist_ok=True)

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
QWidget { background: #121212; color: #e0e0e0; font: 15px Sans; }
QPushButton { background: #1f1f1f; border: 1px solid #333; border-radius: 4px; padding: 8px; }
QPushButton:hover { background: #2a2a2a; }
QTreeWidget { background: #1e1e1e; color: #e0e0e0; alternate-background-color: #252525; }
QSplitter::handle { background: #333; }
QTabBar::tab:selected { background: #3a6ff3; }
'''

LIGHT_STYLE = '''
QWidget { background: #fafafa; color: #333; font: 15px Sans; }
QPushButton { background: #e0e0e0; border: 1px solid #ccc; border-radius: 4px; padding: 8px; }
QPushButton:hover { background: #dddddd; }
QTreeWidget { background: #fff; color: #333; alternate-background-color: #f0f0f0; }
QSplitter::handle { background: #bbb; }
QTabBar::tab:selected { background: #6c8cd5; }
'''

HACKER_STYLE = '''
QWidget { background: #000; color: #0f0; font-family: Courier New; }
QPushButton { background: #001100; border: 1px solid #0f0; border-radius: 4px; padding: 8px; }
QPushButton:hover { background: #002200; }
QTreeWidget { background: #000; color: #0f0; alternate-background-color: #003300; }
QSplitter::handle { background: #0f0; }
QTabBar::tab:selected { background: #0f0; }
'''

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
        # Top controls
        ctrl_layout = QHBoxLayout()
        self.btn_delete = QPushButton('Delete Selected')
        self.btn_delete.clicked.connect(self.delete_selected)
        ctrl_layout.addStretch()
        ctrl_layout.addWidget(self.btn_delete)
        layout.addLayout(ctrl_layout)

        # Main splitter: left tree and right area
        main_splitter = QSplitter(QtCore.Qt.Horizontal)
        # Directory tree on left
        self.dir_tree = QTreeWidget()
        self.dir_tree.setHeaderHidden(True)
        self.dir_tree.itemClicked.connect(self.on_dir_clicked)
        main_splitter.addWidget(self.dir_tree)
        # Right splitter: file list above, chart below
        right_splitter = QSplitter(QtCore.Qt.Vertical)
        # File list
        self.file_list = QTreeWidget()
        self.file_list.setHeaderLabels(['Name', 'Size', 'Modified'])
        right_splitter.addWidget(self.file_list)
        # Chart area
        chart_box = QWidget()
        chart_layout = QVBoxLayout(chart_box)
        self.figure = Figure(figsize=(6, 4), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas)
        right_splitter.addWidget(chart_box)
        right_splitter.setStretchFactor(0, 3)
        right_splitter.setStretchFactor(1, 2)
        main_splitter.addWidget(right_splitter)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 3)
        layout.addWidget(main_splitter)

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

        # gather top-10 files by size
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
                cat = next(
                    (c for c, exts in FILE_CATEGORIES.items() if f.suffix.lower() in exts),
                    'Others'
                )
                item.setForeground(0, QtGui.QBrush(CATEGORY_COLORS.get(cat)))
                self.file_list.addTopLevelItem(item)

        # redraw chart
        self.figure.clear()
        if any(sizes):
            # bar chart
            ax1 = self.figure.add_subplot(121)
            ax1.barh(range(len(sizes)), sizes)
            ax1.invert_yaxis()
            ax1.set_yticks(range(len(names)))
            ax1.set_yticklabels(names, fontsize=8)
            ax1.set_title('Big Files')

            # pie chart
            ax2 = self.figure.add_subplot(122)
            ax2.pie(sizes, labels=names, autopct='%1.1f%%')
            ax2.set_title('Size Distribution')
        else:
            # placeholder for empty/no-size data
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No files to display',
                    ha='center', va='center', fontsize=12)
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
            file_name = item.text(0)
            fpath = self.current_dir / file_name
            meta = TRASH_DIR / (fpath.name + '.meta')
            meta.write_text(str(fpath.parent))
            shutil.move(str(fpath), str(TRASH_DIR / fpath.name))
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
        layout.addWidget(self.tbl)
        self.load()

    def load(self):
        self.tbl.clear()
        for f in sorted(TRASH_DIR.iterdir()):
            if f.is_file() and not f.name.endswith('.meta'):
                deleted = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                size = f.stat().st_size
                size_str = f"{size//1024} KB" if size < 1024**2 else f"{size//1024**2} MB"
                meta = TRASH_DIR / (f.name + '.meta')
                orig = meta.read_text().strip() if meta.exists() else ''
                item = QTreeWidgetItem([f.name, size_str, deleted, orig])
                self.tbl.addTopLevelItem(item)

    def restore(self):
        items = self.tbl.selectedItems()
        if not items:
            QMessageBox.information(self, 'Restore', 'No items selected')
            return
        for item in items:
            fp = TRASH_DIR / item.text(0)
            meta = TRASH_DIR / (fp.name + '.meta')
            dest = Path(meta.read_text().strip()) if meta.exists() else Path.home()
            shutil.move(str(fp), str(dest / fp.name))
        self.load()

    def delete_permanently(self):
        items = self.tbl.selectedItems()
        if not items:
            QMessageBox.information(self, 'Delete', 'No items selected')
            return
        if QMessageBox.question(self, 'Delete', f'Permanently delete {len(items)} files?') != QMessageBox.Yes:
            return
        for item in items:
            fp = TRASH_DIR / item.text(0)
            fp.unlink(missing_ok=True)
            meta = TRASH_DIR / (fp.name + '.meta')
            meta.unlink(missing_ok=True)
        self.load()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('rm-rf-regret')
        toolbar = self.addToolBar('Main')
        toolbar.addAction(QAction('Refresh', self, triggered=self.refresh))
        toolbar.addAction(QAction('Toggle Theme', self, triggered=self.toggle_theme))

        tabs = QTabWidget()
        tabs.addTab(DashboardPage(), 'Dashboard')
        tabs.addTab(RecycleBinPage(), 'Recycle Bin')
        self.setCentralWidget(tabs)
        self.setStyleSheet(DARK_STYLE)

    def refresh(self):
        current = self.centralWidget().currentWidget()
        if hasattr(current, 'load_files'):
            current.load_files(current.current_dir)
        elif hasattr(current, 'load'):
            current.load()

    def toggle_theme(self):
        current = self.styleSheet()
        if current == DARK_STYLE:
            self.setStyleSheet(LIGHT_STYLE)
        elif current == LIGHT_STYLE:
            self.setStyleSheet(HACKER_STYLE)
        else:
            self.setStyleSheet(DARK_STYLE)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
