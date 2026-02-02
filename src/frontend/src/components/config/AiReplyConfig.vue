<script setup>
import { ref } from 'vue';

const mergeReply = ref('不合并');
const monitorInterval = ref(5);
const aiOnTop = ref(false);
const transferKeywords = ref('');
const transferWechatNickname = ref('');

const safeParseInt = (value, fallback) => {
  const parsed = parseInt(value);
  return isNaN(parsed) ? fallback : Math.max(1, parsed);
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-slate-800">AI回复配置</h1>
      <button class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors whitespace-nowrap">
        保存设置
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <!-- 提示信息 -->
      <div class="flex items-start space-x-3 bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
        <i class="ri-information-fill text-blue-500 text-xl mt-0.5"></i>
        <div class="text-sm text-blue-700">
          聊天记录是自动保存本地data文件夹
        </div>
      </div>

      <div class="space-y-6">
        <!-- 消息合并回复 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-3">消息合并回复</label>
          <div class="relative">
            <select
              v-model="mergeReply"
              class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
            >
              <option value="不合并">不合并</option>
              <option value="合并">合并</option>
            </select>
            <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
          </div>
          <button class="mt-2 text-sm text-slate-500 hover:text-slate-700 flex items-center space-x-1">
            <i class="ri-question-line"></i>
            <span>查看说明</span>
          </button>
        </div>

        <!-- 消息监听间隔 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-3">消息监听间隔(秒)</label>
          <div class="flex items-center space-x-3">
            <button
              @click="monitorInterval = Math.max(1, monitorInterval - 1)"
              class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
            >
              <i class="ri-subtract-line text-slate-600"></i>
            </button>
            <input
              type="number"
              v-model.number="monitorInterval"
              @change="monitorInterval = safeParseInt($event.target.value, 1)"
              class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
            <button
              @click="monitorInterval += 1"
              class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
            >
              <i class="ri-add-line text-slate-600"></i>
            </button>
          </div>
          <button class="mt-2 text-sm text-slate-500 hover:text-slate-700 flex items-center space-x-1">
            <i class="ri-question-line"></i>
            <span>查看说明</span>
          </button>
        </div>

        <!-- AI智能体上下文 -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <label class="text-sm font-medium text-slate-700">AI智能体上下文</label>
            <div class="flex items-center space-x-2">
              <span class="text-sm text-slate-600">{{ aiOnTop ? '开启' : '关闭' }}</span>
              <button
                @click="aiOnTop = !aiOnTop"
                class="relative w-12 h-6 rounded-full transition-colors"
                :class="aiOnTop ? 'bg-[#4A90E2]' : 'bg-slate-300'"
              >
                <span
                  class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform"
                  :class="aiOnTop ? 'translate-x-6' : ''"
                ></span>
              </button>
            </div>
          </div>
        </div>

        <!-- 转人工配置 -->
        <div class="pt-4 border-t border-slate-200">
          <h3 class="text-base font-semibold text-slate-800 mb-4">转人工配置</h3>
          
          <!-- 话术词 -->
          <div class="mb-6">
            <div class="flex items-center justify-between mb-3">
              <label class="text-sm font-medium text-slate-700">话术词</label>
              <button class="px-3 py-1.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded text-xs font-medium transition-colors whitespace-nowrap">
                + 添加
              </button>
            </div>
            <p class="text-xs text-slate-500 mb-3">当AI回复中含中话术词时，将触发转人工通知</p>
            <textarea
              v-model="transferKeywords"
              placeholder="请输入话术词，多个词用逗号分隔"
              rows="3"
              class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
            ></textarea>
          </div>

          <!-- 接收通知的微信昵称 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">接收通知的微信昵称</label>
            <p class="text-xs text-slate-500 mb-3">转人工通知将发送给此微信</p>
            <input
              type="text"
              v-model="transferWechatNickname"
              placeholder="请输入用于接收转人工通知的备用微信昵称"
              class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
