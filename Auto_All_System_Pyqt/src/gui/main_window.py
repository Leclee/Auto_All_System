"""
@file main_window.py
@brief 主窗口框架
@details 多业务管理系统的主窗口，支持Google、Microsoft、Facebook、Telegram等多个业务专区
"""

import sys
import os
import time

# 确保src目录在路径中（支持直接运行）
_current_dir = os.path.dirname(os.path.abspath(__file__))
_src_dir = os.path.dirname(_current_dir)
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QSplitter,
    QAbstractItemView, QSpinBox, QToolBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QIcon

# 使用绝对导入（支持直接运行和作为模块导入）
try:
    from gui.base_window import resource_path, get_data_path
except ImportError:
    from base_window import resource_path, get_data_path


class MainWindow(QMainWindow):
    """
    @brief 主窗口框架类
    @details 提供多业务管理的主界面框架，包含：
    - 左侧功能工具箱（按业务分区）
    - 中间控制面板和浏览器列表
    - 右侧运行状态日志
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("比特浏览器窗口管理工具")
        self.resize(1300, 800)
        
        # 设置窗口图标
        self._set_icon()
        
        # 初始化数据库
        self._init_database()
        
        # 初始化UI
        self._init_function_panel()
        self._init_ui()
        
        # 加载初始数据
        QTimer.singleShot(100, self._on_startup)
    
    def _set_icon(self):
        """设置窗口图标"""
        try:
            icon_path = resource_path("beta-1.svg")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass
    
    def _init_database(self):
        """初始化数据库"""
        try:
            from core.database import DBManager
            DBManager.init_db()
        except ImportError:
            try:
                _legacy_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_legacy')
                if _legacy_dir not in sys.path:
                    sys.path.insert(0, _legacy_dir)
                from database import DBManager
                DBManager.init_db()
            except Exception as e:
                print(f"[警告] 数据库初始化失败: {e}")
    
    def _init_function_panel(self):
        """初始化左侧功能工具箱"""
        self.function_panel = QWidget()
        self.function_panel.setFixedWidth(250)
        self.function_panel.setVisible(False)  # 默认隐藏
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.function_panel.setLayout(layout)
        
        # 标题
        title = QLabel("🔥 功能工具箱")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(title)
        
        # 分区工具箱
        self.toolbox = QToolBox()
        self.toolbox.setStyleSheet("""
            QToolBox::tab {
                background: #e1e1e1;
                border-radius: 5px;
                color: #555;
                font-weight: bold;
            }
            QToolBox::tab:selected {
                background: #d0d0d0;
                color: black;
            }
        """)
        layout.addWidget(self.toolbox)
        
        # --- Google 专区 ---
        google_page = self._create_google_panel()
        self.toolbox.addItem(google_page, "Google 专区")
        
        # --- Microsoft 专区 ---
        ms_page = self._create_microsoft_panel()
        self.toolbox.addItem(ms_page, "Microsoft 专区")
        
        # --- Facebook 专区 ---
        fb_page = self._create_facebook_panel()
        self.toolbox.addItem(fb_page, "Facebook 专区")
        
        # --- Telegram 专区 ---
        tg_page = self._create_telegram_panel()
        self.toolbox.addItem(tg_page, "Telegram 专区")
        
        # 默认展开Google
        self.toolbox.setCurrentIndex(0)
    
    def _create_google_panel(self) -> QWidget:
        """创建Google专区面板"""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 10, 5, 10)
        
        # 一键获取SheerLink
        btn_sheerlink = QPushButton("一键获取 G-SheerLink")
        btn_sheerlink.setFixedHeight(40)
        btn_sheerlink.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sheerlink.setStyleSheet("""
            QPushButton {
                text-align: left; 
                padding-left: 15px; 
                font-weight: bold; 
                color: white;
                background-color: #4CAF50;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        btn_sheerlink.clicked.connect(self._action_get_sheerlink)
        layout.addWidget(btn_sheerlink)
        
        # 批量验证SheerID
        btn_verify = QPushButton("批量验证 SheerID Link")
        btn_verify.setFixedHeight(40)
        btn_verify.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_verify.setStyleSheet("""
            QPushButton {
                text-align: left; 
                padding-left: 15px; 
                font-weight: bold; 
                color: white;
                background-color: #2196F3;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        btn_verify.clicked.connect(self._action_verify_sheerid)
        layout.addWidget(btn_verify)
        
        # 一键绑卡订阅
        btn_bind = QPushButton("🔗 一键绑卡订阅")
        btn_bind.setFixedHeight(40)
        btn_bind.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_bind.setStyleSheet("""
            QPushButton {
                text-align: left; 
                padding-left: 15px; 
                font-weight: bold; 
                color: white;
                background-color: #FF9800;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #F57C00; }
        """)
        btn_bind.clicked.connect(self._action_bind_card)
        layout.addWidget(btn_bind)
        
        # 一键全自动处理
        btn_auto = QPushButton("🚀 一键全自动处理")
        btn_auto.setFixedHeight(40)
        btn_auto.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_auto.setStyleSheet("""
            QPushButton {
                text-align: left; 
                padding-left: 15px; 
                font-weight: bold; 
                color: white;
                background-color: #9C27B0;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #7B1FA2; }
        """)
        btn_auto.clicked.connect(self._action_auto_all)
        layout.addWidget(btn_auto)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def _create_microsoft_panel(self) -> QWidget:
        """创建Microsoft专区面板"""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 10, 5, 10)
        
        label = QLabel("🔧 功能开发中...")
        label.setStyleSheet("color: #666; padding: 20px;")
        layout.addWidget(label)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def _create_facebook_panel(self) -> QWidget:
        """创建Facebook专区面板"""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 10, 5, 10)
        
        label = QLabel("🔧 功能开发中...")
        label.setStyleSheet("color: #666; padding: 20px;")
        layout.addWidget(label)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def _create_telegram_panel(self) -> QWidget:
        """创建Telegram专区面板"""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 10, 5, 10)
        
        label = QLabel("🔧 功能开发中...")
        label.setStyleSheet("color: #666; padding: 20px;")
        layout.addWidget(label)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def _init_ui(self):
        """初始化主界面UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(5)
        main_widget.setLayout(main_layout)
        
        # 1. 左侧功能面板
        main_layout.addWidget(self.function_panel)
        
        # 2. 中间区域（控制面板 + 浏览器列表）
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        
        # 顶部栏
        top_bar = self._create_top_bar()
        left_layout.addLayout(top_bar)
        
        # 创建参数配置
        config_group = self._create_config_group()
        left_layout.addWidget(config_group)
        
        # 操作按钮
        action_buttons = self._create_action_buttons()
        left_layout.addLayout(action_buttons)
        
        # 浏览器列表
        browser_group = self._create_browser_list_group()
        left_layout.addWidget(browser_group)
        
        # 3. 右侧日志区域
        right_widget = self._create_log_panel()
        
        # 使用分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
    
    def _create_top_bar(self) -> QHBoxLayout:
        """创建顶部栏"""
        layout = QHBoxLayout()
        
        # 工具箱切换按钮
        self.btn_toggle_tools = QPushButton("工具箱 📂")
        self.btn_toggle_tools.setCheckable(True)
        self.btn_toggle_tools.setChecked(False)
        self.btn_toggle_tools.setFixedHeight(30)
        self.btn_toggle_tools.setStyleSheet("""
            QPushButton { background-color: #607D8B; color: white; border-radius: 4px; padding: 5px 10px; }
            QPushButton:checked { background-color: #455A64; }
        """)
        self.btn_toggle_tools.clicked.connect(lambda checked: self.function_panel.setVisible(checked))
        layout.addWidget(self.btn_toggle_tools)
        
        # 标题
        title_label = QLabel("控制面板")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setContentsMargins(10, 0, 10, 0)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # 全局并发数
        layout.addWidget(QLabel("🔥 全局并发数:"))
        self.thread_spinbox = QSpinBox()
        self.thread_spinbox.setRange(1, 50)
        self.thread_spinbox.setValue(1)
        self.thread_spinbox.setFixedSize(70, 30)
        self.thread_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thread_spinbox.setStyleSheet("font-size: 14px; font-weight: bold; color: #E91E63;")
        layout.addWidget(self.thread_spinbox)
        
        return layout
    
    def _create_config_group(self) -> QGroupBox:
        """创建参数配置区"""
        group = QGroupBox("创建参数配置")
        layout = QVBoxLayout()
        
        # 模板窗口ID
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("模板窗口ID:"))
        self.template_input = QLineEdit()
        self.template_input.setPlaceholderText("请输入模板窗口ID")
        row1.addWidget(self.template_input)
        layout.addLayout(row1)
        
        # 窗口前缀
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("窗口前缀:"))
        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("可选，默认按模板名或'默认模板'命名")
        row2.addWidget(self.prefix_input)
        layout.addLayout(row2)
        
        # 平台URL
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("平台URL:"))
        self.platform_input = QLineEdit()
        self.platform_input.setPlaceholderText("可选，平台URL")
        row3.addWidget(self.platform_input)
        layout.addLayout(row3)
        
        # 额外URL
        row4 = QHBoxLayout()
        row4.addWidget(QLabel("额外URL:"))
        self.extra_url_input = QLineEdit()
        self.extra_url_input.setPlaceholderText("可选，逗号分隔")
        row4.addWidget(self.extra_url_input)
        layout.addLayout(row4)
        
        # 统计信息
        stats_layout = QHBoxLayout()
        self.stats_accounts = QLabel("📋 待创建窗口账号: 0")
        self.stats_proxies = QLabel("📡 可用代理: 0")
        stats_layout.addWidget(self.stats_accounts)
        stats_layout.addWidget(self.stats_proxies)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_action_buttons(self) -> QHBoxLayout:
        """创建操作按钮"""
        layout = QHBoxLayout()
        
        # 开始创建（模板）
        self.btn_create_template = QPushButton("开始根据模板创建窗口")
        self.btn_create_template.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        self.btn_create_template.clicked.connect(self._start_creation_template)
        layout.addWidget(self.btn_create_template)
        
        # 使用默认模板创建
        self.btn_create_default = QPushButton("使用默认模板创建")
        self.btn_create_default.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.btn_create_default.clicked.connect(self._start_creation_default)
        layout.addWidget(self.btn_create_default)
        
        # 停止
        self.btn_stop = QPushButton("停止任务")
        self.btn_stop.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 10px;")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self._stop_task)
        layout.addWidget(self.btn_stop)
        
        return layout
    
    def _create_browser_list_group(self) -> QGroupBox:
        """创建浏览器列表区域"""
        group = QGroupBox("现有窗口列表")
        layout = QVBoxLayout()
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        self.btn_refresh = QPushButton("刷新列表")
        self.btn_refresh.clicked.connect(self._refresh_browser_list)
        toolbar.addWidget(self.btn_refresh)
        
        self.btn_refresh_2fa = QPushButton("刷新并保存验证码")
        self.btn_refresh_2fa.clicked.connect(self._refresh_2fa)
        toolbar.addWidget(self.btn_refresh_2fa)
        
        self.cb_select_all = QCheckBox("全选")
        self.cb_select_all.stateChanged.connect(self._toggle_select_all)
        toolbar.addWidget(self.cb_select_all)
        
        toolbar.addStretch()
        
        self.btn_open = QPushButton("打开选中窗口")
        self.btn_open.setStyleSheet("color: #2196F3;")
        self.btn_open.clicked.connect(self._open_selected_browsers)
        toolbar.addWidget(self.btn_open)
        
        self.btn_delete = QPushButton("删除选中窗口")
        self.btn_delete.setStyleSheet("color: #f44336;")
        self.btn_delete.clicked.connect(self._delete_selected_browsers)
        toolbar.addWidget(self.btn_delete)
        
        layout.addLayout(toolbar)
        
        # 浏览器表格
        self.browser_table = QTableWidget()
        self.browser_table.setColumnCount(5)
        self.browser_table.setHorizontalHeaderLabels(["选择", "名称", "窗口ID", "2FA验证码", "备注"])
        self.browser_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.browser_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.browser_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.browser_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.browser_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.browser_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        layout.addWidget(self.browser_table)
        
        group.setLayout(layout)
        return group
    
    def _create_log_panel(self) -> QWidget:
        """创建日志面板"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # 标题
        title = QLabel("运行状态日志")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 日志文本框
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #1e1e1e; color: #dcdcdc; font-family: Consolas;")
        layout.addWidget(self.log_text)
        
        # 清除日志按钮
        btn_clear = QPushButton("清除日志")
        btn_clear.clicked.connect(lambda: self.log_text.clear())
        layout.addWidget(btn_clear)
        
        return widget
    
    # ==================== 事件处理 ====================
    
    def _on_startup(self):
        """启动时执行"""
        self._refresh_browser_list()
        self._check_files()
    
    def _check_files(self):
        """检查数据库状态"""
        try:
            from core.database import DBManager
            accounts = DBManager.get_accounts_without_browser()
            proxies = DBManager.get_available_proxies()
            self.stats_accounts.setText(f"📋 待创建窗口账号: {len(accounts)}")
            self.stats_proxies.setText(f"📡 可用代理: {len(proxies)}")
        except Exception as e:
            self.log(f"检查数据库状态失败: {e}")
    
    def log(self, message: str):
        """添加日志"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _refresh_browser_list(self):
        """刷新浏览器列表"""
        self.log("正在刷新窗口列表...")
        # TODO: 实现刷新逻辑
        self.log("列表刷新完成")
    
    def _refresh_2fa(self):
        """刷新并保存2FA验证码"""
        self.log("正在刷新2FA验证码...")
        # TODO: 实现2FA刷新逻辑
    
    def _toggle_select_all(self, state):
        """全选/取消全选"""
        is_checked = (state == Qt.CheckState.Checked.value)
        for row in range(self.browser_table.rowCount()):
            item = self.browser_table.item(row, 0)
            if item:
                item.setCheckState(Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked)
    
    def _open_selected_browsers(self):
        """打开选中的浏览器"""
        self.log("正在打开选中的窗口...")
        # TODO: 实现打开逻辑
    
    def _delete_selected_browsers(self):
        """删除选中的浏览器"""
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除选中的窗口吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.log("正在删除选中的窗口...")
            # TODO: 实现删除逻辑
    
    def _start_creation_template(self):
        """使用模板创建窗口"""
        template_id = self.template_input.text().strip()
        if not template_id:
            QMessageBox.warning(self, "提示", "请输入模板窗口ID")
            return
        self.log(f"开始使用模板 {template_id} 创建窗口...")
        # TODO: 实现创建逻辑
    
    def _start_creation_default(self):
        """使用默认模板创建窗口"""
        self.log("开始使用默认模板创建窗口...")
        # TODO: 实现创建逻辑
    
    def _stop_task(self):
        """停止当前任务"""
        self.log("正在停止任务...")
        # TODO: 实现停止逻辑
    
    # ==================== Google专区功能 ====================
    
    def _action_get_sheerlink(self):
        """一键获取SheerLink"""
        self.log("开始获取SheerLink...")
        # TODO: 实现获取逻辑
    
    def _action_verify_sheerid(self):
        """打开SheerID验证窗口"""
        try:
            from google.frontend import SheerIDWindow
            self.sheerid_window = SheerIDWindow(self)
            self.sheerid_window.show()
        except Exception as e:
            self.log(f"打开SheerID验证窗口失败: {e}")
            QMessageBox.warning(self, "错误", f"打开窗口失败: {e}")
    
    def _action_bind_card(self):
        """打开绑卡订阅窗口"""
        try:
            from google.frontend import BindCardWindow
            self.bind_card_window = BindCardWindow()
            self.bind_card_window.show()
        except Exception as e:
            self.log(f"打开绑卡窗口失败: {e}")
            QMessageBox.warning(self, "错误", f"打开窗口失败: {e}")
    
    def _action_auto_all(self):
        """打开一键全自动处理窗口"""
        try:
            from google.frontend import AutoAllInOneWindow
            if AutoAllInOneWindow:
                self.auto_all_window = AutoAllInOneWindow()
                self.auto_all_window.show()
            else:
                QMessageBox.warning(self, "提示", "功能模块未加载")
        except Exception as e:
            self.log(f"打开一键全自动窗口失败: {e}")
            QMessageBox.warning(self, "错误", f"打开窗口失败: {e}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
