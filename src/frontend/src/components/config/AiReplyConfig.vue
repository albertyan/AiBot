<script setup>
import { ref, onMounted, watch } from 'vue';
import { message } from 'ant-design-vue';
import { getChatHistorySettings, saveChatHistorySettings } from '../../api/setting';

const mergeReply = ref('none');
const monitorInterval = ref(5);
const aiOnTop = ref(false);
const contextHistoryCount = ref(5);
const transferKeywords = ref([]);
const transferWechatNickname = ref('');

// 添加关键词相关
const showAddKeywordInput = ref(false);
const newKeyword = ref('');

// 标记是否正在初始化加载，避免触发 watch
const isInitializing = ref(true);

const safeParseInt = (value, fallback) => {
  const parsed = parseInt(value);
  return isNaN(parsed) ? fallback : Math.max(1, parsed);
};

const addKeyword = () => {
  if (newKeyword.value.trim()) {
    if (!transferKeywords.value.includes(newKeyword.value.trim())) {
      transferKeywords.value.push(newKeyword.value.trim());
    }
    newKeyword.value = '';
    showAddKeywordInput.value = false;
  }
};

const removeKeyword = (index) => {
  transferKeywords.value.splice(index, 1);
};

// 获取配置
const fetchSettings = async () => {
  try {
    const res = await getChatHistorySettings();
    if (res.code === 200 && res.data && res.data.chat_history_settings) {
      const settings = res.data.chat_history_settings;
      
      // 映射配置到前端状态
      mergeReply.value = settings.messageMerge?.mode || 'none';
      monitorInterval.value = settings.messageMerge?.interval || 5;
      aiOnTop.value = settings.includeContext !== false; // 默认为 true
      contextHistoryCount.value = settings.contextCount || 7;
      transferKeywords.value = settings.transferConfig?.phrases || [];
      transferWechatNickname.value = settings.transferConfig?.notifyWechat || '';
    }
  } catch (error) {
    console.error('获取 AI 回复配置失败:', error);
    message.error('获取配置失败');
  } finally {
    // 延迟一点设置初始化完成，避免 watch 立即触发
    setTimeout(() => {
      isInitializing.value = false;
    }, 100);
  }
};

// 保存配置
const saveSettings = async () => {
  if (isInitializing.value) return;

  const config = {
    chat_history_settings: {
      autoSave: false, // 保持默认
      includeContext: aiOnTop.value,
      contextCount: contextHistoryCount.value,
      includeUserInfo: false, // 保持默认
      messageMerge: {
        mode: mergeReply.value,
        interval: monitorInterval.value
      },
      transferConfig: {
        phrases: transferKeywords.value,
        notifyWechat: transferWechatNickname.value
      }
    }
  };

  try {
    const res = await saveChatHistorySettings(config);
    if (res.code !== 200) {
      message.error(res.msg || '保存配置失败');
    }
    message.success('配置已保存');
  } catch (error) {
    console.error('保存 AI 回复配置失败:', error);
    message.error('保存配置失败');
  }
};

// 监听数据变化自动保存
watch(
  [mergeReply, monitorInterval, aiOnTop, contextHistoryCount, transferKeywords, transferWechatNickname],
  () => {
    saveSettings();
  },
  { deep: true }
);

onMounted(() => {
  fetchSettings();
});
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm h-full">
    <!-- 顶部标题 -->
    <div class="p-6 border-b border-slate-100">
      <h1 class="text-lg font-bold text-slate-800 mb-1">AI回复配置</h1>
      <p class="text-xs text-slate-400">聊天记录自动保存本地data文件夹</p>
    </div>

    <div class="p-6 space-y-6">
      <!-- 基础配置 -->
      <div class="space-y-6">
        <!-- 消息合并回复 -->
        <div class="flex items-center justify-between">
          <label class="text-sm font-medium text-slate-700">消息合并回复</label>
          <div class="flex items-center space-x-2">
            <div class="relative w-32">
              <select
                v-model="mergeReply"
                class="w-full pl-3 pr-8 py-1.5 bg-white border border-slate-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
              >
                <option value="none">不合并</option>
                <option value="concat">合并</option>
              </select>
              <i class="ri-arrow-down-s-line absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
            </div>
            <i class="ri-question-fill text-slate-400 text-lg cursor-help" title="说明"></i>
          </div>
        </div>

        <!-- 消息监听间隔 -->
        <div class="flex items-center justify-between">
          <label class="text-sm font-medium text-slate-700">消息监听间隔(秒)</label>
          <div class="flex items-center space-x-2">
            <div class="flex items-center border border-slate-300 rounded overflow-hidden">
              <button
                @click="monitorInterval = Math.max(1, monitorInterval - 1)"
                class="px-3 py-1.5 hover:bg-slate-50 border-r border-slate-300 transition-colors text-slate-600"
              >
                <i class="ri-subtract-line"></i>
              </button>
              <input
                type="number"
                v-model.number="monitorInterval"
                @change="monitorInterval = safeParseInt($event.target.value, 1)"
                class="w-12 py-1.5 text-center text-sm focus:outline-none focus:ring-inset focus:ring-2 focus:ring-[#4A90E2]"
              />
              <button
                @click="monitorInterval += 1"
                class="px-3 py-1.5 hover:bg-slate-50 border-l border-slate-300 transition-colors text-slate-600"
              >
                <i class="ri-add-line"></i>
              </button>
            </div>
            <i class="ri-question-fill text-slate-400 text-lg cursor-help" title="说明"></i>
          </div>
        </div>

        <!-- AI智能体上下文 -->
        <div class="flex items-center justify-between">
          <label class="text-sm font-medium text-slate-700">AI智能体上下文</label>
          <div class="flex items-center space-x-3">
            <span class="text-sm font-medium text-slate-700">关闭</span>
            <button
              @click="aiOnTop = !aiOnTop"
              class="relative w-12 h-6 rounded-full transition-colors duration-200 ease-in-out focus:outline-none"
              :class="aiOnTop ? 'bg-[#4A90E2]' : 'bg-slate-200'"
            >
              <span
                class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow transition-transform duration-200 ease-in-out"
                :class="aiOnTop ? 'translate-x-6' : 'translate-x-0'"
              ></span>
            </button>
            <span class="text-sm font-medium text-[#4A90E2]">开启</span>
          </div>
        </div>

        <!-- 携带上下文条数 -->
        <div class="flex items-center justify-between" v-if="aiOnTop">
          <label class="text-sm font-medium text-slate-700">携带上下文条数</label>
          <div class="flex items-center space-x-2">
            <div class="flex items-center border border-slate-300 rounded overflow-hidden">
              <button
                @click="contextHistoryCount = Math.max(1, contextHistoryCount - 1)"
                class="px-3 py-1.5 hover:bg-slate-50 border-r border-slate-300 transition-colors text-slate-600"
              >
                <i class="ri-subtract-line"></i>
              </button>
              <input
                type="number"
                v-model.number="contextHistoryCount"
                @change="contextHistoryCount = safeParseInt($event.target.value, 1)"
                class="w-12 py-1.5 text-center text-sm focus:outline-none focus:ring-inset focus:ring-2 focus:ring-[#4A90E2]"
              />
              <button
                @click="contextHistoryCount += 1"
                class="px-3 py-1.5 hover:bg-slate-50 border-l border-slate-300 transition-colors text-slate-600"
              >
                <i class="ri-add-line"></i>
              </button>
            </div>
            <i class="ri-question-fill text-slate-400 text-lg cursor-help" title="说明"></i>
          </div>
        </div>
      </div>

      <!-- 转人工配置 -->
      <div class="pt-2">
        <h3 class="text-sm font-medium text-slate-500 mb-4">转人工配置</h3>
        
        <!-- 话术词 -->
        <div class="bg-[#F8FAFC] rounded-lg p-4 mb-4">
          <div class="flex items-center justify-between mb-2">
            <div class="flex flex-col">
              <span class="text-base font-bold text-slate-800">话术词</span>
              <span class="text-xs text-slate-400 mt-1">当AI回复中命中话术词时，将触发转人工通知</span>
            </div>
            <button
              v-if="!showAddKeywordInput"
              @click="showAddKeywordInput = true"
              class="px-3 py-1.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded text-xs font-medium transition-colors"
            >
              +添加
            </button>
          </div>

          <!-- 关键词列表 -->
          <div class="flex flex-wrap gap-2 mt-3">
            <span
              v-for="(keyword, index) in transferKeywords"
              :key="index"
              class="inline-flex items-center px-2 py-1 bg-[#E6F0FF] text-[#4A90E2] border border-[#B3D1FF] rounded text-sm"
            >
              {{ keyword }}
              <i
                @click="removeKeyword(index)"
                class="ri-close-line ml-1.5 cursor-pointer hover:text-[#357ABD]"
              ></i>
            </span>
            
            <!-- 输入框 -->
            <div v-if="showAddKeywordInput" class="inline-flex items-center">
              <input
                v-model="newKeyword"
                @keyup.enter="addKeyword"
                @blur="addKeyword"
                ref="keywordInput"
                type="text"
                class="w-24 px-2 py-1 text-sm border border-[#4A90E2] rounded focus:outline-none focus:ring-1 focus:ring-[#4A90E2]"
                placeholder="输入..."
                autoFocus
              />
            </div>
          </div>
        </div>

        <!-- 接收通知的微信昵称 -->
        <div class="bg-[#F8FAFC] rounded-lg p-4">
          <div class="flex flex-col mb-3">
            <span class="text-base font-bold text-slate-800">接收通知的微信昵称</span>
            <span class="text-xs text-slate-400 mt-1">转人工通知将发送给此微信</span>
          </div>
          <input
            type="text"
            v-model="transferWechatNickname"
            placeholder="请输入微信昵称"
            class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
          />
        </div>
      </div>
    </div>
  </div>
</template>
