<script setup>
import { ref } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';

const route = useRoute();
const router = useRouter();
const isMobileMenuOpen = ref(false);

const goLaunch = () => {
  router.push('/');
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

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
  const activeClass = "text-primary-300 bg-white/5 border-b-2 border-primary-400 font-medium";
  const inactiveClass = "text-slate-300 hover:text-white hover:bg-white/10";
  
  return `${baseClass} ${isActive(path) ? activeClass : inactiveClass}`;
}

const getMobileLinkClass = (path) => {
  const baseClass = "block px-4 py-3 rounded-md text-base font-medium transition-colors border-l-4 border-transparent";
  const activeClass = "text-primary-300 bg-white/10 border-l-primary-400";
  const inactiveClass = "text-slate-300 hover:text-white hover:bg-white/5";
  return `${baseClass} ${isActive(path) ? activeClass : inactiveClass}`;
}
</script>

<template>
  <nav class="bg-[#3B4A5C] border-b border-[#2d3a4b] sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div 
          class="flex items-center space-x-3 cursor-pointer hover:opacity-90 transition-opacity" 
          @click="goLaunch"
          role="button"
          tabindex="0"
          aria-label="返回首页"
          @keydown.enter="goLaunch"
        >
          <div class="w-8 h-8 bg-gradient-to-br from-primary-400 to-primary-600 rounded flex items-center justify-center shadow-lg shadow-primary-500/20">
            <i class="ri-robot-2-line text-white text-lg"></i>
          </div>
          <span class="text-white text-lg font-medium tracking-wide">安伦科技</span>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center space-x-1">
          <RouterLink to="/home" :class="getLinkClass('/home')">欢迎</RouterLink>
          <RouterLink to="/ai-sales" :class="getLinkClass('/ai-sales')">AI销冠</RouterLink>
          <RouterLink to="/customer-management" :class="getLinkClass('/customer-management')">客户管理</RouterLink>
          <RouterLink to="/moments" :class="getLinkClass('/moments')">朋友圈</RouterLink>
          <RouterLink to="/automation-sop" :class="getLinkClass('/automation-sop')">自动化SOP</RouterLink>
          <RouterLink to="/config" :class="getLinkClass('/config')">配置</RouterLink>
        </div>

        <!-- Mobile Menu Button -->
        <button 
          @click="toggleMobileMenu" 
          class="md:hidden w-10 h-10 flex items-center justify-center text-slate-300 hover:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-lg"
          aria-label="切换导航菜单"
          :aria-expanded="isMobileMenuOpen"
        >
          <i :class="isMobileMenuOpen ? 'ri-close-line' : 'ri-menu-line'" class="text-2xl"></i>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-show="isMobileMenuOpen" class="md:hidden bg-[#3B4A5C] border-t border-[#2d3a4b] px-4 pt-2 pb-4 space-y-2 shadow-lg animate-fade-in-down">
      <RouterLink to="/home" :class="getMobileLinkClass('/home')" @click="isMobileMenuOpen = false">欢迎</RouterLink>
      <RouterLink to="/ai-sales" :class="getMobileLinkClass('/ai-sales')" @click="isMobileMenuOpen = false">AI销冠</RouterLink>
      <RouterLink to="/customer-management" :class="getMobileLinkClass('/customer-management')" @click="isMobileMenuOpen = false">客户管理</RouterLink>
      <RouterLink to="/moments" :class="getMobileLinkClass('/moments')" @click="isMobileMenuOpen = false">朋友圈</RouterLink>
      <RouterLink to="/automation-sop" :class="getMobileLinkClass('/automation-sop')" @click="isMobileMenuOpen = false">自动化SOP</RouterLink>
      <RouterLink to="/config" :class="getMobileLinkClass('/config')" @click="isMobileMenuOpen = false">配置</RouterLink>
    </div>
  </nav>
</template>
