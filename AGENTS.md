# AGENTS.md

## 项目概述

本项目是 525 郑雯迪的《高级网页设计》课堂实践作品集，包含 13 个 HTML 练习页面，
涵盖 HTML 基础、CSS 选择器、盒模型、Flex 布局、CSS3 过渡动画等知识点。

## 技术栈

- **纯原生 HTML / CSS / JavaScript**，不使用任何第三方库或 CDN
- 内联 `<style>` 标签编写样式，内联 `<script>` 编写脚本
- 响应式设计（`@media` 查询、`clamp()` 函数）
- 语义化 HTML 标签（`header`、`main`、`section`、`footer`）
- 图标统一使用 `font/` 目录下的 iconfont 字体图标（`iconfont.css` + `iconfont.ttf`），禁止引入 font-awesome、lucide 等外部图标库
- 数据获取统一使用原生 `fetch()` API

## 文件命名规范

| 文件 | 说明 |
|------|------|
| `index.html` | 作品集首页（导航目录页） |
| `1.html` ~ `9-1transtion.html` | 课堂练习页面，按章节编号命名 |
| `css.css` | 独立的 CSS 练习文件 |
| `img/` | 图片资源目录 |
| `cdn/` | ⚠️ 历史遗留目录（font-awesome / lucide），**禁止在新页面中引用** |

## 代码风格

- 使用 CSS 自定义属性（`--ink`、`--coral`、`--blue`、`--yellow` 等）管理配色
- 字体优先使用系统字体（`Microsoft YaHei`、`PingFang SC`、`Georgia`、`Songti SC`）
- 布局优先使用 CSS Grid 和 Flexbox
- 使用 `clamp()` 实现流式排版
- 颜色方案：米色背景 + 珊瑚红/深蓝/暖黄点缀

## 开发约定

- 新建的 HTML 文件必须同步添加到 `index.html` 的导航卡片中
- 所有页面必须可直接在浏览器打开，无需构建工具
- 保持中文注释和中文内容
- 新增练习页面时，需同步更新 `index.html` 中的导航卡片
- 使用相对路径引用本地资源（如图片）
- 页面需具备基本的可访问性（`aria-labelledby`、`alt` 属性等）
- **每个 HTML 页面 `<head>` 标签内必须包含页面注释**，格式如下：
  ```html
  <!--
  姓名：郑雯迪
  日期：yyyy-mm-dd
  功能名称：（填写当前页面实际功能，如"CSS 变量主题切换演示"）
  -->
  ```

## 命名规范

- 所有 CSS 类名、id 名、JS 变量名都必须以 `yl_` 开头

## 提示词记录

- 每次执行任务前，需将提示词以附加方式写入 `zheng_prompt.md`，不覆盖之前的内容
- 写入内容包括：
  - 时间（格式：`yyyy-mm-dd-hh-mm`）
  - 使用的模型
  - 提示词内容
