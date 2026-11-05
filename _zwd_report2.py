# -*- coding: utf-8 -*-
import docx
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

WORK = r"c:\Users\lenovo\.trae-cn\builtin\work"
OUT = r"d:\高级网页设计\1\_zwd_report2_new.docx"

doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21)
sec.page_height = Cm(29.7)
sec.left_margin = Cm(2.6)
sec.right_margin = Cm(2.6)
sec.top_margin = Cm(2.4)
sec.bottom_margin = Cm(2.4)

normal = doc.styles["Normal"]
normal.font.name = "宋体"
normal.font.size = Pt(10.5)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


def para(text="", size=10.5, bold=False, font="宋体", align=None, indent=True,
          before=0, after=6, line=1.5, color=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = line
    if indent:
        pf.first_line_indent = Pt(size * 2)
    if align is not None:
        p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.name = font
        r.element.rPr.rFonts.set(qn("w:eastAsia"), font)
        r.font.size = Pt(size)
        r.bold = bold
        if color:
            r.font.color.rgb = RGBColor(*color)
    return p


def h1(text):
    p = para(text, size=15, bold=True, font="黑体", indent=False, before=16, after=8, line=1.4)
    # 下边框
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), "BFB7A6")
    borders.append(bottom)
    pPr.append(borders)
    return p


def h2(text):
    return para(text, size=12, bold=True, font="黑体", indent=False, before=10, after=4, line=1.4)


def fig(path, width_cm, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Cm(width_cm))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_before = Pt(0)
    c.paragraph_format.space_after = Pt(10)
    r = c.add_run(caption)
    r.font.name = "宋体"
    r.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    return c


def code(lines):
    for ln in lines:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.0
        pf.left_indent = Cm(0.6)
        pf.first_line_indent = Pt(0)
        r = p.add_run(ln if ln else " ")
        r.font.name = "Consolas"
        r.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
        r.font.size = Pt(7.5)
        # 浅灰底纹
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "F6F4EE")
        pPr.append(shd)
    # 代码段后间距
    doc.paragraphs[-1].paragraph_format.space_after = Pt(8)


def cell_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "6")
        e.set(qn("w:color"), "BFB7A6")
        borders.append(e)
    tcPr.append(borders)


# ============ 封面 ============
para("", after=0, indent=False)
para("", after=0, indent=False)
para("《高级网页设计I》", size=18, bold=True, font="黑体",
     align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, after=10, line=1.2)
para("图像解决方案 项目报告", size=22, bold=True, font="黑体",
     align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, after=26, line=1.2)

t = doc.add_table(rows=3, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.autofit = False
widths = [Cm(7.2), Cm(8.4)]
rows_data = [
    ("学　号：24001010525　　姓　名：郑雯迪", ""),
    ("班　级", "计算机24005"),
    ("项目选题名称", "传统茶文化展示网页（移动端茶文化 App 首页）"),
]
for ri, (a, b) in enumerate(rows_data):
    for ci in range(2):
        cell = t.cell(ri, ci)
        cell.width = widths[ci]
        cell_border(cell)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.3
        r = p.add_run(a if ci == 0 else b)
        r.font.name = "宋体"
        r.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
        r.font.size = Pt(10.5)
        if ri == 0:
            r.bold = False

# 合并第一行两格
t.cell(0, 0).merge(t.cell(0, 1))

for _ in range(16):
    para("", after=0, indent=False)
para("2026 年 11 月", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)

doc.add_page_break()

# ============ 实施过程 ============
h1("实施过程")
h2("项目需求与实现")
para("本次实验的三级项目选题为“传统茶文化展示网页”（移动端茶文化 App 首页）。实验任务是使用 iconfont.com 检索、加工并生成个性化图标文件，用 SVG 的方式完成该项目的下导航设计，要求自适应宽度。由于上一个项目（网页元素设计）已经使用 iconfont 字体图标，本次按要求改用 SVG，以体现两种图像解决方案在获得图像、使用图像与用 CSS 修饰图像上的区别。")
para("下导航共 5 项：首页、茶库、记一泡、茶友、我的。其中“茶友”带数字徽章 12，“茶库”和“我的”带红点提醒；当前项“首页”以珊瑚红高亮显示。页面容器限制最大宽度 420px 并在浏览器窗口居中，模拟手机屏幕效果；下导航使用 position: fixed 固定在页面底部，宽度 100%、最大 420px，随视口自适应。")
para("图标的获得方式：在 iconfont.com 项目（Project ID 5244853，项目名“24001010525 郑雯迪”）中挑选并保留 20 个图标，下载到本地 font 目录，包含 iconfont.css、woff2、woff、ttf 字体文件与 demo_index.html 预览页。本项目不使用字体渲染，而是把选中的 5 个图标（首页、发现、新增、微信、我的）的字形轮廓转换为 SVG path 后内联到 HTML 中，用 fill: currentColor 交由 CSS 统一控制颜色与大小。")
para("五项入口按茶文化 App 的使用路径安排：首页展示今日茶单与茶事日程；茶库用于检索六大茶类与产区资料；中间的“记一泡”是记录本次冲泡参数的主操作，做成圆形凸起；茶友用于茶席约伴与动态交流；我的管理收藏与冲泡记录。")
para("采用 SVG 而不是字体图标的考虑：内联 SVG 不产生额外的字体请求，图形在任意缩放下都不失真；图标颜色通过 fill: currentColor 继承父级 color，激活态与悬停态只需修改一个 color 值，无需切换字体类名。代价是 HTML 中 path 数据较长，因此本项目只在 5 个导航图标上使用这种方式。")
para("给出你的三级项目的下导航截图，如果没有下导航用三级项目的其他导航代替，或其他相关网站的下导航。", indent=False, color=(0x66, 0x66, 0x66))
para("本项目三级项目为展示型网页，没有底部导航，故截取其页面顶部导航区作为参照，并在此基础上设计移动端 App 的下导航（图 1）。")
fig(WORK + r"\p1_top.png", 12.2, "图1  三级项目页面顶部导航截图（传统茶文化展示网页）")

para("从 iconfont 获得的所有图标的截图：", indent=False, color=(0x66, 0x66, 0x66))
fig(WORK + r"\p2_iconset.png", 14.4, "图2  iconfont.com 项目（Project ID 5244853）中获得的全部图标及 Unicode")

para("下导航原图：", indent=False, color=(0x66, 0x66, 0x66))
para("设计线框先确定结构：手机容器宽 420px，导航高 60px，五栏等分；中间“记一泡”按钮为 40px 圆形并上移 24px 做凸起；图标 23px、标签 11px；“茶友”右上角为数字徽章，“茶库”“我的”为红点。", indent=False)
fig(WORK + r"\p2_ref.png", 12.0, "图3  下导航设计原图（420px 手机容器 / 五栏等分 / 中间凸起）")

para("下导航实现图：", indent=False, color=(0x66, 0x66, 0x66))
para("四级项目2.html 在 1280px 桌面视口下的实现效果：页面容器限制为 420px 并居中，导航 fixed 固定在屏幕底部；下导航特写中可看到五栏等分、中间“记一泡”圆形凸起、“茶友”数字徽章 12、“茶库”与“我的”红点、当前项“首页”珊瑚红高亮。", indent=False)
fig(WORK + r"\p2_navcrop.png", 15.0, "图4  下导航实现效果 · 特写（五栏等分 / 中间凸起 / 徽章 12 / 红点 / 首页高亮）")

para("对比说明：实现效果与原图结构一致——五栏横向等分、中间按钮圆形凸起、首项高亮；线框中的灰色占位圆在实现时替换为 iconfont 项目中的真实图标字形，并用 currentColor 由 CSS 统一着色；导航在手机视口铺满宽度，在桌面视口限制为 420px 并居中，更接近真实 App 的观感。")

# ============ 项目代码 ============
h1("项目代码")
para("要求：使用字体图标或 SVG 的方式使用 iconfont 图标，代码中要包含学号或姓名，或者类名中包括姓名缩写，原则上不建议使用 id 选择器，原则上要设计全局 CSS。", indent=False, color=(0x66, 0x66, 0x66))
para("本项目代码中的 CSS 类名统一以姓名缩写 zwd_ 开头（郑雯迪）；HTML 页面头部包含姓名与学号注释；未使用 id 选择器；在 :root 中集中定义了全局配色、字体与尺寸变量。")
para("（1）获得 SVG：把 iconfont 字体中选中图标的字形轮廓转换为 24×24 的 SVG path，内联写入页面，再交给 CSS 着色。以下为其中一个图标（首页）：", indent=False)
code([
    '<!-- iconfont 项目 5244853 · 图标“首页”（&#xe65d;），字形轮廓转 SVG -->',
    '<svg class="zwd_icon" viewBox="0 0 24 24" aria-hidden="true">',
    '  <path d="M22.27 10.72 13.86 1.88Q13.44 1.44 12.87 1.28Q12.3 1.12 11.72 1.27',
    '           Q11.14 1.42 10.72 1.86L1.75 10.87Q1.25 11.37 1.21 11.92 … （路径略）"/>',
    '</svg>',
])
para("（2）HTML 结构：下导航由 5 个导航项组成，每项为“SVG 图标 + 文字标签”，徽章与红点用 <i> 元素绝对定位在图标右上角：", indent=False)
code([
    '<!-- 姓名：郑雯迪 学号：24001010525 日期：2026-11-05 功能名称：茶文化 App-固定下导航 -->',
    '<nav class="zwd_nav" aria-label="底部导航">',
    '  <a class="zwd_nav_item is_active" href="#" aria-label="首页">',
    '    <svg class="zwd_icon" viewBox="0 0 24 24" aria-hidden="true">…</svg>',
    '    <span class="zwd_label">首页</span>',
    '  </a>',
    '  <a class="zwd_nav_item" href="#" aria-label="茶库">',
    '    <svg class="zwd_icon" viewBox="0 0 24 24" aria-hidden="true">…</svg>',
    '    <span class="zwd_label">茶库</span>',
    '    <i class="zwd_dot" aria-hidden="true"></i>',
    '  </a>',
    '  <!-- 中间凸起按钮：记一泡 -->',
    '  <a class="zwd_nav_item zwd_center" href="#" aria-label="记一泡">',
    '    <svg class="zwd_icon" viewBox="0 0 24 24" aria-hidden="true">…</svg>',
    '    <span class="zwd_label">记一泡</span>',
    '  </a>',
    '  <a class="zwd_nav_item" href="#" aria-label="茶友">',
    '    <svg class="zwd_icon" viewBox="0 0 24 24" aria-hidden="true">…</svg>',
    '    <span class="zwd_label">茶友</span>',
    '    <i class="zwd_badge" aria-hidden="true">12</i>',
    '  </a>',
    '  <a class="zwd_nav_item" href="#" aria-label="我的">…</a>',
    '</nav>',
])
para("（3）CSS 修饰：flex: 1 让 5 个导航项均分宽度实现自适应；position: fixed 实现固定下导航；宽度 100%、最大 420px 并水平居中，模拟手机屏幕；图标大小与颜色通过 CSS 控制；徽章与红点绝对定位：", indent=False)
code([
    ':root {                                  /* 全局 CSS 变量 */',
    '  --zwd_coral: #d95d46;  --zwd_muted: #7c8792;',
    '  --zwd_card: #fffdf8;   --zwd_nav_h: 60px;  --zwd_app_w: 420px;',
    '}',
    '',
    '.zwd_app {                               /* 手机容器：最大 420px，居中 */',
    '  width: 100%; max-width: var(--zwd_app_w); margin: 0 auto;',
    '  padding-bottom: calc(var(--zwd_nav_h) + 26px);',
    '}',
    '',
    '.zwd_nav {                               /* 固定下导航 + 自适应宽度 */',
    '  position: fixed; left: 50%; bottom: 0; transform: translateX(-50%);',
    '  width: 100%; max-width: var(--zwd_app_w);',
    '  height: calc(var(--zwd_nav_h) + env(safe-area-inset-bottom, 0px));',
    '  display: flex; align-items: flex-end; z-index: 100;',
    '  background: var(--zwd_card); box-shadow: 0 -8px 26px rgba(23,33,43,.09);',
    '}',
    '',
    '.zwd_nav_item {                          /* 每项均分宽度 */',
    '  flex: 1; display: flex; flex-direction: column;',
    '  align-items: center; justify-content: center;',
    '  color: var(--zwd_muted); font-size: 11px; transition: color .2s ease;',
    '}',
    '',
    '.zwd_nav_item .zwd_icon {                 /* SVG 用 currentColor 着色 */',
    '  width: 23px; height: 23px; fill: currentColor;',
    '}',
    '.zwd_nav_item.is_active { color: var(--zwd_coral); }',
    '',
    '.zwd_nav_item.zwd_center { margin-top: -24px; }   /* 中间按钮凸起 */',
    '.zwd_nav_item.zwd_center .zwd_icon {',
    '  width: 40px; height: 40px; padding: 8px; border-radius: 50%;',
    '  background: var(--zwd_card); fill: var(--zwd_coral);',
    '  box-shadow: 0 6px 16px rgba(217,93,70,.34);',
    '}',
    '',
    '.zwd_badge {                              /* 数字徽章 */',
    '  position: absolute; top: 3px; left: calc(50% + 6px);',
    '  min-width: 16px; height: 16px; padding: 0 4px; border-radius: 999px;',
    '  background: var(--zwd_coral); color: #fffdf8; font-size: 10px; line-height: 16px;',
    '}',
    '.zwd_dot {                                /* 红点提醒 */',
    '  position: absolute; top: 8px; left: calc(50% + 8px);',
    '  width: 7px; height: 7px; border-radius: 50%; background: var(--zwd_coral);',
    '}',
])

# ============ 测试与发布 ============
h1("测试与发布")
para("给出不同视口、不同浏览器下的测试截图，给出在服务器端发布的截图（可选）。", indent=False, color=(0x66, 0x66, 0x66))
para("测试图（或发布图）：", indent=False, color=(0x66, 0x66, 0x66))
para("在不同视口（viewport）下对页面进行了测试：分别在 480px（手机）、768px（平板竖屏）、1280px（桌面）视口中运行四级项目2.html。测试结果表明：页面容器始终保持最大宽度 420px 并水平居中，下导航 fixed 固定在底部、宽度与容器一致且 5 个导航项均分宽度，中间按钮凸起正常，数字徽章与红点位置正确，SVG 图标清晰无锯齿；浏览器兼容性方面在 Edge（Chromium 内核）与 Chrome 内核浏览器下效果一致。")
fig(WORK + r"\p2_480.png", 6.8, "图5  480px 视口测试（容器 420px 居中，下导航固定底部）")
fig(WORK + r"\p2_edge_768.png", 9.4, "图6  768px 视口测试 · Edge 浏览器（导航宽度与容器一致，五栏等分）")
fig(WORK + r"\p2_1280.png", 12.4, "图7  1280px 桌面视口测试 · Chrome 浏览器（模拟手机屏幕居中效果）")
para("发布图：本次项目源码与内联 SVG 图标整理在同一文件夹内，可直接在浏览器中打开运行；因暂未申请服务器空间，尚未发布到 gitee / github 等平台，故此处省略发布截图。", indent=False)

# ============ 项目总结 ============
h1("项目总结")
para("提交项目报告者对本次项目实施过程的所得与教训进行简单分析与描述，写出项目实施心得。如果使用了 AI 必须说明使用的 AI 方法，鼓励使用 AI。", indent=False, color=(0x66, 0x66, 0x66))
para("本次“图像解决方案”实验中，我围绕三级项目“传统茶文化展示网页”完成了移动端下导航的设计与实现。在 iconfont.com 的项目（Project ID 5244853）中挑选了首页、发现、新增、微信、我的等图标，下载字体文件与 demo 页面，再把选中图标的字形轮廓转换为 SVG path 内联到页面，用 CSS 完成固定定位、五栏等分与激活态高亮，并用 420px 容器模拟手机屏幕，分别在 480px、768px、1280px 三个视口和 Chrome、Edge 两个浏览器下完成测试。")
para("通过实验，我掌握了前端图像解决方案中字体图标与 SVG 的使用方法：理解了 @font-face 加载自定义字体以及 “:before { content: \"\\eXXX\" }” 显示图标的原理，也理解了 SVG 直接把矢量图形写进 HTML、用 fill: currentColor 继承 CSS 颜色的方式；学会了通过 CSS 的 font-size / width / height 和 color / fill 灵活改变图标的大小与颜色（这正是字体图标与 SVG 相对于位图图片的优势）；练习了用 flex 布局实现导航项均分、自适应宽度；用 position: fixed + left: 50% + translateX(-50%) 实现限制宽度后的底部固定导航；还用绝对定位实现了数字徽章与红点提醒。")
para("调试中遇到的问题有两点：一是容器限制最大宽度后，fixed 定位的导航默认相对视口定位导致不居中，改用 left: 50% 加 translateX(-50%) 后解决；二是固定导航会遮挡正文最后一段内容，给容器加上 padding-bottom 并配合 env(safe-area-inset-bottom) 处理安全区后解决。这些问题的解决加深了我对定位、变换与盒模型的理解。")
para("AI 使用说明：本项目按课程要求使用了 AI 辅助开发。使用的 AI 方法是：在 AI IDE（Trae）中通过自然语言提示词与大模型（DeepSeek-V4.1-Flash）协作，由 AI 协助整理 iconfont 图标与 Unicode 的对应关系、转换字形为 SVG path，并生成下导航的 HTML 结构与 CSS 初稿；图标的语义挑选、420px 容器与固定定位的尺寸调整、配色与三个视口、两种浏览器的测试均由本人完成与核对。AI 显著提高了编码效率，但图标的语义挑选、设计还原和样式细节仍需人工把关，体会到“AI 生成 + 人工审查修改”是高效且可靠的工作方式。")

doc.save(OUT)
print("saved", OUT)
