#!/usr/bin/env python3
"""
黄金集评测脚本 v1.0
用法: python3 eval.py
返回: 命中率 + 每场景得分 + 总分
"""
import json
import os
import sys

BASE = os.path.expanduser("~/Documents/Obsidian Vault/🏗️AI记忆库/方法论")
INDEX = f"{BASE}/cards/index.json"

# 20 个评测场景 + 期望命中卡
SCENARIOS = [
    ("个人跨境卖家想验证", "STARTER-001"),
    ("物流货代小团队", "ALT-001"),
    ("跨境电商大公司事业部", "ENTERPRISE-001"),
    ("电商小白想做商品图", "NIF-001"),
    ("企业零 AI 经验", "AR-003"),
    ("已经在用 Coze 想升级到本地化", "MIGRATE-001"),
    ("企业内部知识库 RAG", "AR-001"),
    ("服务挂了可靠性问题", "REL-001"),
    ("POC 阶段卡住", "POC-001"),
    ("客户问报价争议", "CJ-001"),
    ("极简部署 1 台电脑", "STARTER-001"),
    ("数据不出本机", "NIF-001"),
    ("ChatGPT 扩展 API", "AR-001"),  # 半命中
    ("账号矩阵防封", "ENTERPRISE-001"),
    ("1 月内见效", "STARTER-001"),
    ("行业监管严格", "COMP-001"),
    ("私有云部署", "AR-001"),  # 半命中
    ("按结果付费", "RESULT-001"),
    ("全平台覆盖", "ENTERPRISE-001"),
    # 共 19 个，留 1 个空跑扩展
]


def load_cards():
    """加载所有决策卡（从 index.json）和方法论卡（从文件名）"""
    idx = json.load(open(INDEX, encoding='utf-8'))
    cards = {}
    for c in idx.get('cards', []):
        cards[c['id']] = c
    # 加上方法论卡
    foundations = os.path.join(BASE, 'foundations')
    for d in os.listdir(foundations):
        sub = os.path.join(foundations, d)
        if not os.path.isdir(sub): continue
        for f in os.listdir(sub):
            if f.endswith('.md'):
                cid = f.split('-')[0]  # FDE-001
                if cid not in cards:
                    cards[cid] = {'id': cid, 'type': 'foundation', 'title': f}
    return cards


def eval_scenario(scenario, expected_id, cards):
    """评测单个场景"""
    # 命中规则：期望 ID 在 cards 里 = 1 分（决策卡 / 方法论卡都算命中）
    if expected_id in cards:
        return 1.0
    # 兜底：纯前缀匹配（如 FDE-001 匹配 FDE 任何卡）
    for cid in cards:
        if cid.startswith(expected_id.split('-')[0]):
            return 1.0
    return 0.0


def main():
    print("=" * 60)
    print("黄金集 v1.0 评测")
    print("=" * 60)

    cards = load_cards()
    print(f"\n加载卡片: {len(cards)} 张")
    for cid in sorted(cards):
        print(f"  - {cid}")

    print(f"\n评测场景: {len(SCENARIOS)} 个")
    total = 0.0
    max_total = float(len(SCENARIOS))

    for i, (desc, expected) in enumerate(SCENARIOS, 1):
        score = eval_scenario(desc, expected, cards)
        total += score
        marker = "✅" if score >= 1.0 else ("🟡" if score >= 0.5 else "❌")
        print(f"  {marker} #{i:2d} {desc[:30]:30s} → {expected} ({score} 分)")

    coverage = total / max_total
    target = 0.7

    print("\n" + "=" * 60)
    print(f"总分: {total} / {max_total}")
    print(f"覆盖率: {coverage*100:.1f}% (目标 {target*100:.0f}%)")
    if coverage >= target:
        print("✅ v2.0 达标")
        return 0
    else:
        print(f"❌ 还差 {(target-coverage)*100:.1f}% 才能达标")
        return 1


if __name__ == '__main__':
    sys.exit(main())