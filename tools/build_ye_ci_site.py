#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import html as htmlmod
from pathlib import Path
import markdown

ROOT = Path("/workspace/ye-ci-github")
DOCS = ROOT / "docs"
DEV = ROOT / "dev"
OUT = ROOT / "index.html"
OUT_DEV = ROOT / "dev.html"

CHAPTERS = [
    ("00-本文怎么用.md", "c-00", "本文怎么用", "先确认这是什么游戏"),
    ("01-产品定位.md", "c-01", "产品定位", "先确认这是什么游戏"),
    ("02-相对v0.1的关键变更.md", "c-02", "相对 v0.1 的关键变更", "先确认这是什么游戏"),
    ("03-设计优化与锁定.md", "c-03", "设计优化与锁定", "先确认这是什么游戏"),
    ("04-三种模式.md", "c-04", "三种模式", "怎么玩"),
    ("05-一局怎么玩.md", "c-05", "一局怎么玩", "怎么玩"),
    ("06-核心规则.md", "c-06", "核心规则", "怎么玩"),
    ("07-今夜科仪.md", "c-07", "今夜科仪", "怎么玩"),
    ("08-阵营标签与克制.md", "c-08", "阵营、标签与克制", "怎么玩"),
    ("09-编制与制作方法.md", "c-09", "编制与制作方法", "怎么玩"),
    ("10-人物编制.md", "c-10", "人物编制（32）", "编制与成长"),
    ("11-鬼物编制.md", "c-11", "鬼物编制（32）", "编制与成长"),
    ("12-进化变异与装备.md", "c-12", "进化、变异、融契与装备", "编制与成长"),
    ("13-构筑流派.md", "c-13", "构筑流派", "编制与成长"),
    ("14-图鉴与立绘.md", "c-14", "图鉴与立绘", "体验、关卡与界面"),
    ("15-平衡框架.md", "c-15", "平衡框架", "体验、关卡与界面"),
    ("16-关卡块与爽点.md", "c-16", "关卡块与爽点", "体验、关卡与界面"),
    ("17-操作与界面.md", "c-17", "操作与界面", "体验、关卡与界面"),
    ("18-叙事骨架.md", "c-18", "叙事骨架", "叙事、美术与制作范围"),
    ("19-美术与声音.md", "c-19", "美术与声音", "叙事、美术与制作范围"),
    ("20-范围解锁与DLC.md", "c-20", "范围、解锁与 DLC", "叙事、美术与制作范围"),
    ("21-验收与禁令.md", "c-21", "验收与禁令", "叙事、美术与制作范围"),
    ("22-附录-单位表说明.md", "c-22", "附录：单位表说明", "叙事、美术与制作范围"),
]

DEV_CHAPTERS = [
    ("README.md", "d-index", "目录", "怎么用"),
    ("00-给Astra的总说明与工作协议.md", "d-00", "总说明与工作协议", "怎么用"),
    ("01-不可违反的锁定清单.md", "d-01", "不可违反的锁定清单", "怎么用"),
    ("02-工程规范.md", "d-02", "工程规范", "怎么用"),
    ("03-阶段总表与考核总则.md", "d-03", "阶段总表与考核总则", "怎么用"),
    ("P0-工程奠基.md", "d-p0", "P0 工程奠基", "通往 G0"),
    ("P1-战场与镜头.md", "d-p1", "P1 战场与镜头", "通往 G0"),
    ("P2-单位与职分AI.md", "d-p2", "P2 单位与职分 AI", "通往 G0"),
    ("P3-鬼潮与路径时间.md", "d-p3", "P3 鬼潮与路径时间", "通往 G0"),
    ("P4-决策指令.md", "d-p4", "P4 决策指令（G0）", "通往 G0"),
    ("P5-一夜循环.md", "d-p5", "P5 一夜循环", "通往 G1"),
    ("P6-三种模式.md", "d-p6", "P6 三种模式", "通往 G1"),
    ("P7-进化变异与装备.md", "d-p7", "P7 进化、变异与装备（G1）", "通往 G1"),
    ("P8-编制内容入场.md", "d-p8", "P8 编制内容入场", "通往 G2"),
    ("P9-界面全套.md", "d-p9", "P9 界面全套", "通往 G2"),
    ("P10-关卡块与科仪.md", "d-p10", "P10 关卡块与科仪（G2）", "通往 G2"),
    ("P11-叙事音频与打磨.md", "d-p11", "P11 叙事、音频与打磨", "通往 G3"),
    ("P12-发布与上架验收.md", "d-p12", "P12 发布与上架验收（G3）", "通往 G3"),
]

FILE_TO_ID = {fn: cid for fn, cid, *_ in CHAPTERS}
DEV_FILE_TO_ID = {fn: cid for fn, cid, *_ in DEV_CHAPTERS}


ART = [
    ("art/13-实机-镜头切片与全图.jpg", "实机：镜头切片与全图", "当前镜头与全图标准。正式画面是全图上的镜头切片，小地图为更大的整座祠场，镜头框与当前画面一致。"),
    ("art/25-实机-掩体与基地内防守.jpg", "实机：掩体与基地内防守", "人类站位标准。人依托门窗、拒马和桌案防守，不站在庭院空地与潮混战；镜头尺度仍与 13 相同。"),
    ("art/24-实机-人类技能特效.jpg", "实机：人类技能特效", "人类上场更少，用更完整的点册、青灯、符印特效压质；镜头尺度仍与 13 相同。若图中仍有人在庭院空地读条，以第 25 号图的站位为准。"),
    ("art/14-UI-购入与部署.jpg", "UI：购入与部署", "购入并部署到防线的掩体岗位，不能部署到外门以外。卡片含费用和生命、攻击等关键数值。"),
    ("art/15-UI-升级与变异.jpg", "UI：升级与装备", "升级与装上香器，显示当前数值、升级预览和装备槽。"),
    ("art/16-UI-点册超度.jpg", "UI：点册超度", "点册/超度过程，可打断，其他单位继续自动作战。"),
    ("art/17-UI-立绘面板.jpg", "UI：立绘面板", "点击后弹出立绘，以及属性、技能、数值与装备。"),
    ("art/18-UI-夜程图.jpg", "UI：夜程图", "一夜的分支路线，当前节点高亮。"),
    ("art/19-UI-战后三选一.jpg", "UI：战后三选一", "战后必须三选一，构筑今夜。"),
    ("art/20-UI-图鉴.jpg", "UI：图鉴", "分栏点选后显示完整数值、技能、特性与装备。"),
    ("art/21-UI-结夜结算.jpg", "UI：结夜结算", "一夜结束后看香火、名分与谁还在册上。"),
    ("art/22-UI-夜市.jpg", "UI：夜市", "用香火购入香器或编制。"),
    ("art/23-UI-战斗内警告.jpg", "UI：战斗内警告", "门将破、名册告急等提示贴在边角，不挡住战场。"),
    ("art/12-实机-可平移长战场.jpg", "过程稿：可平移长战场", "曾误把小地图收成适配画面，导致场景变小。"),
    ("art/11-实机-可活动空间与退守.jpg", "过程稿：可活动空间", "室内楼梯与退守近景。"),
    ("art/10-实机-鬼潮比例.jpg", "过程稿：鬼潮比例", "普通鬼与人对高，门前 2–4 排涌入，大形约两倍人高。"),
    ("art/09-实机-人类阵营-房间进深.jpg", "过程稿：房间进深", "人类房间进深与设施比例。"),
    ("art/08-实机-场景布局-多层断面.jpg", "过程稿：场景布局", "接近段高差与沿路鬼潮。"),
    ("art/07-实机-画面框-参考构图.jpg", "过程稿：画面框", "16:9 画面框，世界铺满上半屏；布局已由 08 取代"),
    ("art/06-实机-尺度锁定-远镜头鬼潮.jpg", "过程稿：尺度锁定", "单位缩小与冲路纵深，画面框已由 07 取代"),
    ("art/01-实机-鬼潮守门.jpg", "早期实机：鬼潮守门", "只保留色板与 HUD 结构，不再作为尺度依据"),
    ("art/02-UI-暂停与指令栏.jpg", "早期 UI：暂停与指令栏", "早期过程稿，界面已由 14–16 取代"),
    ("art/03-UI-框选变异菜单.jpg", "早期 UI：框选变异菜单", "早期过程稿，界面已由 15 取代"),
    ("art/04-爽点-破门灌入.jpg", "早期爽点：破门灌入", "将按第 13 号镜头切片重做"),
    ("art/05-爽点-缢鬼上楼.jpg", "早期爽点：缢鬼上楼", "将按第 13 号镜头切片重做"),
]

md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "smarty"])


def strip_nav(text: str) -> str:
    # Drop the trailing chapter-nav we added for GitHub browsing.
    parts = re.split(r"\n---\s*\n(?=\n*上一章：|\n*\[返回目录\])", text, maxsplit=1)
    text = parts[0]
    text = re.sub(r"\n---\s*$", "", text).strip()
    return text


def rewrite_links(text: str) -> str:
    def file_link(m):
        raw = m.group(1)
        name = Path(raw).name
        if name in FILE_TO_ID:
            return f"(#{FILE_TO_ID[name]})"
        return m.group(0)

    text = re.sub(r"\((?:\./)?(\d{2}-[^)]+\.md)\)", file_link, text)
    text = text.replace("(../README.md)", "(#top)")
    text = text.replace("(../art/", "(art/")
    text = text.replace("](../art/)", "](#gallery)")
    text = text.replace("(../tables/", "(tables/")
    return text


def embed_art_links(html: str) -> str:
    def repl(m):
        href, inner = m.group(1), m.group(2)
        if re.search(r"\.(jpe?g|png|webp|gif)$", href, re.I):
            cap = inner.strip() or Path(href).stem
            return (
                f'<figure class="shot">'
                f'<img src="{htmlmod.escape(href)}" alt="{htmlmod.escape(cap)}" loading="lazy">'
                f"<figcaption>{inner}</figcaption></figure>"
            )
        return m.group(0)

    return re.sub(r'<a href="([^"]+)">(.+?)</a>', repl, html, flags=re.S)


def render_chapter(fn, cid, title, body_md):
    md.reset()
    body_html = md.convert(rewrite_links(strip_nav(body_md)))
    body_html = embed_art_links(body_html)
    # The first h2 is usually "N. Title" — keep it, section has the id.
    return f'<section class="chapter" id="{cid}">\n{body_html}\n</section>\n'


def sidebar_html():
    groups = []
    current = None
    items = []
    specials = [
        ("progress", "当前进度"),
        ("gallery", "画面锁定"),
    ]
    out = ['<a href="#progress">当前进度</a>', '<a href="#gallery">画面锁定</a>', '<a href="dev.html">开发规范</a>']
    last_group = None
    for fn, cid, title, group in CHAPTERS:
        if group != last_group:
            out.append(f'<div class="nav-group">{htmlmod.escape(group)}</div>')
            last_group = group
        out.append(f'<a href="#{cid}">{htmlmod.escape(title)}</a>')
    return "\n        ".join(out)


gallery_figures = "\n".join(
    f'''      <figure class="shot">
        <img src="{src}" alt="{htmlmod.escape(title)}" loading="lazy">
        <figcaption><strong>{htmlmod.escape(title)}</strong> · {htmlmod.escape(cap)}</figcaption>
      </figure>'''
    for src, title, cap in ART
)

chapters_html = []
for fn, cid, title, group in CHAPTERS:
    raw = (DOCS / fn).read_text(encoding="utf-8")
    chapters_html.append(render_chapter(fn, cid, title, raw))
chapters = "\n".join(chapters_html)

css = r"""
:root {
  --bg: #0b0b0c;
  --bg-2: #121214;
  --bg-3: #1a1a1e;
  --ink: #ece4d6;
  --muted: #9a9388;
  --line: rgba(236, 228, 214, 0.12);
  --teal: #6aa8a4;
  --cinnabar: #c45a46;
  --gold: #c4a574;
  --side: 252px;
  --max: 760px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 17px/1.75 "Noto Sans SC", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
}
a { color: var(--teal); text-decoration-thickness: 1px; text-underline-offset: 3px; }
a:hover { color: #8fc4c0; }
.menu-btn {
  display: none;
  position: fixed; top: 12px; left: 12px; z-index: 40;
  background: var(--bg-3); color: var(--ink);
  border: 1px solid var(--line); border-radius: 8px;
  padding: 8px 12px; font: inherit; cursor: pointer;
}
aside {
  position: fixed; inset: 0 auto 0 0;
  width: var(--side);
  background: #0e0e10;
  border-right: 1px solid var(--line);
  overflow: auto;
  padding: 28px 18px 48px;
}
.brand {
  font-family: "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif;
  font-size: 28px; letter-spacing: 0.18em; margin: 0 0 4px;
}
.sub { margin: 0 0 22px; color: var(--muted); font-size: 12px; letter-spacing: 0.08em; }
aside nav a {
  display: block; color: var(--muted); text-decoration: none;
  padding: 5px 10px; border-radius: 6px; font-size: 13px; line-height: 1.45;
}
aside nav a:hover, aside nav a.active { background: var(--bg-3); color: var(--ink); }
aside nav a.active { box-shadow: inset 2px 0 0 var(--cinnabar); }
.nav-group {
  margin: 16px 0 6px; padding: 0 10px;
  color: var(--gold); font-size: 11px; letter-spacing: 0.12em;
}
main { margin-left: var(--side); padding: 48px 40px 120px; }
.wrap { max-width: var(--max); margin: 0 auto; }
.hero h1 {
  font-family: "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif;
  font-weight: 600; font-size: 42px; letter-spacing: 0.12em;
  margin: 0 0 12px;
}
.hero .one-liner { font-size: 18px; color: var(--ink); margin: 0 0 14px; }
.hero .meta { color: var(--muted); font-size: 13px; margin: 0 0 8px; }
hr.rule { border: 0; border-top: 1px solid var(--line); margin: 36px 0; }
section.chapter, #progress, #gallery { scroll-margin-top: 24px; margin: 56px 0 0; }
h1, h2, h3, h4 {
  font-family: "Noto Serif SC", "Source Han Serif SC", "Songti SC", serif;
  font-weight: 600; line-height: 1.35;
}
h2 { font-size: 26px; margin: 0 0 18px; padding-bottom: 10px; border-bottom: 1px solid var(--line); }
h3 { font-size: 20px; margin: 32px 0 12px; color: #f3eadc; }
h4 { font-size: 17px; margin: 24px 0 10px; }
p { margin: 0 0 14px; }
ul, ol { margin: 0 0 16px; padding-left: 1.3em; }
li { margin: 0 0 6px; }
table {
  width: 100%; border-collapse: collapse; font-size: 14px;
  margin: 0 0 20px; line-height: 1.55;
  display: block; overflow-x: auto;
}
th, td {
  border: 1px solid var(--line); padding: 8px 10px; text-align: left;
  vertical-align: top; min-width: 4em;
}
th { background: var(--bg-3); color: var(--gold); font-weight: 600; white-space: nowrap; }
tr:nth-child(even) td { background: rgba(255,255,255,0.015); }
code, pre {
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.9em;
}
code { background: var(--bg-3); padding: 0.1em 0.35em; border-radius: 4px; }
blockquote {
  margin: 0 0 16px; padding: 10px 16px;
  border-left: 3px solid var(--cinnabar);
  background: var(--bg-2); color: #d9d0c3;
}
.note {
  background: var(--bg-2); border: 1px solid var(--line);
  border-left: 3px solid var(--teal);
  padding: 12px 16px; margin: 0 0 20px; color: var(--muted); font-size: 14px;
}
.progress-grid { display: grid; gap: 14px; margin: 16px 0 8px; }
.card {
  background: var(--bg-2); border: 1px solid var(--line);
  border-radius: 10px; padding: 16px 18px;
}
.card h3 { margin: 0 0 8px; font-size: 15px; color: var(--gold); border: 0; }
.card ul { margin: 0; }
.card .tag {
  display: inline-block; font-size: 11px; letter-spacing: 0.08em;
  color: var(--teal); margin-bottom: 6px;
}
.log { list-style: none; padding: 0; margin: 8px 0 0; color: var(--muted); font-size: 14px; }
.log li { padding: 6px 0; border-bottom: 1px solid var(--line); }
.log time { color: var(--gold); margin-right: 8px; font-variant-numeric: tabular-nums; }
#gallery .shots, .shots {
  display: grid; gap: 22px; margin: 18px 0 8px;
}
figure.shot { margin: 20px 0; }
figure.shot img {
  display: block; width: 100%; height: auto;
  border: 1px solid var(--line); border-radius: 8px; background: #000;
}
figure.shot figcaption { color: var(--muted); font-size: 13px; margin-top: 8px; }
.topbar-links { margin-top: 18px; font-size: 13px; color: var(--muted); }
.top { position: fixed; right: 20px; bottom: 20px; z-index: 20;
  width: 40px; height: 40px; border-radius: 50%;
  background: var(--bg-3); color: var(--ink); border: 1px solid var(--line);
  text-decoration: none; display: grid; place-items: center; font-size: 18px;
}
.top:hover { color: var(--teal); }
@media (max-width: 900px) {
  .menu-btn { display: block; }
  aside {
    transform: translateX(-100%); transition: transform 0.2s ease;
    z-index: 30; width: min(84vw, 300px);
    box-shadow: 8px 0 32px rgba(0,0,0,0.4);
  }
  aside.open { transform: none; }
  main { margin-left: 0; padding: 64px 18px 100px; }
  .hero h1 { font-size: 30px; letter-spacing: 0.08em; }
  .backdrop { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 25; }
  .backdrop.show { display: block; }
}
@media print {
  aside, .menu-btn, .top, .backdrop { display: none !important; }
  main { margin: 0; padding: 0; }
  body { background: #fff; color: #111; }
  a { color: inherit; }
  figure.shot img { break-inside: avoid; }
}
"""

js = r"""
(function () {
  const btn = document.querySelector('.menu-btn');
  const side = document.querySelector('aside');
  const back = document.querySelector('.backdrop');
  const toggle = (on) => {
    side.classList.toggle('open', on);
    back.classList.toggle('show', on);
  };
  btn.addEventListener('click', () => toggle(!side.classList.contains('open')));
  back.addEventListener('click', () => toggle(false));
  side.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => toggle(false)));

  const links = [...side.querySelectorAll('nav a')];
  const secs = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const id = '#' + e.target.id;
      links.forEach((l) => l.classList.toggle('active', l.getAttribute('href') === id));
    });
  }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });
  secs.forEach((s) => io.observe(s));
})();
"""

page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《夜祠》游戏设计方案</title>
  <meta name="description" content="《夜祠》纯单机游戏设计方案：侧视 2D 实时指挥与肉鸽构筑。方案 A 墨煞像素，v0.2。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&family=Noto+Serif+SC:wght@600&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body id="top">
  <button class="menu-btn" type="button">目录</button>
  <div class="backdrop"></div>
  <aside>
    <p class="brand">夜祠</p>
    <p class="sub">NIGHT SHRINE · v0.2</p>
    <nav>
        {sidebar_html()}
    </nav>
  </aside>
  <main>
    <div class="wrap">
      <header class="hero">
        <h1>夜祠</h1>
        <p class="one-liner">在名字开始从世上脱落的夜里，你守住一册尚存的名，或率领无名之潮去夺回一张脸。</p>
        <p class="meta">游戏设计方案 v0.2 · 2026-11-15 · 纯单机 · 侧视 2D 实时指挥 + 肉鸽构筑</p>
        <p class="meta">视觉锁定：方案 A「墨煞像素」· 成人向灵异</p>
        <p class="topbar-links">源文件仓库：<a href="https://github.com/gh393872102/ye-ci">github.com/gh393872102/ye-ci</a>　·　<a href="dev.html">给 GPT-Astra 的开发规范</a></p>
      </header>

      <section id="progress">
        <h2>当前进度</h2>
        <p>以后每次改方案、补关卡或调整编制，都会更新到这一页。你可以把这个地址收藏起来，不用再到 GitHub 里一个个点开文件。</p>
        <div class="progress-grid">
          <div class="card">
            <div class="tag">已完成</div>
            <h3>设计方案 v0.2，并锁定战场与指挥方式</h3>
            <ul>
              <li>方案 A 墨煞像素作为实机视觉锁定</li>
              <li>三种坐席：守香、夺名、观祭，共用同一套规则</li>
              <li>32 名人物、32 种鬼物的编制、技能与特性</li>
              <li>变异、融契、香器、今夜科仪与平衡框架</li>
              <li>公开仓库与本阅读网站上线</li>
              <li>战场拉远、单位缩小：普通单位约占屏高 1/12–1/14，高潮夜同屏 80–150+</li>
              <li>画面框锁定：16:9，可玩世界铺满上部 60%–72%，夜空是有星和远景的暗夜，不是纯黑上下边</li>
              <li>场景布局与潮水分布：接近段高差、沿路 2–4 排的流，禁止三角山</li>
              <li>人类阵营房间进深：每层 2–3 个房间，门洞、桌案、层高和人对得上，名册房可辨认</li>
              <li>鬼与人对照：普通鬼与守门人等高，能几乎顶到门楣；大形约 1.6–2.2 倍；禁止单列小偶</li>
              <li>可活动空间：每层可走动，能放置阻碍物，楼梯是退路，支持层层退守，不是塔防站桩</li>
              <li>可平移长战场：全图约 4–6 个镜头宽；无交战走完 45–70 秒；人类撤退快于鬼潮追击</li>
              <li>镜头切片：正式画面匹配大全图上的小镜头框，不再把小地图收成适配一张全景</li>
              <li>玩家只做决策指令，单位按职分自动进退</li>
              <li>十张关键界面稿，其中立绘、图鉴、购入、升级已补上属性、技能、数值和装备</li>
              <li>第 24 号图锁定人类技能特效：远镜头下仍要能认出点册、青灯、符印</li>
              <li>第 6.6 节与第 25 号图锁定人类依托掩体、不出基地</li>
            </ul>
          </div>
          <div class="card">
            <div class="tag">现在</div>
            <h3>给 GPT-Astra 的开发规范正文已齐</h3>
            <ul>
              <li>P0–P12 已全部发布，覆盖 G0 到 G3 的提示词、实现范围和考核表</li>
              <li>在线阅读：<a href="dev.html">开发规范专页</a>。交给 Astra 时从 P0 起，一阶段一阶段做</li>
              <li>引擎锁定为 Godot 4.4 或更新的 4.x 稳定版，游戏工程将放在独立仓库</li>
              <li>设计锁定未改：镜头仍以第 13 号图为准，人类站位仍以第 25 号图为准</li>
            </ul>
          </div>
          <div class="card">
            <div class="tag">下一步</div>
            <h3>把本页交给 Astra 开工</h3>
            <ul>
              <li>从 P0 工程奠基开始，不得跳阶段，关键项未通过不得宣称达到门槛</li>
              <li>标题、暂停菜单与失败结算如需再补视觉稿，可并行，但不改已锁定设计</li>
            </ul>
          </div>
        </div>
        <h3>更新记录</h3>
        <ul class="log">
          <li><time>2026-11-15</time>加厚 P8–P12：编制、界面、科仪与关卡块、结局与音效、上架回归均已拆到可执行细则。</li>
          <li><time>2026-11-15</time>加厚 P7：20 香器、16 技艺、12 名帖、融契配方和六条流派验收都拆到可执行的 id 与步骤。</li>
          <li><time>2026-11-15</time>开发规范 P0–P12 全部发布，G0 到 G3 的提示词和考核表已齐，见 <a href="dev.html">开发规范专页</a>。</li>
          <li><time>2026-11-15</time>开发规范已写到 P4（G0 规则能玩），含各阶段提示词和考核表，见 <a href="dev.html">开发规范专页</a>。</li>
          <li><time>2026-11-15</time>开始发布给 GPT-Astra 的开发规范。第一批含总说明、锁定清单、工程规范、阶段总表和 P0 工程奠基。</li>
          <li><time>2026-11-15</time>锁定人类依托掩体、不出基地；新增第 25 号站位标准图。庭院用于设阻和退守，不是把人拉出去列阵。</li>
          <li><time>2026-11-15</time>立绘、图鉴、购入和升级面板补上属性、技能、数值与装备；新增第 24 号人类技能特效图。人类用更高规格压质，不靠推近镜头。</li>
          <li><time>2026-11-15</time>补齐图鉴、结夜结算、夜市与战斗内警告四张界面稿。</li>
          <li><time>2026-11-15</time>正式画面改为匹配大全图上的镜头切片；单位改为按职分自动作战，玩家只做购入、部署、升级/变异和点册。新增第 13 号标准图和 14–19 号界面稿。</li>
          <li><time>2026-11-15</time>锁定可平移长战场，并补上走速、射程与自动退守。一夜 25–40 分钟是整夜总时长；单场路径必须按走速留足。</li>
          <li><time>2026-11-15</time>锁定可活动空间与层层退守。祠堂改为可走动的连续地面，能放置阻碍物，楼梯是退路，名册房为最后据点。</li>
          <li><time>2026-11-15</time>锁定鬼潮与人的对照比例。普通鬼与普通人等高，能几乎顶到门楣；大形约 1.6–2.2 倍；门前保持 2–4 排涌入。</li>
          <li><time>2026-11-15</time>锁定人类阵营的房间进深与设施比例。祠堂改为有门厅、香案、名册房的剖视建筑，门洞、桌案、层高与人对得上。</li>
          <li><time>2026-11-15</time>锁定场景布局与潮水分布。接近段增加高差，鬼潮改为沿路流动，不再堆成三角山。</li>
          <li><time>2026-11-15</time>修正画面框。可玩世界铺满 16:9 上半屏，夜空改为有星和远景的暗夜，不再是细带加纯黑上下边。</li>
          <li><time>2026-11-15</time>锁定战场尺度。新增尺度标准图，场面拉大、单位缩小，潮水须有纵深层次。</li>
          <li><time>2026-11-15</time>发布设计方案 v0.2，并上线本阅读网站。</li>
        </ul>
      </section>

      <section id="gallery">
        <h2>画面锁定（方案 A）</h2>
        <div class="note">图中中文可能有生成误差，只看构图、密度、色板和 HUD 结构，不看字。镜头与全图以「镜头切片与全图」为准，人类特效以「人类技能特效」为准；14–23 是待拍板的界面稿；12 及更早画面为过程稿。</div>
        <div class="shots">
{gallery_figures}
        </div>
      </section>

      <hr class="rule">

{chapters}
    </div>
  </main>
  <a class="top" href="#top" title="回到顶部">↑</a>
  <script>{js}</script>
</body>
</html>
"""

def rewrite_dev_links(text: str) -> str:
    def file_link(m):
        raw = m.group(1)
        name = Path(raw).name
        if name in DEV_FILE_TO_ID:
            return f"(#{DEV_FILE_TO_ID[name]})"
        if name in FILE_TO_ID:
            return f"(index.html#{FILE_TO_ID[name]})"
        if raw.startswith("../README.md"):
            return "(index.html#top)"
        if raw.startswith("../docs/"):
            return f"({raw[3:]})"  # docs/filename.md
        if raw.startswith("../art/"):
            return f"(art/{Path(raw).name})"
        if raw.startswith("../tables/"):
            return f"(tables/{Path(raw).name})"
        return m.group(0)

    text = re.sub(r"\((?:\./)?([^)]+\.md)\)", file_link, text)
    text = text.replace("](../art/)", "](index.html#gallery)")
    text = text.replace("(../art/", "(art/")
    text = text.replace("(../tables/", "(tables/")
    return text


def dev_sidebar_html():
    out = [
        '<a href="index.html">设计方案</a>',
        '<a href="#top">开发规范目录</a>',
    ]
    last_group = None
    for fn, cid, title, group in DEV_CHAPTERS:
        if group != last_group:
            out.append(f'<div class="nav-group">{htmlmod.escape(group)}</div>')
            last_group = group
        out.append(f'<a href="#{cid}">{htmlmod.escape(title)}</a>')
    return "\n        ".join(out)


dev_chapters_html = []
for fn, cid, title, group in DEV_CHAPTERS:
    raw = (DEV / fn).read_text(encoding="utf-8")
    md.reset()
    body_html = md.convert(rewrite_dev_links(strip_nav(raw)))
    body_html = embed_art_links(body_html)
    dev_chapters_html.append(f'<section class="chapter" id="{cid}">\n{body_html}\n</section>\n')
dev_chapters = "\n".join(dev_chapters_html)

dev_page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《夜祠》开发规范 · 交给 GPT-Astra</title>
  <meta name="description" content="《夜祠》分阶段开发规范、提示词与考核目标，供 GPT-Astra 按锁定设计实现游戏。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600&family=Noto+Serif+SC:wght@600&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body id="top">
  <button class="menu-btn" type="button">目录</button>
  <div class="backdrop"></div>
  <aside>
    <p class="brand">夜祠</p>
    <p class="sub">开发规范 · ASTRA</p>
    <nav>
        {dev_sidebar_html()}
    </nav>
  </aside>
  <main>
    <div class="wrap">
      <header class="hero">
        <h1>开发规范</h1>
        <p class="one-liner">给 GPT-Astra 的分阶段开发圣经：按什么顺序做、做到哪算过、每次该贴怎样的提示词。</p>
        <p class="meta">与设计方案 v0.2 配套 · 2026-11-15 · 已发布：总说明到 P12（G0–G3 全文）</p>
        <p class="meta">引擎锁定：Godot 4.4 或更新的 4.x 稳定版 · 主语言 GDScript · 游戏工程放独立仓库</p>
        <p class="topbar-links"><a href="index.html">返回设计方案</a>　·　源文件：<a href="https://github.com/gh393872102/ye-ci/tree/main/dev">github.com/gh393872102/ye-ci/dev</a></p>
      </header>
      <div class="note">设计冲突以设计方案为准。工程顺序、提示词和阶段考核以本页为准。P0–P12 已全部发布。Astra 必须从 P0 起一阶段一阶段做，不得跳步，也不得在关键项未通过时宣称达到门槛。</div>
{dev_chapters}
    </div>
  </main>
  <a class="top" href="#top" title="回到顶部">↑</a>
  <script>{js}</script>
</body>
</html>
"""

OUT.write_text(page, encoding="utf-8")
OUT_DEV.write_text(dev_page, encoding="utf-8")
print("wrote", OUT, "bytes", OUT.stat().st_size)
print("wrote", OUT_DEV, "bytes", OUT_DEV.stat().st_size)
text = OUT.read_text(encoding="utf-8")
assert "c-10" in text and "铁肩" in text and "art/01-实机-鬼潮守门.jpg" in text
assert "dev.html" in text
assert "{{" not in text
dtext = OUT_DEV.read_text(encoding="utf-8")
assert "d-p0" in dtext and "工程奠基" in dtext and "G12" in dtext
assert "{{" not in dtext
print("ok, images", text.count("<img "), "chapters", text.count('class="chapter"'), "dev chapters", dtext.count('class="chapter"'))
