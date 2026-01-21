"""
@file __init__.py
@brief 谷歌业务后端模块
@details 包含谷歌账号自动化的核心业务逻辑

已迁移模块:
- account_manager: 账号状态管理
- sheerid_verifier: SheerID链接验证
- google_auth: Google登录状态检测
- google_login_service: Google登录服务
- sheerlink_service: SheerLink提取服务
"""

from .sheerid_verifier import SheerIDVerifier
from .account_manager import AccountManager
from .google_auth import (
    GoogleLoginStatus,
    check_google_login_status,
    is_logged_in,
    navigate_and_check_login,
    google_login,
    check_google_one_status,
)
from .google_login_service import (
    GoogleLoginService,
    login_google_account,
    check_browser_login_status,
    quick_login_check,
)
from .sheerlink_service import (
    SheerLinkService,
    process_browser,
    extract_sheerlink_batch,
)

# 待迁移的模块 - 目前从旧位置导入
try:
    import sys
    import os
    _src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    _legacy_dir = os.path.join(_src_dir, '_legacy')
    if _legacy_dir not in sys.path:
        sys.path.insert(0, _legacy_dir)
    
    from auto_bind_card import auto_bind_card, check_and_login
except ImportError as e:
    print(f"[google.backend] 部分模块导入失败: {e}")
    auto_bind_card = check_and_login = None

__all__ = [
    # 已迁移模块 - 核心类
    'SheerIDVerifier',
    'AccountManager',
    'GoogleLoginService',
    'SheerLinkService',
    # 登录状态
    'GoogleLoginStatus',
    'check_google_login_status',
    'is_logged_in',
    'navigate_and_check_login',
    'google_login',
    'check_google_one_status',
    # 登录服务便捷函数
    'login_google_account',
    'check_browser_login_status',
    'quick_login_check',
    # SheerLink服务
    'process_browser',
    'extract_sheerlink_batch',
    # 待迁移模块
    'auto_bind_card',
    'check_and_login',
]

