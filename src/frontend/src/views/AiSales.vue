<script setup>
import { ref } from 'vue';
import NavBar from '../components/NavBar.vue';

const autoReply = ref(false);
const manualReview = ref(false);
const showStats = ref(false);
const activeTab = ref('recent');
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <!-- 顶部导航 -->
    <NavBar />

    <!-- 主要内容区域 -->
    <div class="flex h-[calc(100vh-64px)]">
      <!-- 主内容区 -->
      <div class="flex-1 flex overflow-hidden">
        <!-- 左侧会话列表 - 40% -->
        <div class="w-[40%] bg-white border-r border-slate-200 flex flex-col">
          <!-- 控制面板 -->
          <div class="p-4 border-b border-slate-200">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-3">
                <label class="flex items-center space-x-2 cursor-pointer">
                  <div :class="`relative w-11 h-6 rounded-full transition-colors ${autoReply ? 'bg-teal-500' : 'bg-slate-300'}`">
                    <div :class="`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform ${autoReply ? 'translate-x-5' : 'translate-x-0'}`"></div>
                    <input
                      type="checkbox"
                      class="sr-only"
                      v-model="autoReply"
                    />
                  </div>
                  <span class="text-sm text-slate-700">自动回复</span>
                </label>

                <label class="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    class="w-4 h-4 text-teal-500 border-slate-300 rounded focus:ring-teal-500"
                    v-model="manualReview"
                  />
                  <span class="text-sm text-slate-700">人工复核</span>
                </label>
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <button
                @click="showStats = !showStats"
                class="flex-1 px-4 py-2 bg-gradient-to-r from-[#4A90E2] to-[#357ABD] text-white rounded-lg font-medium shadow-sm hover:shadow-md transition-all whitespace-nowrap flex items-center justify-center space-x-2 text-sm"
              >
                <i class="ri-bar-chart-line text-base"></i>
                <span>数据统计</span>
              </button>
              
              <button class="px-4 py-2 bg-white text-slate-700 rounded-lg font-medium shadow-sm hover:shadow-md transition-all border border-slate-200 whitespace-nowrap flex items-center justify-center space-x-2 text-sm">
                <i class="ri-calendar-line text-base"></i>
                <span>日志</span>
              </button>
              
              <button class="px-4 py-2 bg-gradient-to-r from-[#9B59B6] to-[#8E44AD] text-white rounded-lg font-medium shadow-sm hover:shadow-md transition-all whitespace-nowrap flex items-center justify-center space-x-2 text-sm">
                <i class="ri-settings-3-line text-base"></i>
                <span>AI助理配置</span>
              </button>
            </div>
          </div>

          <!-- 数据统计卡片 - 可折叠 -->
          <div :class="`transition-all duration-300 overflow-hidden ${showStats ? 'max-h-48' : 'max-h-0'}`">
            <div class="p-4 bg-slate-50 border-b border-slate-200">
              <div class="grid grid-cols-3 gap-3">
                <div class="bg-white rounded-lg p-3 text-center shadow-sm">
                  <div class="text-3xl font-bold text-slate-800 mb-1">0</div>
                  <div class="text-xs text-slate-500 mb-1">服务用户数</div>
                  <div class="flex items-center justify-center space-x-1 text-xs text-teal-500">
                    <i class="ri-arrow-up-line"></i>
                    <span>+0% 昨日</span>
                  </div>
                </div>

                <div class="bg-white rounded-lg p-3 text-center shadow-sm">
                  <div class="text-3xl font-bold text-slate-800 mb-1">0</div>
                  <div class="text-xs text-slate-500 mb-1">自动回复数</div>
                  <div class="flex items-center justify-center space-x-1 text-xs text-teal-500">
                    <i class="ri-arrow-up-line"></i>
                    <span>+0% 昨日</span>
                  </div>
                </div>

                <div class="bg-white rounded-lg p-3 text-center shadow-sm">
                  <div class="text-3xl font-bold text-slate-800 mb-1">0</div>
                  <div class="text-xs text-slate-500 mb-1">节省工时(小时)</div>
                  <div class="flex items-center justify-center space-x-1 text-xs text-orange-500">
                    <i class="ri-fire-line"></i>
                    <span>约节省¥0</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 会话列表 -->
          <div class="flex-1 overflow-y-auto">
            <div class="p-4">
              <div class="flex items-center justify-between mb-3">
                <div class="text-sm text-slate-600">
                  <span class="font-semibold">0</span> 条新会话
                </div>
                <button class="w-8 h-8 flex items-center justify-center bg-[#4A90E2] text-white rounded-full hover:bg-[#357ABD] transition-colors">
                  <i class="ri-refresh-line text-sm"></i>
                </button>
              </div>

              <!-- 空状态 -->
              <div class="flex flex-col items-center justify-center py-16">
                <div class="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                  <i class="ri-message-3-line text-4xl text-slate-300"></i>
                </div>
                <div class="text-sm text-slate-400">暂无新消息</div>
              </div>
            </div>
          </div>

          <!-- 底部标签切换 -->
          <div class="border-t border-slate-200">
            <div class="flex">
              <button
                @click="activeTab = 'recent'"
                :class="`flex-1 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'recent'
                    ? 'text-[#4A90E2] border-b-2 border-[#4A90E2]'
                    : 'text-slate-500 hover:text-slate-700'
                }`"
              >
                最近会话
              </button>
              <button
                @click="activeTab = 'history'"
                :class="`flex-1 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'history'
                    ? 'text-[#4A90E2] border-b-2 border-[#4A90E2]'
                    : 'text-slate-500 hover:text-slate-700'
                }`"
              >
                历史会话
              </button>
            </div>
          </div>
        </div>

        <!-- 右侧聊天区域 - 60% -->
        <div class="flex-1 flex flex-col bg-[#F5F7FA]">
        </div>
      </div>
    </div>
  </div>
</template>
