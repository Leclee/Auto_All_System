"""
@file main.py
@brief 程序主入口
@details Auto_All_System_Pyqt 应用程序入口点
"""
import sys
import os

# 确保src目录在路径中
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# 确保_legacy目录也在路径中（兼容旧模块）
LEGACY_DIR = os.path.join(SRC_DIR, '_legacy')
if LEGACY_DIR not in sys.path:
    sys.path.insert(0, LEGACY_DIR)

# 初始化核心模块
try:
    from core.database import DBManager
except ImportError:
    from database import DBManager

DBManager.init_db()


def run_gui():
    """
    @brief 运行主GUI界面
    """
    from PyQt6.QtWidgets import QApplication
    
    # 使用新的主窗口
    try:
        from gui.main_window import MainWindow
    except ImportError:
        # 回退到旧版
        try:
            from google.frontend import BrowserWindowCreatorGUI as MainWindow
        except ImportError:
            from create_window_gui import BrowserWindowCreatorGUI as MainWindow
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


def run_web_admin(port=8080):
    """
    @brief 运行Web管理界面
    @param port 服务器端口
    """
    try:
        from web.server import run_server
    except ImportError:
        try:
            from web_admin.server import run_server
        except ImportError:
            print("[警告] web_admin 模块导入失败: No module named 'web_admin'")
            return
    
    run_server(port)


def main():
    """
    @brief 主函数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto All System PyQt')
    parser.add_argument('--web', action='store_true', help='启动Web管理界面')
    parser.add_argument('--port', type=int, default=8080, help='Web服务器端口')
    
    args = parser.parse_args()
    
    if args.web:
        run_web_admin(args.port)
    else:
        run_gui()


if __name__ == '__main__':
    main()

