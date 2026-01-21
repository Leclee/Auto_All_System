# BitBrowser API 使用文档

## 概述

`src/core/bit_api.py` 是比特浏览器Local API的完整Python封装，基于官方文档 https://doc2.bitbrowser.cn/

## 特性

- ✅ 完全基于官方文档实现
- ✅ 使用标准HTTP POST + JSON body方式
- ✅ 封装所有浏览器窗口接口
- ✅ 提供BitBrowserAPI类和兼容函数接口
- ✅ 单例模式支持
- ✅ 完整的类型提示和文档注释

## 使用方式

###方式1: 使用BitBrowserAPI类（推荐）

```python
from core.bit_api import BitBrowserAPI

# 创建API实例
api = BitBrowserAPI()

# 健康检查
result = api.health_check()
print(result)  # {"success": True}

# 获取窗口列表
result = api.list_browsers(page=0, page_size=10)
if result['success']:
    browsers = result['data']['list']
    for browser in browsers:
        print(f"{browser['name']} - {browser['id']}")

# 创建窗口
result = api.create_browser(
    name="测试窗口",
    browser_fingerprint={"coreVersion": "130"},
    proxy_method=2,
    proxy_type="socks5",
    host="127.0.0.1",
    port=1080
)
if result['success']:
    browser_id = result['data']['id']
    print(f"创建成功: {browser_id}")

# 打开窗口
result = api.open_browser(browser_id, queue=True)
if result['success']:
    ws_url = result['data']['ws']
    print(f"WebSocket: {ws_url}")

# 关闭窗口
api.close_browser(browser_id)

# 删除窗口
api.delete_browser(browser_id)
```

### 方式2: 使用兼容函数接口

```python
from core.bit_api import openBrowser, closeBrowser, createBrowser, deleteBrowser

# 创建窗口
browser_id = createBrowser(
    name="测试窗口",
    browser_fingerprint={"coreVersion": "130"}
)

# 打开窗口
result = openBrowser(browser_id)

# 关闭窗口
closeBrowser(browser_id)

# 删除窗口
deleteBrowser(browser_id)
```

### 方式3: 使用单例模式

```python
from core.bit_api import get_api

# 获取全局API实例
api = get_api()

# 使用API
browsers = api.list_browsers(page=0, page_size=100)
```

## 主要接口

### 浏览器窗口管理

| 方法 | 说明 |
|------|------|
| `create_browser()` | 创建浏览器窗口 |
| `open_browser()` | 打开浏览器窗口 |
| `close_browser()` | 关闭浏览器窗口 |
| `delete_browser()` | 删除浏览器窗口 |
| `get_browser_detail()` | 获取窗口详情 |
| `list_browsers()` | 分页获取窗口列表 |
| `update_browser_partial()` | 批量修改窗口字段 |

### 窗口批量操作

| 方法 | 说明 |
|------|------|
| `update_browser_group()` | 批量修改分组 |
| `update_browser_proxy()` | 批量修改代理 |
| `update_browser_remark()` | 批量修改备注 |
| `delete_browsers()` | 批量删除（最多100个） |
| `close_browsers_by_seqs()` | 按序号批量关闭 |
| `close_all_browsers()` | 关闭所有窗口 |

### 窗口排列

| 方法 | 说明 |
|------|------|
| `arrange_windows()` | 排列窗口（宫格/对角线） |
| `arrange_windows_flexible()` | 一键自适应排列 |

### Cookie管理

| 方法 | 说明 |
|------|------|
| `get_browser_cookies()` | 获取实时cookie |
| `set_browser_cookies()` | 设置实时cookie |
| `clear_browser_cookies()` | 清空cookie |
| `format_cookies()` | 格式化cookie |

### 缓存管理

| 方法 | 说明 |
|------|------|
| `clear_browser_cache()` | 清理缓存（本地+云端） |
| `clear_cache_except_extensions()` | 清理缓存（保留扩展） |

### 进程管理

| 方法 | 说明 |
|------|------|
| `get_browser_pids()` | 获取窗口PID |
| `get_all_browser_pids()` | 获取所有PID |
| `get_alive_browser_pids()` | 获取活着的PID |
| `get_browser_ports()` | 获取调试端口 |
| `reset_closing_status()` | 重置关闭状态 |

### 工具接口

| 方法 | 说明 |
|------|------|
| `health_check()` | 健康检查 |
| `check_proxy()` | 代理检测 |
| `random_browser_fingerprint()` | 随机指纹 |
| `get_all_displays()` | 获取显示器列表 |
| `run_rpa_task()` | 执行RPA任务 |
| `stop_rpa_task()` | 停止RPA任务 |
| `auto_paste()` | 仿真输入 |
| `read_excel()` | 读取Excel |
| `read_file()` | 读取文本文件 |

## 创建窗口示例

### 创建Windows窗口 + Socks5代理

```python
api = BitBrowserAPI()

result = api.create_browser(
    name="Windows浏览器",
    proxy_method=2,  # 自定义代理
    proxy_type="socks5",
    host="1.2.3.4",
    port=1020,
    proxyUserName="user",
    proxyPassword="pass",
    browser_fingerprint={
        "coreVersion": "130",
        "ostype": "PC",
        "os": "Win32",
        "osVersion": "10"
    }
)

if result['success']:
    browser_id = result['data']['id']
    print(f"创建成功: {browser_id}")
```

### 创建随机指纹窗口

```python
# 只传空对象，系统自动随机所有指纹值
result = api.create_browser(
    name="随机指纹窗口",
    browser_fingerprint={}  # 空对象表示随机
)
```

### 启动参数示例

```python
# 无头模式
result = api.open_browser(
    browser_id,
    args=["--headless"]
)

# 无痕模式
result = api.open_browser(
    browser_id,
    args=["--incognito"]
)

# 多个参数
result = api.open_browser(
    browser_id,
    args=[
        "--remote-debugging-address=0.0.0.0",
        "--incognito",
        "--load-extension=/path/to/ext"
    ]
)
```

## 响应格式

所有接口返回JSON格式：

```python
# 成功
{
    "success": True,
    "data": {
        "id": "window_id",
        ...
    }
}

# 失败
{
    "success": False,
    "msg": "错误信息"
}
```

## 错误处理

```python
api = BitBrowserAPI()

result = api.open_browser(browser_id)
if result.get('success'):
    ws_url = result['data']['ws']
    print(f"打开成功: {ws_url}")
else:
    print(f"打开失败: {result.get('msg')}")
```

## 注意事项

1. **端口**: 默认Local Server端口为`54345`
2. **超时**: 打开窗口默认超时60秒，其他操作30秒
3. **队列模式**: 打开窗口时建议使用`queue=True`防止并发报错
4. **关闭窗口**: 关闭后等待5秒再进行删除/重新打开
5. **批量操作**: 批量删除最多100个窗口
6. **指纹对象**: 创建时必传，可以传空对象`{}`表示随机

## 在项目中使用

### 在GUI中使用

```python
from core.bit_api import BitBrowserAPI

class MainWindow:
    def __init__(self):
        self.api = BitBrowserAPI()
    
    def refresh_browser_list(self):
        result = self.api.list_browsers(page=0, page_size=1000)
        if result['success']:
            browsers = result['data']['list']
            # 更新UI
```

### 在自动化脚本中使用

```python
from core.bit_api import get_api

api = get_api()

# 获取所有窗口
result = api.list_browsers(page=0, page_size=100)
browsers = result['data']['list']

# 批量打开
for browser in browsers:
    browser_id = browser['id']
    api.open_browser(browser_id, queue=True)
```

## 迁移指南

从旧的`bitbrowser_api`迁移到新的`bit_api`：

```python
# 旧代码
from bitbrowser_api import BitBrowserAPI
api = BitBrowserAPI()
result = api.list_browsers(page=0, page_size=10)

# 新代码（完全相同）
from core.bit_api import BitBrowserAPI
api = BitBrowserAPI()
result = api.list_browsers(page=0, page_size=10)
```

---

*文档更新时间: 2026-01-21*
