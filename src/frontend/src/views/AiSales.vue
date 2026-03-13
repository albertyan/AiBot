<script setup>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue';
import NavBar from '../components/NavBar.vue';
import AiConfigModal from '../components/AiConfigModal.vue';
import DataStatisticsModal from '../components/DataStatisticsModal.vue';
import LogModal from '../components/LogModal.vue';
import { toggleMonitor, getMonitorStatus, refreshWeixinMessages, pullFriendMessages } from '../api/aisale';

const autoReply = ref(false);
const manualReview = ref(false);
const showAiConfigModal = ref(false);
const showDataStatisticsModal = ref(false);
const showLogModal = ref(false);
const activeTab = ref('recent');
const messageInput = ref('');
const isRefreshing = ref(false);
const isSessionRefreshing = ref(false);

/**
 * 选择左侧会话并在右侧展示消息
 * 为什么在前端做一次映射：后端仅返回会话的摘要信息（最后一条消息、时间等），
 * 为了即时交互体验，点击会话时在右侧至少展示当前已知的摘要消息，避免空白，
 * 后续可逐步接入更完整的历史消息接口以替换此映射。
 */
const currentSession = ref(null);
const messages = ref([]);
const sessionMessagesCache = ref({});
const messageContainerRef = ref(null);
const wsRef = ref(null);

/**
 * 将消息容器滚动到最底部
 * 为什么单独封装：避免在多个位置重复写同样的 nextTick + DOM 操作逻辑，降低维护成本
 */
const scrollToBottom = () => {
  nextTick(() => {
    const el = messageContainerRef.value;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  });
};

/**
 * 聚焦消息容器并滚动到底部
 * 为什么聚焦：常见聊天应用在进入会话或切换时希望键盘滚轮等操作作用于消息区
 */
const focusAndScrollToBottom = () => {
  nextTick(() => {
    const el = messageContainerRef.value;
    if (!el) return;
    try { el.focus(); } catch (_) {}
    el.scrollTop = el.scrollHeight;
  });
};


// 最近会话与历史会话分离存储
// 为什么分离：避免标签切换时复用同一数据源导致内容不变，明确数据来源与展示逻辑
const recentSessions = ref([]);
const historySessions = ref([]);
// 根据标签计算当前展示的会话列表
// 为什么用 computed：保证视图自动响应 activeTab 变化，无需手动更新
const displayedSessions = computed(() => activeTab.value === 'recent' ? recentSessions.value : historySessions.value);

/**
 * 生成会话缓存的 Key
 * 为什么不用 index：列表刷新后顺序可能变化，用稳定标识可避免拿错缓存。
 */
const getSessionKey = (session) => {
  return String(session?.id || session?.name || '');
};

/**
 * 将会话转为右侧消息列表的最小可用展示
 * 为什么只使用 last_message：当前抓取逻辑提供的是摘要；在无历史接口时，
 * 展示最后一条可以维持界面一致性与可用性，避免用户点击后右侧空白。
 */
const buildMessagesFromSession = (session) => {
  const list = [];
  const content = session?.last_message || session?.preview;
  if (content) {
    list.push({
      id: `${session.id}-last`,
      content,
      type: 'text',
      isMe: false,
      sender: session.name
    });
  }
  messages.value = list;
};

/**
 * 更新当前选择的会话
 * 为什么不在这里拉取接口：避免频繁请求；仅在用户点击“刷新消息”时才拉取并缓存。
 */
const selectSession = (session) => {
  currentSession.value = session;
  const key = getSessionKey(session);
  const cached = sessionMessagesCache.value[key];
  if (Array.isArray(cached) && cached.length > 0) {
    messages.value = cached;
    // 选中会话后将焦点置于消息区域并滚动到底部
    focusAndScrollToBottom();
    return;
  }
  buildMessagesFromSession(session);
  focusAndScrollToBottom();
};

/**
 * 拉取单个会话的历史消息并解析
 * 为什么只做解析不直接渲染：由“刷新消息”按钮统一触发拉取、缓存、更新视图，逻辑更可控。
 */
const loadFriendMessages = async (session) => {
  try {
    if (!session) return [];
    const res = await pullFriendMessages(session.name, !!session.is_group);
    let arr = res?.data?.sessions || [];
    // 消息列表默认是按时间倒序（最新在前），为了符合聊天习惯（最新在下），需要反转
    if (Array.isArray(arr)) {
      arr = [...arr].reverse();
    }
    const parsed = [];
    for (const item of arr) {
      let sender = '';
      let content = '';
      if (Array.isArray(item) && item.length >= 2) {
        sender = String(item[0] || '');
        content = String(item[1] || '');
      } else if (item && typeof item === 'object') {
        sender = String(item.sender || item.from || '');
        content = String(item.content || item.message || item.text || '');
      } else if (typeof item === 'string') {
        content = item;
      }
      const isTime = !sender && (
                /^\s*\d{1,2}:\d{2}\s*$/.test(content) || 
                /^\s*昨天\s+\d{1,2}:\d{2}\s*$/.test(content) ||
                /^\s*星期[一二三四五六日]\s+\d{1,2}:\d{2}\s*$/.test(content) ||
                /^\s*(\d{4}年)?\d{1,2}月\d{1,2}日(\s+\d{1,2}:\d{2})?\s*$/.test(content)
              );
      if (isTime) {
        parsed.push({
          id: `${session.id}-${parsed.length}-time`,
          type: 'time',
          content
        });
      } else if (content) {
        parsed.push({
          id: `${session.id}-${parsed.length}`,
          type: 'text',
          content,
          isMe: sender === 'Self',
          sender: sender === 'Self' ? '我' : (sender || session.name)
        });
      }
    }
    return parsed;
  } catch (e) {
    console.error('拉取会话消息失败', e);
    return [];
  }
};

/**
 * 刷新当前会话的消息并缓存到前端
 * 为什么要缓存：切换会话时不重复请求，且能在“只刷新才拉取”的约束下正常展示。
 */
const refreshCurrentSessionMessages = async () => {
  const session = currentSession.value;
  if (!session) return;
  
  try {
    isSessionRefreshing.value = true;
    const key = getSessionKey(session);
    const parsed = await loadFriendMessages(session);
    if (Array.isArray(parsed) && parsed.length > 0) {
      sessionMessagesCache.value = { ...sessionMessagesCache.value, [key]: parsed };
      messages.value = parsed;
    }
  } finally {
    isSessionRefreshing.value = false;
  }
};

/**
 * 当消息容器被选中（获得焦点或点击）时，将滚动条置底
 * 为什么：聊天场景默认关注最新消息，交互上聚焦即滚动到底部更符合预期
 */
const handleMessageContainerFocus = () => {
  scrollToBottom();
};

// 当消息列表发生变化时，自动滚动到底部（例如刷新或收到推送）
watch(messages, () => {
  scrollToBottom();
}, { deep: true });

/**
 * 将后端 refresh_weixin_messages 的 sessions 映射为前端会话列表结构
 * 为什么要统一映射：手动刷新与 WebSocket 推送使用同一后端模型，集中映射可避免字段分叉导致 UI 行为不一致。
 */
const mapBackendSessionsToUi = (sessionData) => {
  if (!Array.isArray(sessionData)) return [];
  return sessionData.map(s => ({
    id: s.id,
    name: s.name,
    tag: s.is_group ? '群聊' : '私聊',
    time: s.last_time,
    preview: s.last_message,
    count: s.count,
    source: s.source,
    avatarColor: 'bg-slate-400',
    is_group: !!s.is_group
  }));
};

const fetchMessages = async () => {
  try {
    isRefreshing.value = true;
    const res = await refreshWeixinMessages();
    if (res.code === 200 && res.data && res.data.sessions) {
      const sessionData = res.data.sessions;
      if (Array.isArray(sessionData)) {
        recentSessions.value = mapBackendSessionsToUi(sessionData);
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
    // 根据自动回复开关状态，决定是否连接 WebSocket
    if (autoReply.value) {
      openMessageWS();
    }
    
  } catch (error) {
    console.error('Failed to sync monitor status:', error);
  }
});

onUnmounted(() => {
  // if (refreshTimer.value) {
  //   clearInterval(refreshTimer.value);
  // }
  // 组件卸载时关闭 WebSocket，防止内存泄漏
  if (wsRef.value) {
    try { wsRef.value.close(); } catch (_) {}
    wsRef.value = null;
  }
});

const handleAutoReplyChange = async () => {
  autoReply.value = !autoReply.value;
  try {
    await toggleMonitor(autoReply.value);
    // 开关联动 WebSocket
    if (autoReply.value) {
      openMessageWS();
    } else {
      if (wsRef.value) {
        try { wsRef.value.close(); } catch (_) {}
        wsRef.value = null;
      }
    }
  } catch (error) {
    console.error(error);
    autoReply.value = !autoReply.value;
  }
};

/**
 * 建立 WebSocket 连接并监听新消息
 * 说明：后端以 5s 周期拉取新消息，通过 WS 主动推送到前端；前端被动接收并更新当前会话。
 */
const openMessageWS = () => {
  try {
    const protocol = location.protocol === 'https:' ? 'wss' : 'ws';
    const url = `${protocol}://${location.host}/ws/messages`;
    // 避免重复连接
    if (wsRef.value) {
      try { wsRef.value.close(); } catch (_) {}
      wsRef.value = null;
    }
    const ws = new WebSocket(url);
    wsRef.value = ws;
    ws.onopen = () => {
      // 简单心跳
      // try { ws.send('hi'); } catch (_) {}
      try { ws.send(JSON.stringify({ type: 'subscribe', topics: ['wechat_messages'] })); } catch (_) {}
    };
    ws.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data || '{}');
        if (data && data.type === 'wechat_chat_messages' && Array.isArray(data?.data?.messages)) {
          const senderName = String(data?.data?.sender || '').trim();
          if (!senderName) return;
          const session = (recentSessions.value || []).find(s => getSessionKey(s) === senderName || s?.name === senderName) || {
            id: senderName,
            name: senderName,
            tag: '私聊',
            time: '',
            preview: '',
            count: 0,
            source: '',
            avatarColor: 'bg-slate-400',
            is_group: false
          };
          let arr = data.data.messages;
          if (Array.isArray(arr)) {
            arr = [...arr].reverse();
          } else {
            arr = [];
          }
          const parsed = [];
          for (const item of arr) {
            let sender = '';
            let content = '';
            if (Array.isArray(item) && item.length >= 2) {
              sender = String(item[0] || '');
              content = String(item[1] || '');
            } else if (item && typeof item === 'object') {
              sender = String(item.sender || item.from || '');
              content = String(item.content || item.message || item.text || '');
            } else if (typeof item === 'string') {
              content = item;
            }
            const isTime = !sender && (
                      /^\s*\d{1,2}:\d{2}\s*$/.test(content) || 
                      /^\s*昨天\s+\d{1,2}:\d{2}\s*$/.test(content) ||
                      /^\s*星期[一二三四五六日]\s+\d{1,2}:\d{2}\s*$/.test(content) ||
                      /^\s*(\d{4}年)?\d{1,2}月\d{1,2}日(\s+\d{1,2}:\d{2})?\s*$/.test(content)
                    );
            if (isTime) {
              parsed.push({
                id: `${session.id}-${parsed.length}-time`,
                type: 'time',
                content
              });
            } else if (content) {
              parsed.push({
                id: `${session.id}-${parsed.length}`,
                type: 'text',
                content,
                isMe: sender === 'Self',
                sender: sender === 'Self' ? '我' : (sender || session.name)
              });
            }
          }
          const key = getSessionKey(session);
          if (Array.isArray(parsed) && parsed.length > 0) {
            sessionMessagesCache.value = { ...sessionMessagesCache.value, [key]: parsed };
            const current = currentSession.value;
            if (current && getSessionKey(current) === key) {
              messages.value = parsed;
            }
          }
          return;
        }
        if (data && data.type === 'refresh_weixin_messages' && Array.isArray(data?.data?.sessions)) {
          const pushed = mapBackendSessionsToUi(data.data.sessions);
          if (pushed.length <= 0) return;

          const byKey = new Map((recentSessions.value || []).map(s => [getSessionKey(s), s]));
          for (const s of pushed) {
            const key = getSessionKey(s);
            const existed = byKey.get(key);
            byKey.set(key, existed ? { ...existed, ...s } : s);
          }

          // 为什么按“推送优先”排序：推送代表新变化，置顶在前更符合聊天应用的视觉预期
          const pushedKeys = new Set(pushed.map(s => getSessionKey(s)));
          const merged = [
            ...pushed.map(s => byKey.get(getSessionKey(s))).filter(Boolean),
            ...(recentSessions.value || []).filter(s => !pushedKeys.has(getSessionKey(s)))
          ];
          recentSessions.value = merged;

          const current = currentSession.value;
          if (current) {
            const updated = byKey.get(getSessionKey(current));
            if (updated) {
              currentSession.value = updated;
              const content = String(updated.preview || '');
              if (content) {
                const last = (messages.value || [])[messages.value.length - 1];
                if (!last || last.content !== content) {
                  const msg = {
                    id: `${updated.id}-${Date.now()}-${Math.random().toString(36).slice(2,6)}`,
                    type: 'text',
                    content,
                    isMe: false,
                    sender: updated.name
                  };
                  messages.value = [...messages.value, msg];
                  const cacheKey = getSessionKey(updated);
                  const cached = sessionMessagesCache.value[cacheKey] || [];
                  sessionMessagesCache.value = { ...sessionMessagesCache.value, [cacheKey]: [...cached, msg] };
                }
              }
            }
          }
        }
      } catch (e) {
        console.error('WS parse error', e);
      }
    };
    ws.onclose = () => {
      wsRef.value = null;
    };
    ws.onerror = () => {
      try { ws.close(); } catch (_) {}
      wsRef.value = null;
    };
  } catch (e) {
    console.error('WS open failed', e);
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
          <button 
            @click="refreshCurrentSessionMessages" 
            :disabled="isSessionRefreshing"
            class="px-3 py-1.5 border border-[#1890FF] text-[#1890FF] rounded hover:bg-blue-50 transition-colors text-sm flex items-center space-x-1"
            :class="{ 'opacity-70 cursor-wait': isSessionRefreshing }"
          >
            <i class="ri-refresh-line" :class="{ 'animate-spin': isSessionRefreshing }"></i>
            <span>{{ isSessionRefreshing ? '刷新中...' : '刷新消息' }}</span>
          </button>
        </div>

        <!-- Messages Area -->
        <div
          ref="messageContainerRef"
          tabindex="0"
          @focus="handleMessageContainerFocus"
          @click="handleMessageContainerFocus"
          class="flex-1 overflow-y-auto p-6 space-y-6"
        >
          <div v-for="msg in messages" :key="msg.id" class="w-full">
            <div v-if="msg.type === 'time'" class="text-xs text-slate-400 text-center my-2">
              {{ msg.content }}
            </div>
            <div v-else class="flex items-start max-w-[80%]" :class="msg.isMe ? 'ml-auto justify-end' : ''">
              <!-- 对方头像 -->
              <div v-if="!msg.isMe" class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-white mr-2 shrink-0">
                <i class="ri-user-3-line text-slate-400"></i>
              </div>
              
              <!-- 消息内容 -->
              <div class="px-4 py-3 rounded-2xl shadow-sm text-[15px] leading-relaxed break-words"
                   :class="msg.isMe ? 'bg-[#95EC69] text-slate-900 rounded-tr-none' : 'bg-white text-slate-800 rounded-tl-none'">
                {{ msg.content }}
              </div>

              <!-- 自己头像 -->
              <div v-if="msg.isMe" class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-white ml-2 shrink-0">
                <i class="ri-user-smile-line text-slate-400"></i>
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
