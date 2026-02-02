<script setup>
import { ref } from 'vue';

const cozeToken = ref('');
const difyUrl = ref('');
</script>

<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-slate-800">AI接入配置</h1>

    <!-- Coze平台 -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
            <i class="ri-robot-line text-white text-lg"></i>
          </div>
          <h2 class="text-lg font-semibold text-slate-800">Coze平台</h2>
        </div>
        <button class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors">
          清除全部缓存
        </button>
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">Coze Token</label>
          <div class="relative">
            <input
              type="password"
              v-model="cozeToken"
              placeholder="请输入Coze Token"
              class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
            <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
              <i class="ri-eye-line"></i>
            </button>
          </div>
          <p class="text-xs text-orange-500 mt-2">token已使用 176 天，如果永久期限，记得到期及时更换</p>
        </div>
      </div>
    </div>

    <!-- Dify平台 -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="flex items-center space-x-3 mb-6">
        <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
          <i class="ri-robot-2-line text-white text-lg"></i>
        </div>
        <h2 class="text-lg font-semibold text-slate-800">Dify平台</h2>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 mb-2">服务器地址</label>
        <input
          type="text"
          v-model="difyUrl"
          placeholder="如果是本地则默认可输入：http://localhost/v1"
          class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
        />
      </div>
    </div>
  </div>
</template>
