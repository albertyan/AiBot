<script setup>
import { ref } from 'vue';
import NavBar from '../components/NavBar.vue';
import AiConfigModal from '../components/AiConfigModal.vue';
import DataStatisticsModal from '../components/DataStatisticsModal.vue';
import LogModal from '../components/LogModal.vue';

const autoReply = ref(false);
const manualReview = ref(false);
const showAiConfigModal = ref(false);
const showDataStatisticsModal = ref(false);
const showLogModal = ref(false);
const activeTab = ref('recent');
const messageInput = ref('');

// Mock Data matching the image
const sessions = ref([
  {
    id: 1,
    name: '箭冠~开发群',
    tag: '群聊',
    time: '11:58',
    preview: '已置顶 [1条] 杜青: [图片]',
    source: 'albertyan',
    avatarColor: 'bg-slate-400'
  }
]);

const messages = ref([
  { id: 1, content: '手机好像打印不了', type: 'text', isMe: false, sender: '箭冠~开发群' },
  { id: 2, content: '你看一下，应该可以的', type: 'text', isMe: false, sender: '箭冠~开发群' },
  { id: 3, content: '[图片]', type: 'text', isMe: false, sender: '箭冠~开发群' }
]);

const currentSession = ref(sessions.value[0]);
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex flex-col">
    <!-- 顶部导航 -->
    <NavBar />

    <!-- 顶部控制栏 -->
    <div class="h-14 bg-white border-b border-slate-200 px-6 flex items-center justify-between shrink-0 shadow-sm z-10 relative">
      <div class="flex items-center space-x-6">
        <!-- 自动回复开关 -->
        <div class="flex items-center space-x-2 cursor-pointer" @click="autoReply = !autoReply">
          <div 
            class="w-9 h-5 rounded-full relative transition-colors duration-300 ease-in-out"
            :class="autoReply ? 'bg-[#1890FF]' : 'bg-slate-300'"
          >
            <div 
              class="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow-sm transition-transform duration-300 ease-in-out"
              :class="autoReply ? 'translate-x-4' : 'translate-x-0'"
            ></div>
          </div>
          <span class="text-sm text-slate-700 select-none">自动回复</span>
        </div>

        <!-- 人工复核复选框 -->
        <label class="flex items-center space-x-2 cursor-pointer select-none">
          <input 
            type="checkbox" 
            v-model="manualReview"
            class="w-4 h-4 text-[#1890FF] rounded border-slate-300 focus:ring-[#1890FF]"
          />
          <span class="text-sm text-slate-700">人工复核</span>
        </label>
      </div>

      <div class="flex items-center space-x-3">
        <button 
          @click="showDataStatisticsModal = true"
          class="px-3 py-1.5 bg-white border border-slate-200 text-slate-600 rounded hover:bg-slate-50 hover:text-[#1890FF] hover:border-[#1890FF] transition-colors text-sm flex items-center space-x-1"
        >
          <i class="ri-bar-chart-fill"></i>
          <span>数据统计</span>
        </button>
        <button 
          @click="showLogModal = true"
          class="px-3 py-1.5 bg-white border border-slate-200 text-slate-600 rounded hover:bg-slate-50 hover:text-[#1890FF] hover:border-[#1890FF] transition-colors text-sm flex items-center space-x-1"
        >
          <i class="ri-file-list-line"></i>
          <span>日志</span>
        </button>
        <button 
          @click="showAiConfigModal = true"
          class="px-3 py-1.5 bg-gradient-to-r from-[#7B61FF] to-[#6C5DD3] text-white rounded hover:opacity-90 transition-opacity text-sm flex items-center space-x-1 shadow-sm"
        >
          <i class="ri-robot-line"></i>
          <span>AI助理配置</span>
        </button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="flex-1 flex overflow-hidden">
      <!-- 左侧会话列表 - 280px to 350px width fixed or percentage -->
      <div class="w-[320px] bg-white border-r border-slate-200 flex flex-col flex-shrink-0">
        <!-- 顶部状态栏 -->
        <div class="px-4 py-3 border-b border-slate-100">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-2">
              <span class="text-lg font-medium text-slate-800">1 条新会话</span>
              <span class="px-2 py-0.5 bg-slate-100 text-slate-400 text-xs rounded border border-slate-200">运行中</span>
            </div>
            <div class="flex items-center space-x-2">
              <button class="w-8 h-8 flex items-center justify-center bg-[#4A90E2] text-white rounded-full hover:bg-[#357ABD] transition-colors shadow-sm">
                <i class="ri-refresh-line"></i>
              </button>
            </div>
          </div>
          <div class="text-xs font-bold text-slate-500">
            账号: ALBERTYAN
          </div>
        </div>

        <!-- 会话列表 -->
        <div class="flex-1 overflow-y-auto bg-slate-50/30">
          <div 
            v-for="session in sessions" 
            :key="session.id"
            class="p-3 cursor-pointer transition-colors hover:bg-blue-50/50"
            :class="currentSession?.id === session.id ? 'bg-[#E6F7FF] border-r-2 border-[#1890FF]' : ''"
          >
            <div class="flex items-start space-x-3">
              <!-- Avatar -->
              <div class="w-10 h-10 rounded-full bg-slate-300 flex items-center justify-center text-white shrink-0">
                <i class="ri-user-line text-xl"></i>
              </div>
              
              <!-- Content -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <div class="flex items-center space-x-2 overflow-hidden">
                    <span class="font-bold text-slate-800 truncate">{{ session.name }}</span>
                    <span class="px-1.5 py-0.5 bg-slate-100 text-slate-400 text-[10px] rounded shrink-0">{{ session.tag }}</span>
                  </div>
                  <span class="text-xs text-slate-400 shrink-0">{{ session.time }}</span>
                </div>
                
                <div class="text-sm text-slate-600 truncate mb-1">
                  {{ session.preview }}
                </div>
                
                <div class="flex items-center">
                  <span class="text-xs text-slate-400 bg-[#E6F7FF] text-[#1890FF] px-1 rounded">来自 <span class="font-medium">{{ session.source }}</span></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部标签切换 -->
        <div class="flex border-t border-slate-200 bg-white">
          <button
            @click="activeTab = 'recent'"
            class="flex-1 py-3 text-sm font-medium transition-colors relative"
            :class="activeTab === 'recent' ? 'text-[#1890FF]' : 'text-slate-500 hover:text-slate-700'"
          >
            最近会话
            <div v-if="activeTab === 'recent'" class="absolute bottom-0 left-1/2 -translate-x-1/2 w-8 h-0.5 bg-[#1890FF]"></div>
          </button>
          <button
            @click="activeTab = 'history'"
            class="flex-1 py-3 text-sm font-medium transition-colors relative"
            :class="activeTab === 'history' ? 'text-[#1890FF]' : 'text-slate-500 hover:text-slate-700'"
          >
            历史会话
            <div v-if="activeTab === 'history'" class="absolute bottom-0 left-1/2 -translate-x-1/2 w-8 h-0.5 bg-[#1890FF]"></div>
          </button>
        </div>
      </div>

      <!-- 右侧聊天区域 -->
      <div class="flex-1 flex flex-col bg-[#F5F7FA]">
        <!-- Chat Header -->
        <div class="h-16 px-6 bg-white border-b border-slate-200 flex items-center justify-between shrink-0">
          <div class="flex items-center space-x-3">
            <span class="text-lg font-bold text-slate-800">{{ currentSession?.name }}</span>
            <span class="px-2 py-0.5 bg-slate-100 text-slate-500 text-xs rounded">{{ currentSession?.tag }}</span>
          </div>
          <button class="px-3 py-1.5 border border-[#1890FF] text-[#1890FF] rounded hover:bg-blue-50 transition-colors text-sm flex items-center space-x-1">
            <i class="ri-refresh-line"></i>
            <span>刷新消息</span>
          </button>
        </div>

        <!-- Messages Area -->
        <div class="flex-1 overflow-y-auto p-6 space-y-6">
          <div v-for="msg in messages" :key="msg.id" class="flex flex-col space-y-1">
            <div class="text-xs text-slate-400 ml-1">{{ msg.sender }}</div>
            <div class="flex items-start max-w-[80%]">
              <div class="bg-white px-4 py-3 rounded-2xl rounded-tl-none shadow-sm text-slate-800 text-[15px] leading-relaxed break-words">
                {{ msg.content }}
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="h-48 bg-white border-t border-slate-200 p-4 flex flex-col shrink-0">
          <textarea
            v-model="messageInput"
            placeholder="输入消息..."
            class="flex-1 w-full resize-none outline-none text-sm text-slate-700 placeholder-slate-400 bg-transparent"
          ></textarea>
          
          <div class="flex items-center justify-end space-x-3 mt-2">
            <button class="px-4 py-1.5 border border-slate-200 rounded-full text-slate-500 hover:text-slate-700 hover:border-slate-300 transition-colors text-sm flex items-center space-x-1">
              <i class="ri-magic-line"></i>
              <span>AI生成话术</span>
            </button>
            <button class="px-6 py-1.5 bg-[#1890FF] text-white rounded-full hover:bg-[#096DD9] transition-colors text-sm font-medium shadow-sm">
              发送
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- AI Config Modal -->
    <AiConfigModal v-model="showAiConfigModal" />
    
    <!-- Data Statistics Modal -->
    <DataStatisticsModal v-model="showDataStatisticsModal" />

    <!-- Log Modal -->
    <LogModal v-model="showLogModal" />
  </div>
</template>
