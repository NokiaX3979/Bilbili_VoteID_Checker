"""
Bilibili VoteID 检查器
====================
连接本地 Chrome 浏览器，按用户指定开始结束范围依次查找标题，发起人，参与人数并保存到文本中

使用前请先以调试端口启动 Chrome：
  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
"""

import random
import re
import time
import os
from DrissionPage import ChromiumPage, ChromiumOptions

# ======================== 配置 ========================
TITLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "title.txt")
MIN_DELAY = 0          # 每次请求最小间隔（秒）
MAX_DELAY = 1          # 每次请求最大间隔（秒）
DEBUGGING_PORT = 9222  # Chrome 调试端口

# ======================== 投票标题提取 ========================
def get_votetitle(page) -> str:
    """从投票页面提取标题。"""
    try:
        # 主选择器：div.vote-title
        name_elem = page.ele("css:div.vote-title", timeout=1)
        if name_elem:
            return name_elem.text.strip()
        # 备选：任何 class 包含 votetitle 的元素
        name_elem = page.ele("css:[class*='vote-title']", timeout=1)
        if name_elem:
            return name_elem.text.strip()

        return ""
    except Exception:
        return ""

# ======================== 投票参与人数提取 ========================从投票页面提取参与人数
def get_votepaticipant(page) -> str:
    try:
        # 主选择器：div.vote-title
        name_elem = page.ele("css:div.joined-number", timeout=1)
        if name_elem:
            return name_elem.text.strip()
        # 备选：任何 class 包含 votetitle 的元素
        name_elem = page.ele("css:[class*='joined-number']", timeout=1)
        if name_elem:
            return name_elem.text.strip()

        return ""
    except Exception:
        return ""

# ======================== 发起投票UP主提取 ========================从投票页面页面提取发起人
def get_whovoted(page) -> str:
    try:
        # 主选择器：div.vote-title
        name_elem = page.ele("css:div.vote-user-name", timeout=1)
        if name_elem:
            return name_elem.text.strip()
        # 备选：任何 class 包含 votetitle 的元素
        name_elem = page.ele("css:[class*='vote-user-name']", timeout=1)
        if name_elem:
            return name_elem.text.strip()

        return ""
    except Exception:
        return ""

# ======================== 投票介绍提取 ========================从投票页面提取介绍
def get_voteintroduction(page) -> str:
    try:
        # 主选择器：div.vote-title
        name_elem = page.ele("css:div.vote-introduction", timeout=0.2)
        if name_elem:
            return name_elem.text.strip()
        # 备选：任何 class 包含 votetitle 的元素
        name_elem = page.ele("css:[class*='vote-introduction']", timeout=0.2)
        if name_elem:
            return name_elem.text.strip()

        return ""
    except Exception:
        return ""

# ======================== 主逻辑 ========================
def main():
    print("=" * 55)
    print("   Bilibili 投票检查器 by NokiaX")
    print("=" * 55)

    # 1. 输入VoteID起始结束范围
    voteid = int(input("\n请输入开始vote_id:").strip())
    voteid_end = int(input("\n请输入结束vote_id:").strip())

    # 2. 连接本地 Chrome
    print(f"\n🔗 正在连接本地 Chrome (端口 {DEBUGGING_PORT})...")
    try:
        co = ChromiumOptions()
        co.set_local_port(DEBUGGING_PORT)
        page = ChromiumPage(co)
        print("✅ 成功连接 Chrome 浏览器！")
    except Exception as e:
        print(f"❌ 连接 Chrome 失败: {e}")
        print(f"   请确保已以调试端口启动 Chrome：")
        print(f'   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port={DEBUGGING_PORT}')
        return

    print(f"\n🚀 开始检查... (VoteID: {voteid})")
    print(f"📁 结果保存至: {TITLE_FILE}")
    print("-" * 55)

    try:
        while voteid < voteid_end:
            url = f"http://t.bilibili.com/vote/h5/index/#/result?vote_id={voteid}"
            try:
                page.get(url)
                time.sleep(0.6)  # 等待页面加载

                vote_title = get_votetitle(page)
                vote_participants = get_votepaticipant(page)
                vote_up = get_whovoted(page)
                vote_introduction = get_voteintroduction(page)

                # 写入文件
                with open(TITLE_FILE, "a", encoding="utf-8") as s:
                    s.write(f"VoteID: {voteid} | 标题: {vote_title} | 发起人：{vote_up} | 参与人数： {vote_participants} | 投票介绍：{vote_introduction} \n")
                print(f"VoteID: {voteid} | 标题: {vote_title} | 发起人：{vote_up} | 参与人数： {vote_participants} | 投票介绍：{vote_introduction}")

                voteid += 1
            except Exception as e:
                checked += 1
                print(f"  [{checked}] VoteID {voteid} — ⚠️ 访问出错: {e}")

            # 随机延时
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            time.sleep(delay)

    except KeyboardInterrupt:
        print(f"\n\n{'=' * 55}")
        print(f"🛑 手动停止")
        print(f"   结果文件: {TITLE_FILE}")
        print(f"{'=' * 55}")

if __name__ == "__main__":
    main()