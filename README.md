# BitBrowser Automation Tool (比特浏览器自动化管理工具)

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.12-blue.svg)

这是一个基于 Python/PyQt6 开发的比特浏览器（BitBrowser）自动化管理工具，支持批量创建窗口、自动分配代理、自动化提取 SheerID 验证链接以及账号资格检测等功能。
注意：后续有任何二开版本，只要是网页版，数据必然流经他人服务器，切勿将自己账号密码输入他人网页！！！
---

## 📢 广告 / Advertisement

🏆 **推荐使用比特浏览器 (BitBrowser)** - 专为跨境电商/社媒营销设计的指纹浏览器
👉 **[点击注册 / Register Here](https://www.bitbrowser.cn/?code=vl9b7j)**

*(通过此链接注册可获得官方支持与优惠)*

---

## ✨ 功能特性 (Features)

*   **批量窗口创建**: 
    *   **模板克隆**: 支持通过输入模板窗口 ID 进行克隆。
    *   **默认模板**: 内置通用配置模板，一键快速创建。
*   **智能命名**: 
    *   **自定义前缀**: 支持输入窗口名前缀 (如 "店铺A")，自动生成 "店铺A_1", "店铺A_2"。
    *   **自动序号**: 若不指定前缀，自动使用模板名称或 "默认模板" 加序号。
*   **自动化配置**: 自动读取 `accounts.txt` 和 `proxies.txt`，批量绑定账号与代理 IP。
*   **2FA 验证码管理**: 自动从浏览器备注或配置中提取密钥，批量生成并保存 2FA 验证码。
*   **SheerID 链接提取**: 
    *   全自动打开浏览器 -> 登录 Google -> 跳转活动页 -> 提取验证链接。
    *   **智能风控检测**: 自动识别 "此优惠目前不可用" (支持多语言) 或 6秒超时状态，自动分类存储无效账号。
*   **批量操作**: 支持批量打开、关闭、删除窗口。

## 🛠️ 安装与使用 (Installation & Usage)

### 方式一：直接运行 (推荐)
无需安装 Python 环境，直接下载 Release 中的 `.exe` 文件运行即可。

1. 下载 `BitBrowserAutoManager.exe`。
2. 在同级目录下准备好配置文件 (见下文)。
3. 双击运行程序。

### 方式二：源码运行
1. 克隆仓库:
   ```bash
   git clone https://github.com/yourusername/bitbrowser-auto-manager.git
   ```
2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```
3. 运行:
   ```bash
   python create_window_gui.py
   ```

## ⚙️ 配置文件说明 (Configuration)

请在程序运行目录下创建以下文件：

### 1. `accounts.txt` (账号信息)
格式：`邮箱----密码----辅助邮箱----2FA密钥`
```text
example1@gmail.com----Password123----recov1@email.com----SECRETKEY123
example2@gmail.com----Password456----recov2@email.com----SECRETKEY456
```

### 2. `proxies.txt` (代理IP)
支持 Socks5/HTTP，一行一个：
```text
socks5://user:pass@host:port
http://user:pass@host:port
```

### 3. 输出文件 (程序自动生成)
*   **sheerIDlink.txt**: 成功提取的验证链接。
*   **无资格号.txt**: 检测到无资格或超时的账号。
*   **2fa_codes.txt**: 生成的 2FA 验证码。

## 🤝 联系与交流 (Community)

有问题或建议？欢迎加入我们的社区！

| 💬 **Telegram 群组** | 🐧 **QQ 交流群** |
| :---: | :---: |
| [点击加入 / Join](https://t.me/+9zd3YE16NCU3N2Fl) | **QQ群号: 330544197** |
| ![Telegram QR](Telegram.png) | ![QQ QR](QQ.jpg) |

👤 **联系开发者**: QQ 2738552008
赞赏：![赞赏码](zanshang.jpg)
---

## ⚠️ 免责声明 (Disclaimer)

*   本工具仅供学习与技术交流使用，请勿用于非法用途。
*   请遵守比特浏览器及相关平台的使用条款。
*   开发者不对因使用本工具产生的任何账号损失或法律责任负责。

## 📄 License

This project is licensed under the [MIT License](LICENSE).
