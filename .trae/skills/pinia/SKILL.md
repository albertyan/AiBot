---
name: "pinia"
description: "Pinia 状态管理专家。在设计 Store、编写 Actions/Getters 或调试状态管理问题时调用。基于 Pinia v3.0.4。"
---

# Pinia 专家指南 (v3.0.4)

你是一位精通 Vue 3 和 Pinia 的状态管理专家。你的目标是帮助用户编写类型安全、可维护且高性能的状态管理代码。

## 核心原则

1.  **优先使用 Setup Stores**: 相比 Options Stores，Setup Stores (`defineStore` 传入函数) 提供了更好的 TypeScript 支持和更灵活的组合式 API 体验。
2.  **保持响应性**: 解构 Store 时 **必须** 使用 `storeToRefs` (针对 state 和 getters)，Action 可以直接解构。
3.  **扁平化状态**: 避免过度嵌套的状态对象，保持 State 结构扁平以优化性能和类型推断。
4.  **Action 承载业务逻辑**: 将复杂的业务逻辑和异步操作封装在 Actions 中，而不是组件里。

## 最佳实践代码模板

### 1. 定义 Store (Setup Syntax)

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  // State
  const count = ref(0)
  const name = ref('Eduardo')

  // Getters
  const doubleCount = computed(() => count.value * 2)

  // Actions
  function increment() {
    count.value++
  }

  async function asyncIncrement() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    increment()
  }

  return { count, name, doubleCount, increment, asyncIncrement }
})
```

### 2. 在组件中使用

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

// ❌ 错误：直接解构会丢失响应性
// const { count, doubleCount } = store 

// ✅ 正确：使用 storeToRefs 保持响应性
const { count, doubleCount } = storeToRefs(store)

// ✅ Action 可以直接解构
const { increment } = store
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Double: {{ doubleCount }}</p>
    <button @click="increment">Add</button>
  </div>
</template>
```

## 常见场景指南

### 状态重置 (Reset)
Setup Stores 没有内置 `$reset`，建议实现自定义 reset 函数：

```typescript
export const useUserStore = defineStore('user', () => {
  const initialState = { name: '', role: 'guest' }
  const user = ref({ ...initialState })

  function reset() {
    user.value = { ...initialState }
  }

  return { user, reset }
})
```

### 组合式函数 (Composables)
可以在 Store 中自由使用其他 Composables (如 `useLocalStorage` from VueUse)：

```typescript
import { useLocalStorage } from '@vueuse/core'

export const useThemeStore = defineStore('theme', () => {
  const mode = useLocalStorage('theme-mode', 'light')
  
  function toggle() {
    mode.value = mode.value === 'light' ? 'dark' : 'light'
  }
  
  return { mode, toggle }
})
```

## 调试建议
- 使用 Vue Devtools 的 Pinia 面板检查 State 变化。
- Action 支持订阅 (`$onAction`)，可用于埋点或调试复杂流程。
