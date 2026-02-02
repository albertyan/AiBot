<script setup>
import { ref } from 'vue';

// 状态定义
const taskCount = ref(0);
</script>

<template>
  <div class="flex-1 flex">
    <!-- 左侧跟单任务区域 -->
    <div class="w-[45%] bg-white border-r border-slate-200 flex flex-col">
      <!-- 头部 -->
      <div class="p-4 border-b border-slate-200 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <h2 class="text-lg font-semibold text-slate-800">自动跟单</h2>
          <span class="text-slate-500 text-sm">{{ taskCount }}人</span>
        </div>
        <div class="flex items-center space-x-4 text-sm">
          <button class="text-[#4A90E2] hover:text-[#357ABD] transition-colors">跟单设置</button>
          <button class="text-green-500 hover:text-green-600 transition-colors">编辑</button>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="flex-1 overflow-y-auto p-6">
        <!-- 空状态 -->
        <div class="flex flex-col items-center justify-center h-full pb-20">
          <div class="w-32 h-32 bg-slate-50 rounded-full flex items-center justify-center mb-6">
            <i class="ri-archive-line text-6xl text-slate-200"></i>
          </div>
          <div class="text-slate-400">暂无跟进任务</div>
        </div>
      </div>
    </div>

    <!-- 右侧操作日志区域 -->
    <div class="flex-1 bg-[#F5F7FA] flex flex-col">
      <!-- 头部 -->
      <div class="p-4 bg-white border-b border-slate-200">
        <h2 class="text-lg font-semibold text-slate-800">操作日志</h2>
      </div>

      <!-- 内容区域 -->
      <div class="flex-1 overflow-y-auto p-6">
        <!-- 空状态 -->
        <div class="flex flex-col items-center justify-center h-full pb-20">
          <div class="w-32 h-32 bg-white rounded-full flex items-center justify-center mb-6 shadow-sm">
            <i class="ri-archive-line text-6xl text-slate-200"></i>
          </div>
          <div class="text-slate-400">暂无执行日志</div>
        </div>
      </div>
    </div>
  </div>
</template>
