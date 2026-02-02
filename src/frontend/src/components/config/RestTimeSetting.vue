<script setup>
import { ref } from 'vue';

const restStartTime = ref('00:00');
const restEndTime = ref('05:30');
const autoAddFriend = ref(true);
const autoPassFriend = ref(true);
const enableRestTime = ref(true);

const generateTimeOptions = () => {
  const options = [];
  for (let h = 0; h < 24; h++) {
    for (let m = 0; m < 60; m += 30) {
      const hour = h.toString().padStart(2, '0');
      const minute = m.toString().padStart(2, '0');
      options.push(`${hour}:${minute}`);
    }
  }
  return options;
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-slate-800">休息时间设置</h1>
      <button class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap">
        保存设置
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <!-- 启用休息时间 -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-4">
          <label class="text-sm font-medium text-slate-700">启用休息时间</label>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-slate-600">{{ enableRestTime ? '已启用' : '已禁用' }}</span>
            <button
              @click="enableRestTime = !enableRestTime"
              class="relative w-12 h-6 rounded-full transition-colors"
              :class="enableRestTime ? 'bg-[#4A90E2]' : 'bg-slate-300'"
            >
              <span
                class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform"
                :class="enableRestTime ? 'translate-x-6' : ''"
              ></span>
            </button>
          </div>
        </div>
        <p class="text-xs text-slate-500">启用后，在休息时间段内将暂停执行已勾选的任务</p>
      </div>

      <!-- 休息时间显示 -->
      <div class="mb-6 p-6 bg-gradient-to-r from-blue-50 to-teal-50 rounded-lg border border-blue-100">
        <div class="flex items-center justify-center space-x-4 mb-4">
          <div class="text-center">
            <div class="text-3xl font-bold text-[#4A90E2]">{{ restStartTime }}</div>
            <div class="text-xs text-slate-600 mt-1">开始时间</div>
          </div>
          <div class="text-2xl text-slate-400">-</div>
          <div class="text-center">
            <div class="text-3xl font-bold text-[#4A90E2]">{{ restEndTime }}</div>
            <div class="text-xs text-slate-600 mt-1">结束时间</div>
          </div>
        </div>
        
        <!-- 时间轴可视化 -->
        <div class="relative h-2 bg-slate-200 rounded-full overflow-hidden">
          <div 
            class="absolute h-full bg-[#4A90E2] rounded-full"
            style="left: 0%; width: 22.9%"
          ></div>
        </div>
        <div class="flex justify-between text-xs text-slate-500 mt-2">
          <span>00:00</span>
          <span>06:00</span>
          <span>12:00</span>
          <span>18:00</span>
          <span>24:00</span>
        </div>
      </div>

      <div class="space-y-6">
        <!-- 开始时间 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">开始时间</label>
          <div class="relative">
            <select
              v-model="restStartTime"
              class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
              :disabled="!enableRestTime"
            >
              <option v-for="time in generateTimeOptions()" :key="time" :value="time">{{ time }}</option>
            </select>
            <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
          </div>
        </div>

        <!-- 结束时间 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">结束时间</label>
          <div class="relative">
            <select
              v-model="restEndTime"
              class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
              :disabled="!enableRestTime"
            >
              <option v-for="time in generateTimeOptions()" :key="time" :value="time">{{ time }}</option>
            </select>
            <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
          </div>
        </div>

        <!-- 应用到的任务 -->
        <div class="pt-4 border-t border-slate-200">
          <h3 class="text-base font-semibold text-slate-800 mb-4">应用到的任务</h3>
          <p class="text-xs text-slate-500 mb-4">选择在休息时间内需要暂停的任务</p>
          
          <div class="space-y-3">
            <label class="flex items-center justify-between p-4 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
              <div class="flex items-center space-x-3">
                <input
                  type="checkbox"
                  v-model="autoAddFriend"
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                  :disabled="!enableRestTime"
                />
                <div>
                  <div class="text-sm font-medium text-slate-700">自动加好友</div>
                  <div class="text-xs text-slate-500">休息时间内暂停自动添加好友</div>
                </div>
              </div>
              <span v-if="autoAddFriend" class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded whitespace-nowrap">
                已应用
              </span>
            </label>

            <label class="flex items-center justify-between p-4 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
              <div class="flex items-center space-x-3">
                <input
                  type="checkbox"
                  v-model="autoPassFriend"
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                  :disabled="!enableRestTime"
                />
                <div>
                  <div class="text-sm font-medium text-slate-700">自动通过好友</div>
                  <div class="text-xs text-slate-500">休息时间内暂停自动通过好友申请</div>
                </div>
              </div>
              <span v-if="autoPassFriend" class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded whitespace-nowrap">
                已应用
              </span>
            </label>

            <label class="flex items-center justify-between p-4 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
              <div class="flex items-center space-x-3">
                <input
                  type="checkbox"
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                  :disabled="!enableRestTime"
                />
                <div>
                  <div class="text-sm font-medium text-slate-700">朋友圈自动评论</div>
                  <div class="text-xs text-slate-500">休息时间内暂停朋友圈自动评论</div>
                </div>
              </div>
            </label>

            <label class="flex items-center justify-between p-4 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
              <div class="flex items-center space-x-3">
                <input
                  type="checkbox"
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                  :disabled="!enableRestTime"
                />
                <div>
                  <div class="text-sm font-medium text-slate-700">AI自动回复</div>
                  <div class="text-xs text-slate-500">休息时间内暂停AI自动回复消息</div>
                </div>
              </div>
            </label>
          </div>

          <div class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div class="flex items-start space-x-2">
              <i class="ri-information-fill text-blue-500 text-sm mt-0.5"></i>
              <p class="text-xs text-blue-700">
                未勾选的任务不会受休息时间限制，将继续正常运行
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
