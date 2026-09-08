#!/bin/bash
# 部署成长系统静态镜像到 GitHub Pages (2026-09-08 12:00 定时任务执行)
# 步骤: 建仓 growth-system-panel → 推 main → 开 Pages → 裸连验证
set -e
SITE=~/growth_site_build
REPO=growth-panel-online
GH_USER=xinxinlon5b

cd "$SITE"
# 1. git init + 提交(带代理提交)
git init -q 2>/dev/null || true
git add -A
git -c user.name="$GH_USER" -c user.email="$GH_USER@users.noreply.github.com" commit -q -m "成长系统静态镜像 $(date '+%Y-%m-%d %H:%M')" 2>&1 | tail -1 || echo "(无新提交或已提交过)"

# 2. 建仓并推送(如已有则只推送)
if gh repo view "$GH_USER/$REPO" >/dev/null 2>&1; then
  echo "仓库已存在, 直接推送"
else
  echo "创建仓库 $REPO"
  gh repo create "$REPO" --public --source=. --push --description "成长系统在线镜像(静态版) — 卡库/文档/视频/审核报告可读"
fi

# 3. 推送(带代理)
echo "推送中(代理)..."
git -c http.proxy=socks5://127.0.0.1:7892 -c https.proxy=socks5://127.0.0.1:7892 push -u origin main 2>&1 | tail -3 || git -c http.proxy=http://127.0.0.1:7892 -c https.proxy=http://127.0.0.1:7892 push -u origin main 2>&1 | tail -3

# 4. 开 Pages(如已开会报 409 忽略)
echo "开启 Pages..."
gh api -X POST "repos/$GH_USER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" 2>&1 | head -3 || echo "(Pages 可能已开启, 忽略)"

# 5. 裸连验证(等构建 40-90s)
URL="https://$GH_USER.github.io/$REPO/"
echo "等待构建并验证: $URL"
for i in $(seq 1 20); do
  code=$(curl -s -o /dev/null -w "%{http_code}" --noproxy '*' --max-time 10 "$URL" 2>/dev/null || echo 000)
  echo "  第 ${i} 次: HTTP $code"
  if [ "$code" = "200" ]; then
    # 内容 marker: 首页含 弹药库/Agent 操作台
    if curl -s --noproxy '*' --max-time 10 "$URL" 2>/dev/null | grep -q "弹药库"; then
      echo "✅ 上线成功: $URL"
      echo "=== 验证 01 文档 ==="
      curl -s -o /dev/null -w "  01文档: %{http_code}\n" --noproxy '*' --max-time 10 "$URL" "obs/成长系统/01_审核标准与三审流水线.md" 2>/dev/null || true
      exit 0
    else
      echo "  (200 但内容未更新, 继续等)"
    fi
  fi
  sleep 10
done
echo "⚠️ 20 次轮询未等到 200, 请手动检查"
exit 1
