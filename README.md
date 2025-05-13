# 🧹 RM-RF-REGRET

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://riverbankcomputing.com/software/pyqt)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5+-orange.svg)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/Aryan-kaushal/rm-rf-regret/graphs/commit-activity)

<div align="center">
  <img src="https://raw.githubusercontent.com/Aryan-kaushal/rm-rf-regret/main/docs/logo.png" alt="RM-RF-REGRET Logo" width="250"/>
  <br>
  <em>Because everyone deserves a second chance after rm -rf</em>
</div>

---

---

## 🚀 Project Overview

**RM-RF-REGRET** is a safe, user-friendly file management utility for Linux that helps you reclaim disk space without fear of permanently losing important data.

Inspired by the anxiety that comes after running `rm -rf` commands, this tool implements a recoverable deletion system with an intuitive graphical interface and insightful disk usage analytics.

---

## ✨ Key Features

### 🛡️ Safe File Operations

* **Reversible Deletions**: Files are moved to a hidden trash directory (`~/.rm-rf-regret/trash`) instead of being permanently deleted
* **Metadata Preservation**: Original file paths are stored for perfect restoration
* **Comprehensive Logging**: All operations are logged with timestamps for auditing

### 📊 Powerful Analytics

* **Visual File Size Distribution**: Interactive charts show disk usage patterns
* **Category-Based Analysis**: Files automatically categorized by type (documents, images, videos, etc.)
* **Large File Detection**: Quickly identify space-hogging files

### 🖥️ Intuitive Interface

* **Dual-Pane Explorer**: Directory tree on left, file list on right
* **Multi-Selection Support**: Perform operations on multiple files simultaneously
* **Real-Time Updates**: Interface refreshes automatically after operations

### 🎨 Customization

* **Multiple Themes**: Choose between Dark, Light, and Hacker themes
* **Responsive Layout**: Adapts to your window size and preferences

---

## 🖼️ Screenshots

<div align="center">
  <img src="https://raw.githubusercontent.com/Aryan-kaushal/rm-rf-regret/main/docs/dashboard.png" alt="Dashboard View" width="45%"/>
  <img src="https://raw.githubusercontent.com/Aryan-kaushal/rm-rf-regret/main/docs/trash.png" alt="Trash View" width="45%"/>
  <br>
  <em>Left: Dashboard view with file analytics | Right: Trash bin with restore options</em>
</div>

---

---

## ⚙️ Installation

### Prerequisites

* Python 3.8 or higher
* PyQt5
* Matplotlib

### Method 1: From PyPI (Recommended)

```bash
pip install rm-rf-regret
```

### Method 2: From Source

```bash
# Clone the repository
git clone https://github.com/Aryan-kaushal/rm-rf-regret.git
cd rm-rf-regret

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Graphical Interface

```bash
# If installed via pip
rm-rf-regret

# If installed from source
python prj.py
```

### Command-Line Interface

```bash
# Show help
python cleaner.py --help

# Scan and visualize a specific directory
python cleaner.py --path ~/Documents

# Move all files from a directory to trash
python cleaner.py --path ~/Downloads --delete-all

# Restore a specific file from trash
python cleaner.py --restore important_document.pdf

# Permanently empty trash
python cleaner.py --purge-trash

# Analyze disk usage in current directory
python cleaner.py --analyze
```

---

## 🧰 Technical Details

### Architecture

RM-RF-REGRET follows a modular architecture with clear separation of concerns:

* **UI Layer**: PyQt5-based interface with responsive design
* **Business Logic**: Core file operations and analytics processing
* **Data Layer**: File system interaction and metadata management

### Directory Structure

```
~/.rm-rf-regret/
├── trash/        # Where deleted files are stored
│   ├── file1
│   ├── file1.meta  # Contains original path information
│   └── ...
└── log.txt       # Operation logs with timestamps
```

### Safeguards

* Confirmation dialogs prevent accidental deletions
* Self-healing error handling prevents data loss
* Background backup of metadata files

---

## 🔄 Workflow Examples

### Data Clean-Up Workflow

1. Launch RM-RF-REGRET
2. Navigate to a storage-heavy directory
3. Use the bar chart to identify large files
4. Select unnecessary files and click "Delete Selected"
5. Files are moved to the Trash bin (not permanently deleted)
6. Review deleted files in the Trash tab anytime
7. Restore files if needed or permanently delete them

### File Recovery Workflow

1. Go to the "Recycle Bin" tab
2. Find your accidentally deleted files
3. Select files to recover
4. Click "Restore Selected"
5. Files are moved back to their original locations

---

## 🛠️ Development

### Requirements

* Python 3.8+
* PyQt5 5.15+
* Matplotlib 3.5+

### Setting Up Development Environment

```bash
# Clone repository with development branch
git clone -b develop https://github.com/Aryan-kaushal/rm-rf-regret.git
cd rm-rf-regret

# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Build from Source

```bash
python setup.py build
```

---

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

---

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👏 Acknowledgements

* Inspired by the anxiety of accidental `rm -rf` commands
* PyQt5 for providing excellent GUI capabilities
* The open-source community for continuous support and inspiration

---
