<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import NavBar from '../components/NavBar.vue';
import AiConfigModal from '../components/AiConfigModal.vue';
import DataStatisticsModal from '../components/DataStatisticsModal.vue';
import LogModal from '../components/LogModal.vue';
import { toggleMonitor, getMonitorStatus, refreshWeixinMessages } from '../api/aisale';

const autoReply = ref(false);
const manualReview = ref(false);
const showAiConfigModal = ref(false);
const showDataStatisticsModal = ref(false);
const showLogModal = ref(false);
const activeTab = ref('recent');
const messageInput = ref('');
const refreshTimer = ref(null);
const isRefreshing = ref(false);

/**
 * 选择左侧会话并在右侧展示消息
 * 为什么在前端做一次映射：后端仅返回会话的摘要信息（最后一条消息、时间等），
 * 为了即时交互体验，点击会话时在右侧至少展示当前已知的摘要消息，避免空白，
 * 后续可逐步接入更完整的历史消息接口以替换此映射。
 */
const currentSession = ref(null);
const messages = ref([]);
// 最近会话与历史会话分离存储
// 为什么分离：避免标签切换时复用同一数据源导致内容不变，明确数据来源与展示逻辑
const recentSessions = ref([]);
const historySessions = ref([]);
// 根据标签计算当前展示的会话列表
// 为什么用 computed：保证视图自动响应 activeTab 变化，无需手动更新
const displayedSessions = computed(() => activeTab.value === 'recent' ? recentSessions.value : historySessions.value);

/**
 * 将会话转为右侧消息列表的最小可用展示
 * 为什么只使用 last_message：当前抓取逻辑提供的是摘要；在无历史接口时，
 * 展示最后一条可以维持界面一致性与可用性，避免用户点击后右侧空白。
 */
const buildMessagesFromSession = (session) => {
  const list = [];
  if (session?.last_message) {
    list.push({
      id: `${session.id}-last`,
      content: session.last_message,
      type: 'text',
      isMe: false,
      sender: session.name
    });
  }
  messages.value = list;
};

/**
 * 更新当前选择的会话
 * 为什么在点击时同步构建消息：减少额外等待，提升选择反馈速度。
 */
const selectSession = (session) => {
  currentSession.value = session;
  buildMessagesFromSession(session);
};

const fetchMessages = async () => {
  try {
    isRefreshing.value = true;
    const res = await refreshWeixinMessages();
    if (res.code === 200 && res.data && res.data.sessions) {
      // Transform backend data to frontend format if necessary
      // Assuming backend returns sessions in a format we can adapt
      // Example backend structure based on previous context: {"sessions": {...}}
      // We need to map it to sessions array format
      
      // Since I don't see the exact response structure of refresh_weixin_messages in the context
      // I will assume it returns a list or a dict that needs transformation.
      // However, looking at aisale.py (user provided context), it returns {"sessions": newMessages_dict}
      
      // Let's adapt based on the provided mock structure for now, 
      // but ideally we should populate it with real data.
      // If the backend just returns the count or status, we might need another API to get the list.
      // But let's assume res.data.sessions contains the session list.
      
      const sessionData = res.data.sessions;
      if (Array.isArray(sessionData)) {
         recentSessions.value = sessionData.map(s => ({
            id: s.id,
            name: s.name,
            tag: s.is_group ? '群聊' : '私聊',
            time: s.last_time,
            preview: s.last_message,
            count: s.count,
            source: s.source,
            avatarColor: 'bg-slate-400'
         }));
         // 默认选中第一条会话以避免右侧空白
         if (!currentSession.value && recentSessions.value.length > 0) {
           selectSession(recentSessions.value[0]);
         }
      }
    }
  } catch (error) {
    console.error('Failed to refresh messages:', error);
  } finally {
    isRefreshing.value = false;
  }
};

onMounted(async () => {
  try {
    const res = await getMonitorStatus();
    if (res.code === 200) {
      autoReply.value = res.data.enabled;
    }
    
    // // Initial fetch
    // await fetchMessages();
    
    // // Set up polling every 5 seconds (or appropriate interval)
    // refreshTimer.value = setInterval(fetchMessages, 5000);
    
  } catch (error) {
    console.error('Failed to sync monitor status:', error);
  }
});

onUnmounted(() => {
  // if (refreshTimer.value) {
  //   clearInterval(refreshTimer.value);
  // }
});

const handleAutoReplyChange = async () => {
  autoReply.value = !autoReply.value;
  try {
    await toggleMonitor(autoReply.value);
  } catch (error) {
    console.error(error);
    autoReply.value = !autoReply.value;
  }
};

// 当会话列表变化且当前未选择时，自动选中第一项
watch(displayedSessions, (val) => {
  if (!currentSession.value && Array.isArray(val) && val.length > 0) {
    selectSession(val[0]);
  }
});
// 标签切换时重置选中并选取新列表的第一项
watch(activeTab, () => {
  const list = displayedSessions.value || [];
  currentSession.value = null;
  if (list.length > 0) {
    selectSession(list[0]);
  } else {
    messages.value = [];
  }
});
</script>
<template>
  <div class="h-screen overflow-hidden bg-slate-50 flex flex-col">

    <!-- 顶部控制栏 -->
    <!-- 顶部导航 -->
    <NavBar />

    <!-- 顶部控制栏 -->
    <div class="h-14 bg-white border-b border-slate-200 px-6 flex items-center justify-between shrink-0 shadow-sm z-10 relative">
      <div class="flex items-center space-x-6">
        <!-- 自动回复开关 -->
        <div 
          class="flex items-center space-x-2 cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#1890FF] rounded-lg p-1" 
          @click="handleAutoReplyChange"
          @keydown.enter.prevent="handleAutoReplyChange"
          @keydown.space.prevent="handleAutoReplyChange"
          role="switch"
          :aria-checked="autoReply"
          tabindex="0"
          aria-label="自动回复开关"
        >
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
        <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between shrink-0">
          <div class="flex items-center space-x-2">
            <span class="text-lg font-medium text-slate-800">1 条新会话</span>
            <span class="px-2 py-0.5 bg-slate-100 text-slate-400 text-xs rounded border border-slate-200">运行中</span>
          </div>
          <div class="flex items-center space-x-2">
            <button 
              @click="fetchMessages" 
              class="w-8 h-8 flex items-center justify-center bg-[#4A90E2] text-white rounded-full hover:bg-[#357ABD] transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#4A90E2]"
              :class="{ 'opacity-75 cursor-wait': isRefreshing }"
              :disabled="isRefreshing"
              title="刷新消息"
            >
              <i class="ri-refresh-line" :class="{ 'animate-spin': isRefreshing }"></i>
            </button>
          </div>
        </div>

        <div class="px-4 py-2 bg-slate-50 border-b border-slate-100 text-sm font-bold text-slate-500 flex items-center shrink-0">
           账号: ALBERTYAN
        </div>

        <!-- 会话列表 -->
        <div class="flex-1 min-h-0 overflow-y-auto bg-white">
          <div 
            v-for="session in displayedSessions" 
            :key="session.id"
            class="px-4 py-3 border-b border-slate-50 cursor-pointer transition-colors hover:bg-slate-50"
            :class="(currentSession && currentSession.id) === session.id ? 'bg-blue-50/50 border-l-2 border-blue-500' : ''"
            @click="selectSession(session)"
          >
            <div class="flex items-start space-x-3">
              <!-- Avatar -->
              <div class="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center text-white shrink-0">
                <i class="ri-user-line text-xl text-slate-400"></i>
              </div>
              
              <!-- Content -->
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-0.5">
                  <div class="flex items-center space-x-2 overflow-hidden">
                    <span class="font-bold text-slate-800 truncate text-[15px]">{{ session.name }}</span>
                    <span class="px-1.5 py-0.5 bg-slate-100 text-slate-500 text-[10px] rounded shrink-0">{{ session.tag }}</span>
                  </div>
                  <span class="text-xs text-slate-400 shrink-0">{{ session.time }}</span>
                </div>
                
                <div class="text-sm text-slate-500 truncate mb-1.5 flex items-center">
                  <span v-if="session.count > 0" class="text-slate-500 mr-1">[{{ session.count }}条]</span>
                  <span>{{ session.preview }}</span>
                </div>
                
                <div class="flex items-center">
                  <span class="text-xs text-slate-400 mr-1.5">来自</span>
                  <span class="text-xs bg-blue-100 text-blue-500 px-1.5 py-0.5 rounded font-medium">{{ session.source }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部标签切换 -->
        <div class="flex border-t border-slate-200 bg-white shrink-0">
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
            <span class="text-lg font-bold text-slate-800">{{ currentSession ? currentSession.name : '' }}</span>
            <span class="px-2 py-0.5 bg-slate-100 text-slate-500 text-xs rounded">{{ currentSession ? currentSession.tag : '' }}</span>
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
