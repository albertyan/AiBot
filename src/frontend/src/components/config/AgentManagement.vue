<script setup>
import { ref } from 'vue';

const agents = ref([
  { id: '1', name: '过敏', botId: '75326*****55496' },
]);
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-slate-800">智能体管理</h1>
      <button class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors">
        测试
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="space-y-4">
        <div v-for="agent in agents" :key="agent.id" class="flex items-center justify-between p-4 border border-slate-200 rounded-lg">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
              <i class="ri-robot-line text-white text-lg"></i>
            </div>
            <div>
              <div class="text-sm font-semibold text-slate-800">{{ agent.name }}</div>
              <div class="text-xs text-slate-500">Bot ID: {{ agent.botId }}</div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button class="px-3 py-1.5 bg-green-50 text-green-600 rounded text-xs font-medium hover:bg-green-100 transition-colors">
              默认
            </button>
            <button class="w-8 h-8 flex items-center justify-center text-red-500 hover:bg-red-50 rounded-lg transition-colors">
              <i class="ri-delete-bin-line"></i>
            </button>
          </div>
        </div>
      </div>

      <button class="w-full mt-4 px-4 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors">
        添加智能体
      </button>
    </div>
  </div>
</template>
