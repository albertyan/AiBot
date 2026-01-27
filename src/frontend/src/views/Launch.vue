<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const handleLaunch = () => {
  router.push('/home');
};
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center relative overflow-hidden">
    <!-- 背景装饰 (柔和流光) -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
      <!-- 顶部光晕 -->
      <div class="absolute -top-[20%] -left-[10%] w-[800px] h-[800px] bg-blue-100/40 rounded-full blur-3xl opacity-60"></div>
      <div class="absolute -bottom-[20%] -right-[10%] w-[800px] h-[800px] bg-indigo-100/40 rounded-full blur-3xl opacity-60"></div>
      
      <!-- 科技网格背景 -->
      <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTAgMGg0MHY0MEgwVjB6bTEgMWgzOHYzOEgxVjF6IiBmaWxsPSIjOTRBN0I4IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIG9wYWNpdHk9IjAuMSIvPjwvc3ZnPg==')] opacity-30"></div>
    </div>

    <div class="bg-white/80 backdrop-blur-xl border border-white/50 rounded-2xl shadow-2xl shadow-blue-900/5 p-12 max-w-xl w-full mx-4 relative z-10">
      <!-- 标题区域 -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-slate-800 mb-3 tracking-tight">
        Anlunai <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-500 to-blue-600 text-xl font-medium ml-1">v1.5.5</span>
      </h1>
      <div class="flex items-center justify-center space-x-3 mt-4">
        <div class="h-[2px] w-6 bg-gradient-to-r from-teal-400 to-teal-600 rounded-full"></div>
        <p class="text-slate-500 text-xs tracking-[0.2em] uppercase font-bold">AI Intelligent Assistant</p>
        <div class="h-[2px] w-6 bg-gradient-to-r from-teal-600 to-teal-400 rounded-full"></div>
      </div>
    </div>

    <!-- 启动向导 -->
    <div class="mb-10">
      <h2 class="text-lg font-bold text-slate-800 mb-6 flex items-center">
        <span class="w-1.5 h-5 bg-gradient-to-b from-teal-500 to-blue-600 rounded-full mr-3"></span>
        启动向导
      </h2>
      
      <div class="space-y-5 mb-6 pl-1">
        <div class="flex items-start space-x-4 group">
          <div class="w-7 h-7 bg-white border border-slate-200 shadow-sm rounded-lg flex items-center justify-center shrink-0 group-hover:bg-teal-500 group-hover:border-teal-500 transition-all duration-300">
            <span class="font-bold text-xs text-slate-500 group-hover:text-white transition-colors duration-200">01</span>
          </div>
          <p class="text-slate-600 text-sm leading-7">请确保已登录至少 <span class="text-teal-600 font-bold">1个</span> 微信号</p>
        </div>

        <div class="bg-teal-50/50 border border-teal-100 rounded-lg p-4 flex items-start space-x-3">
          <i class="ri-information-fill text-teal-500 text-lg mt-0.5"></i>
          <p class="text-teal-700 text-sm leading-relaxed font-medium">确保微信窗口可见，不要最小化或关闭</p>
        </div>

        <div class="flex items-start space-x-4 group">
          <div class="w-7 h-7 bg-white border border-slate-200 shadow-sm rounded-lg flex items-center justify-center shrink-0 group-hover:bg-teal-500 group-hover:border-teal-500 transition-all duration-300">
            <span class="font-bold text-xs text-slate-500 group-hover:text-white transition-colors duration-200">02</span>
          </div>
          <p class="text-slate-600 text-sm leading-7">点击启动应用后，请勿操作鼠标</p>
        </div>

        <div class="flex items-start space-x-4 group">
          <div class="w-7 h-7 bg-white border border-slate-200 shadow-sm rounded-lg flex items-center justify-center shrink-0 group-hover:bg-teal-500 group-hover:border-teal-500 transition-all duration-300">
            <span class="font-bold text-xs text-slate-500 group-hover:text-white transition-colors duration-200">03</span>
          </div>
          <p class="text-slate-600 text-sm leading-7">以上知晓后，点击下方按钮启动应用</p>
        </div>
      </div>
    </div>

    <!-- 启动按钮 -->
    <button
      @click="handleLaunch"
      class="group w-full bg-gradient-to-r from-teal-500 to-blue-600 hover:from-teal-600 hover:to-blue-700 text-white py-4 rounded-xl font-bold text-lg transition-all shadow-lg shadow-teal-500/20 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
    >
        <span class="flex items-center justify-center">
          <i class="ri-rocket-fill mr-2 group-hover:translate-x-1 transition-transform"></i>
          启动应用
        </span>
      </button>

      <!-- 免责声明 -->
      <div class="mt-10 text-center border-t border-slate-100 pt-6">
        <p class="text-xs text-slate-400 flex items-center justify-center gap-2">
          <i class="ri-shield-check-line"></i>
          <span>安全保障 · 仅供日常交流 · 严禁非法用途</span>
        </p>
      </div>
    </div>
  </div>
</template>
