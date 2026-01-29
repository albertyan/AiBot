<script setup>
import { useRoute, useRouter, RouterLink } from 'vue-router';

const route = useRoute();
const router = useRouter();

const goLaunch = () => {
  router.push('/');
}

/**
 * 为什么需要 isActive：
 * - 根据当前路由高亮对应的导航项，减少用户定位成本
 * - 仅比较 path，避免复杂匹配导致误高亮
 */
const isActive = (path) => route.path === path;

/**
 * 为什么这样设计选中样式：
 * - 使用轻微浅色背景提升选中块的可辨识度，同时保持深色导航的稳重
 * - 文字用金色（更显层级与状态强调），对比度在深色背景下更友好
 * - 底部加 2px 的下划线强化“当前页签”的视觉锚点，贴合参考图
 * - 通过函数封装统一生成类名，保证后续扩展一致性
 */
const getLinkClass = (path) => {
  const baseClass = "transition-all whitespace-nowrap text-[15px] px-5 py-2 rounded-md tracking-wide border-b-2 border-transparent";
  const activeClass = "text-[#F6C84E] bg-white/5 border-b-2 border-[#F6C84E] font-medium";
  const inactiveClass = "text-[#a0aec0] hover:text-white hover:bg-white/10";
  
  return `${baseClass} ${isActive(path) ? activeClass : inactiveClass}`;
}
</script>

<template>
  <nav class="bg-[#3B4A5C] border-b border-[#2d3a4b] sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center space-x-3 cursor-pointer hover:opacity-90 transition-opacity" @click="goLaunch">
          <div class="w-8 h-8 bg-gradient-to-br from-teal-400 to-teal-500 rounded flex items-center justify-center shadow-lg shadow-teal-500/20">
            <i class="ri-robot-2-line text-white text-lg"></i>
          </div>
          <span class="text-white text-lg font-medium tracking-wide">安伦科技</span>
        </div>
        <div class="flex items-center space-x-1">
          <RouterLink to="/home" :class="getLinkClass('/home')">欢迎</RouterLink>
          <RouterLink to="/ai-sales" :class="getLinkClass('/ai-sales')">AI销冠</RouterLink>
          <RouterLink to="/customer-management" :class="getLinkClass('/customer-management')">客户管理</RouterLink>
          <RouterLink to="/moments" :class="getLinkClass('/moments')">朋友圈</RouterLink>
          <RouterLink to="/automation-sop" :class="getLinkClass('/automation-sop')">自动化SOP</RouterLink>
          <RouterLink to="/config" :class="getLinkClass('/config')">配置</RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>
