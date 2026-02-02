<script setup>
import { ref } from 'vue';

const apiIdentifier = ref('');
const apiUrl = ref('');
const apiKey = ref('');
const apiDescription = ref('');
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-slate-800">外部API配置</h1>
      <button class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap">
        保存配置
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <!-- 提示信息 -->
      <div class="flex items-start space-x-3 bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <i class="ri-information-fill text-blue-500 text-xl mt-0.5"></i>
        <div class="text-sm text-blue-700">
          定制API需要对接调试，可联系客服咨询
        </div>
      </div>

      <div class="space-y-6">
        <!-- API标识符 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">API标识符</label>
          <input
            type="text"
            v-model="apiIdentifier"
            placeholder="请输入API标识符"
            class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
          />
          <p class="text-xs text-slate-500 mt-2">用于识别不同的API接口</p>
        </div>

        <!-- API地址 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">API地址</label>
          <input
            type="url"
            v-model="apiUrl"
            placeholder="https://api.example.com/endpoint"
            class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
          />
        </div>

        <!-- API密钥 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">API密钥</label>
          <div class="relative">
            <input
              type="password"
              v-model="apiKey"
              placeholder="请输入API密钥"
              class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
            <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
              <i class="ri-eye-line"></i>
            </button>
          </div>
        </div>

        <!-- API描述 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">API描述</label>
          <textarea
            v-model="apiDescription"
            placeholder="请输入API的功能描述和使用说明"
            rows="4"
            class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
          ></textarea>
        </div>

        <!-- 测试按钮 -->
        <div class="flex items-center space-x-3 pt-4">
          <button class="px-6 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium transition-colors whitespace-nowrap">
            测试连接
          </button>
          <span class="text-sm text-slate-500">测试API是否可以正常连接</span>
        </div>
      </div>
    </div>

    <!-- API列表 -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <h3 class="text-base font-semibold text-slate-800 mb-4">已配置的API</h3>
      <div class="text-center py-12">
        <i class="ri-link text-5xl text-slate-300 mb-3"></i>
        <div class="text-sm text-slate-400">暂无已配置的API</div>
      </div>
    </div>
  </div>
</template>
