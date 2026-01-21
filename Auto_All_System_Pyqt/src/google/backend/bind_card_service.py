"""
@file bind_card_service.py
@brief 绑卡订阅服务模块
@details 自动绑定测试卡并完成Google One订阅
"""
import asyncio
from typing import Tuple, Optional, Callable
from playwright.async_api import async_playwright, Page


def get_card_from_db() -> dict:
    """
    @brief 从数据库获取可用的卡片信息
    @return 卡信息字典，若无可用卡则返回None
    """
    try:
        from core.database import DBManager
        cards = DBManager.get_available_cards()
        if cards:
            card = cards[0]
            return {
                'id': card.get('id'),
                'number': card.get('card_number', ''),
                'exp_month': card.get('exp_month', ''),
                'exp_year': card.get('exp_year', ''),
                'cvv': card.get('cvv', ''),
                'zip_code': card.get('zip_code', ''),
            }
    except Exception as e:
        print(f"[BindCard] 获取卡片失败: {e}")
    return None


def update_card_usage(card_id: int):
    """
    @brief 更新卡片使用次数
    @param card_id 卡片ID
    """
    try:
        from core.database import DBManager
        DBManager.increment_card_usage(card_id)
    except Exception as e:
        print(f"[BindCard] 更新卡片使用次数失败: {e}")


async def auto_bind_card(page: Page, card_info: dict = None, account_info: dict = None) -> Tuple[bool, str]:
    """
    @brief 自动绑卡订阅
    @param page Playwright页面对象
    @param card_info 卡信息字典 {'number', 'exp_month', 'exp_year', 'cvv'}
    @param account_info 账号信息(用于登录)
    @return (success, message)
    """
    # 优先从数据库获取卡片
    if card_info is None:
        card_info = get_card_from_db()
        if card_info is None:
            return False, "数据库中无可用卡片，请先在Web管理界面导入卡片"
    
    try:
        print("[BindCard] 开始自动绑卡流程...")
        
        # 等待页面加载
        await asyncio.sleep(3)
        
        # Step 1: 点击 "Get student offer" 按钮
        print("[BindCard] 步骤1: 查找Get student offer按钮...")
        try:
            selectors = [
                'button:has-text("Get student offer")',
                'button:has-text("Get offer")',
                'a:has-text("Get student offer")',
            ]
            
            for selector in selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        await element.click()
                        print(f"[BindCard] ✅ 已点击 'Get student offer'")
                        break
                except:
                    continue
            
            await asyncio.sleep(8)
        except Exception as e:
            print(f"[BindCard] Get student offer 点击失败: {e}")
        
        # Step 2: 检查是否已绑卡(订阅按钮是否出现)
        print("[BindCard] 步骤2: 检查是否已绑卡...")
        await asyncio.sleep(3)
        
        try:
            iframe_locator = page.frame_locator('iframe[src*="tokenized.play.google.com"]')
            
            subscribe_selectors = [
                'span.UywwFc-vQzf8d:has-text("Subscribe")',
                'span:has-text("Subscribe")',
            ]
            
            for selector in subscribe_selectors:
                try:
                    element = iframe_locator.locator(selector).first
                    if await element.count() > 0:
                        print("[BindCard] ✅ 账号已绑卡，直接订阅...")
                        await element.click()
                        await asyncio.sleep(10)
                        return await _check_subscription_status(page, account_info)
                except:
                    continue
        except:
            pass
        
        # Step 3: 切换到iframe并点击Add card
        print("[BindCard] 步骤3: 切换到iframe...")
        await asyncio.sleep(10)
        
        try:
            iframe_locator = page.frame_locator('iframe[src*="tokenized.play.google.com"]')
            print("[BindCard] ✅ 找到付款iframe")
            
            # 点击 Add card
            await asyncio.sleep(10)
            add_card_selectors = [
                'span.PjwEQ:has-text("Add card")',
                ':text("Add card")',
            ]
            
            for selector in add_card_selectors:
                try:
                    element = iframe_locator.locator(selector).first
                    if await element.count() > 0:
                        await element.click()
                        print("[BindCard] ✅ 已点击 'Add card'")
                        break
                except:
                    continue
            
            await asyncio.sleep(10)
            
            # 检查是否有第二层iframe
            try:
                inner_iframe = iframe_locator.frame_locator('iframe[name="hnyNZeIframe"]')
                test = inner_iframe.locator('body')
                if await test.count() >= 0:
                    iframe_locator = inner_iframe
                    print("[BindCard] ✅ 找到第二层iframe")
                    await asyncio.sleep(10)
            except:
                pass
            
        except Exception as e:
            return False, f"未找到付款iframe: {e}"
        
        # Step 4: 填写卡号
        print(f"[BindCard] 步骤4: 填写卡号 {card_info['number'][:4]}****")
        await asyncio.sleep(10)
        
        try:
            all_inputs = iframe_locator.locator('input')
            input_count = await all_inputs.count()
            print(f"[BindCard] 找到 {input_count} 个输入框")
            
            if input_count < 3:
                return False, f"输入框数量不足: {input_count}"
            
            # 填写卡号、过期日期、CVV
            await all_inputs.nth(0).click()
            await all_inputs.nth(0).fill(card_info['number'])
            print("[BindCard] ✅ 卡号已填写")
            
            await all_inputs.nth(1).click()
            await all_inputs.nth(1).fill(f"{card_info['exp_month']}{card_info['exp_year']}")
            print("[BindCard] ✅ 过期日期已填写")
            
            await all_inputs.nth(2).click()
            await all_inputs.nth(2).fill(card_info['cvv'])
            print("[BindCard] ✅ CVV已填写")
            
        except Exception as e:
            return False, f"填写卡信息失败: {e}"
        
        # Step 5: 点击 Save card
        print("[BindCard] 步骤5: 保存卡信息...")
        try:
            save_selectors = [
                'button:has-text("Save card")',
                'button:has-text("Save")',
            ]
            
            for selector in save_selectors:
                try:
                    element = iframe_locator.locator(selector).first
                    if await element.count() > 0:
                        await element.click()
                        print("[BindCard] ✅ 已点击 'Save card'")
                        break
                except:
                    continue
            
        except Exception as e:
            return False, f"保存卡失败: {e}"
        
        # Step 6: 点击订阅按钮
        print("[BindCard] 步骤6: 等待订阅页面...")
        await asyncio.sleep(18)
        
        try:
            iframe_locator = page.frame_locator('iframe[src*="tokenized.play.google.com"]')
            subscribe_selectors = [
                'span.UywwFc-vQzf8d:has-text("Subscribe")',
                'span:has-text("Subscribe")',
            ]
            
            for selector in subscribe_selectors:
                try:
                    element = iframe_locator.locator(selector).first
                    if await element.count() > 0:
                        await element.click()
                        print("[BindCard] ✅ 已点击订阅按钮")
                        break
                except:
                    continue
            
            await asyncio.sleep(10)
            
        except Exception as e:
            print(f"[BindCard] 订阅按钮点击失败: {e}")
        
        return await _check_subscription_status(page, account_info)
        
    except Exception as e:
        print(f"[BindCard] ❌ 绑卡失败: {e}")
        import traceback
        traceback.print_exc()
        return False, f"绑卡错误: {str(e)}"


async def _check_subscription_status(page: Page, account_info: dict = None) -> Tuple[bool, str]:
    """检查订阅状态"""
    try:
        iframe_locator = page.frame_locator('iframe[src*="tokenized.play.google.com"]')
        
        subscribed_selectors = [
            ':text("Subscribed")',
            'text=Subscribed',
        ]
        
        for selector in subscribed_selectors:
            try:
                element = iframe_locator.locator(selector).first
                if await element.count() > 0:
                    print("[BindCard] ✅ 检测到 'Subscribed'，订阅成功！")
                    
                    # 更新数据库状态
                    if account_info and account_info.get('email'):
                        try:
                            from core.database import DBManager
                            DBManager.update_account_status(account_info['email'], 'subscribed')
                        except:
                            pass
                    
                    return True, "绑卡订阅成功 (Subscribed)"
            except:
                continue
        
        return True, "绑卡已完成"
        
    except Exception as e:
        return True, f"绑卡已完成 (状态检查异常: {e})"


def process_bind_card(browser_id: str, card_info: dict = None, log_callback: Callable = None) -> Tuple[bool, str]:
    """
    @brief 处理单个浏览器的绑卡订阅
    @param browser_id 浏览器ID
    @param card_info 卡信息
    @param log_callback 日志回调
    @return (success, message)
    """
    def log(msg):
        print(msg)
        if log_callback:
            log_callback(msg)
    
    log("打开浏览器...")
    
    try:
        from core.bit_api import open_browser, close_browser, get_browser_info
        from core.database import DBManager
        from google.backend.google_auth import ensure_google_login
    except ImportError as e:
        return False, f"导入失败: {e}"
    
    # 获取账号信息
    account_info = None
    try:
        browser_info = get_browser_info(browser_id)
        if browser_info:
            remark = browser_info.get('remark', '')
            if '----' in remark:
                parts = remark.split('----')
                if len(parts) >= 4:
                    account_info = {
                        'email': parts[0].strip(),
                        'password': parts[1].strip(),
                        'backup': parts[2].strip(),
                        'secret': parts[3].strip()
                    }
    except:
        pass
    
    # 打开浏览器
    result = open_browser(browser_id)
    if not result.get('success'):
        return False, f"打开浏览器失败: {result.get('msg', '未知错误')}"
    
    ws_endpoint = result['data']['ws']
    
    async def _run():
        async with async_playwright() as playwright:
            try:
                browser = await playwright.chromium.connect_over_cdp(ws_endpoint)
                context = browser.contexts[0]
                page = context.pages[0] if context.pages else await context.new_page()
                
                # 导航到目标页面
                target_url = "https://one.google.com/ai-student?g1_landing_page=75"
                log("导航到Google One学生页面...")
                await page.goto(target_url, wait_until='domcontentloaded', timeout=30000)
                await asyncio.sleep(5)
                
                # 确保已登录
                if account_info:
                    log("检查登录状态...")
                    success, msg = await ensure_google_login(page, account_info)
                    if not success:
                        return False, f"登录失败: {msg}"
                    
                    # 重新导航
                    await page.goto(target_url, wait_until='domcontentloaded', timeout=30000)
                    await asyncio.sleep(5)
                
                # 执行绑卡
                return await auto_bind_card(page, card_info, account_info)
                
            except Exception as e:
                return False, str(e)
    
    return asyncio.run(_run())
