---
name: "vue-best-practices"
description: "Vue 3 最佳实践、常见陷阱与性能优化指南。在编写 Vue 组件、调试响应式问题或进行代码审查时调用。"
---

# Vue 3 最佳实践 (Vue Best Practices)

本技能基于 antfu/skills 的 Vue 最佳实践整理，旨在帮助开发者编写高质量、高性能且易于维护的 Vue 3 代码。

## 核心原则

在编写 Vue 代码时，请遵循以下核心原则：

### 1. 响应式系统 (Reactivity)

- **优先使用 `ref` 而非 `reactive`**: `ref` 更显式，且能避免解构丢失响应性的问题。
  - *避免*: `const state = reactive({ count: 0 })`
  - *推荐*: `const count = ref(0)`
- **脚本中访问 `ref` 需加 `.value`**: 在 `<script setup>` 中必须通过 `.value` 读写，模板中自动解包。
- **解构 `reactive` 对象会丢失响应性**: 如果必须解构，使用 `toRefs`。
- **数组/集合中的 `ref` 需要 `.value`**: `ref` 只有作为顶层属性时才会在模板中自动解包，在数组或 Map 中不会。
- **大型对象使用 `shallowRef`**: 对于不需要深层响应的大型数据（如可视化图表数据、地图数据），使用 `shallowRef` 提升性能。

### 2. 计算属性 (Computed)

- **计算属性不应有副作用**: `computed` 仅用于派生状态，不要在其中进行 DOM 操作或异步请求。
- **避免修改计算属性**: 计算属性默认是只读的。
- **计算属性返回新引用**: 避免在计算属性中直接修改数组（如 `sort`, `reverse`），应先拷贝副本 `[...arr].sort()`。
- **避免在计算属性中接收参数**: 计算属性不应是函数。如果需要参数，请使用普通函数。

### 3. 侦听器 (Watchers)

- **侦听响应式对象属性需要 getter**: `watch(() => obj.count, ...)` 而非 `watch(obj.count, ...)`。
- **明确 `watch` vs `watchEffect`**: `watch` 用于懒执行且需要访问旧值；`watchEffect` 用于自动追踪依赖。
- **异步依赖追踪**: `watchEffect` 只能追踪同步执行期间访问的响应式状态。`await` 之后的访问不会被追踪。
- **访问更新后的 DOM**: 使用 `flush: 'post'` 选项（或 `watchPostEffect`）来在 DOM 更新后触发回调。

### 4. 组件与 Props (Components & Props)

- **Props 是只读的**: 永远不要在子组件中修改 props。应该通过 emit 事件通知父组件修改。
- **组件命名使用 PascalCase**: 如 `<MyComponent />`，区分于原生 HTML 元素。
- **优先使用 Props/Emit 通信**: 避免滥用 `ref` 直接访问子组件实例（紧耦合）。
- **定义 Props 类型**: 始终为 props 定义类型和默认值。

### 5. 模板与渲染 (Templates)

- **`v-for` 中使用 `key`**: 始终为列表渲染提供唯一的 `key`。
- **避免 `v-if` 和 `v-for` 同级使用**: 优先使用计算属性过滤列表。
- **`v-html` 防范 XSS**: 仅对可信内容使用 `v-html`。
- **`v-if` vs `v-show`**: 频繁切换显示状态用 `v-show`（CSS切换），条件很少改变用 `v-if`（DOM销毁重建）。

### 6. 生命周期 (Lifecycle)

- **生命周期钩子同步注册**: `onMounted` 等钩子必须在 `setup` 函数同步执行期间调用，不能放在 `await` 之后。
- **避免在 `updated` 钩子中执行昂贵操作**: 这会严重拖慢渲染性能。

## AI 助手使用指南

当用户请求以下任务时，请参考此技能：
1. **代码审查**: 检查用户代码是否违反上述原则。
2. **重构**: 将 Vue 2 代码或不规范的 Vue 3 代码重构为最佳实践风格。
3. **性能优化**: 识别不必要的重渲染或深层响应式开销。
4. **Bug 修复**: 尤其是关于响应式丢失、计算属性不更新等问题。

在生成代码时，**默认使用 `<script setup>` 和 Composition API**。
