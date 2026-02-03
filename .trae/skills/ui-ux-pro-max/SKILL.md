---
name: "ui-ux-pro-max"
description: "全面的 UI/UX 设计指南和验证器。在设计 UI 组件、选择颜色/排版或审查代码的 UX/可访问性时调用。"
---

# UI/UX Pro Max - 设计智能指南

适用于 Web 和移动应用程序的综合设计指南。使用此技能可确保高质量的 UI/UX 实现。

## 适用场景 (When to Apply)
在以下情况下参考这些指南：
- 设计新的 UI 组件或页面
- 选择调色板和排版
- 审查代码的 UX 问题
- 构建落地页或仪表板
- 实施无障碍（Accessibility）要求

## 快速参考与规则 (Quick Reference & Rules)

### 1. 无障碍性 (Accessibility) - [关键]
- **颜色对比度 (color-contrast)**: 普通文本的对比度至少为 4.5:1。
- **焦点状态 (focus-states)**: 交互元素必须有可见的焦点环（Focus Ring）。
- **替代文本 (alt-text)**: 为有意义的图像提供描述性 `alt` 文本。
- **ARIA 标签 (aria-labels)**: 为纯图标按钮添加 `aria-label` 属性。
- **键盘导航 (keyboard-nav)**: Tab 键顺序必须与视觉顺序一致。
- **表单标签 (form-labels)**: 使用带有 `for` 属性的 `label` 标签关联输入框。

### 2. 触控与交互 (Touch & Interaction) - [关键]
- **触控目标尺寸 (touch-target-size)**: 触控目标至少为 44x44px。
- **悬停与点击 (hover-vs-tap)**: 主要交互必须支持点击/触摸（不能仅依赖悬停）。
- **加载状态按钮 (loading-buttons)**: 异步操作期间禁用按钮并显示加载状态。
- **错误反馈 (error-feedback)**: 在问题字段附近显示清晰的错误消息。
- **鼠标指针 (cursor-pointer)**: 为所有可点击元素添加 `cursor-pointer` 样式。

### 3. 性能 (Performance) - [高]
- **图片优化 (image-optimization)**: 使用 WebP 格式, `srcset`, 和懒加载 (lazy loading)。
- **减少动画 (reduced-motion)**: 检查并尊重 `prefers-reduced-motion` 媒体查询设置。
- **内容跳动 (content-jumping)**: 为异步加载的内容预留空间（使用骨架屏 Skeleton）。

### 4. 布局与响应式 (Layout & Responsive) - [高]
- **视口设置 (viewport-meta)**: 使用 `width=device-width initial-scale=1`。
- **可读字号 (readable-font-size)**: 移动端正文文本至少 16px。
- **水平滚动 (horizontal-scroll)**: 确保内容适应视口宽度（避免意外的水平滚动条）。
- **层级管理 (z-index-management)**: 定义严格的 z-index 层级规范（例如：10, 20, 30, 50）。

### 5. 排版与色彩 (Typography & Color) - [中]
- **行高 (line-height)**: 正文文本使用 1.5-1.75 倍行高。
- **行长 (line-length)**: 每行限制 65-75 个字符以提高可读性。
- **字体搭配 (font-pairing)**: 标题与正文字体风格要协调。
- **一致性 (consistency)**: 使用定义的调色板（主色、次色、中性色、错误色、成功色）。

### 6. 动画 (Animation) - [中]
- **持续时间 (duration-timing)**: 微交互动画时长控制在 150-300ms。
- **变换性能 (transform-performance)**: 优先通过 `transform` 和 `opacity` 进行动画，避免改变 `width`/`height`/`top`/`left`。
- **加载状态 (loading-states)**: 等待时间超过 1 秒时使用骨架屏或加载指示器。

### 7. 风格选择 (Style Selection) - [中]
- **风格匹配 (style-match)**: 风格应符合产品类型（例如：金融科技用专业风，游戏用俏皮风）。
- **一致性 (consistency)**: 所有页面使用相同的风格/组件库。
- **图标使用 (no-emoji-icons)**: 界面元素优先使用 SVG 图标，避免直接使用 Emoji。

### 8. 图表与数据 (Charts & Data) - [低]
- **图表类型 (chart-type)**: 根据数据类型匹配图表（比较用柱状图，趋势用折线图）。
- **颜色指引 (color-guidance)**: 数据可视化使用无障碍调色板。
- **数据表格 (data-table)**: 为复杂图表提供表格形式的替代视图。

## 使用示例 (Examples)

### 示例 1：设计新组件
**用户指令**: "帮我设计一个用户注册表单，要求风格现代简洁。"
**Skill 响应**: 应用 **无障碍性**（标签关联、焦点态）、**触控与交互**（清晰的错误反馈、加载状态）和 **排版与色彩**（一致的间距、品牌色按钮）规则生成代码。

### 示例 2：代码审查
**用户指令**: "检查一下这个页面的代码有什么 UX 问题。"
**Skill 响应**: 对照 **快速参考与规则** 列表，检查是否存在对比度不足、缺少 Aria 标签、点击区域过小或未处理加载状态等问题，并提出修改建议。

### 示例 3：优化移动端体验
**用户指令**: "优化这个页面在手机上的显示。"
**Skill 响应**: 重点应用 **布局与响应式**（字号 >=16px，无水平滚动）和 **触控与交互**（44px 点击热区）规则进行调整。

## AI 助手工作流 (Workflow for AI Assistant)

当用户请求 UI/UX 相关工作（设计、构建、创建、实现、审查、修复、改进）时：

1.  **分析需求**: 提取产品类型（SaaS/电商等）、风格关键词、行业和技术栈。
2.  **构思设计系统**: 在编码前，先在脑海中构建调色板、排版和网格系统。
3.  **实施与验证**: 生成代码时立即应用 **无障碍性** 和 **响应式** 规则。
4.  **UX 自查**: 生成后对照上述规则清单进行检查，发现严重问题立即自动修正。
