<script setup>
import { ref } from 'vue';
import NavBar from '../components/NavBar.vue';
import AiAccessSetting from '../components/config/AiAccessSetting.vue';
import AgentManagement from '../components/config/AgentManagement.vue';
import MomentsReview from '../components/config/MomentsReview.vue';
import ScriptGroupConfig from '../components/config/ScriptGroupConfig.vue';
import AiReplyConfig from '../components/config/AiReplyConfig.vue';
import ExternalApiConfig from '../components/config/ExternalApiConfig.vue';
import AlertConfig from '../components/config/AlertConfig.vue';
import RestTimeSetting from '../components/config/RestTimeSetting.vue';

const activeSection = ref('ai-access');

const menuItems = [
  { id: 'ai-access', icon: 'ri-robot-line', label: 'AI接入设置' },
  { id: 'agent-management', icon: 'ri-brain-line', label: '智能体管理' },
  { id: 'moments-review', icon: 'ri-chat-smile-3-line', label: '朋友圈评论' },
  { id: 'tag-group', icon: 'ri-price-tag-3-line', label: '话术组配置' },
  { id: 'ai-reply', icon: 'ri-message-3-line', label: 'AI回复配置' },
  { id: 'external-api', icon: 'ri-link', label: '外部API配置' },
  { id: 'forecast', icon: 'ri-line-chart-line', label: '预警配置' },
  { id: 'rest-time', icon: 'ri-time-line', label: '休息时间设置' },
];

/**
 * 为什么采用与自动化SOP一致的左侧菜单样式：
 * - 使用左侧 4px 强调色条（#4A90E2）来表达“当前选中”状态，贴合用户视觉习惯
 * - 选中项采用浅蓝背景（bg-blue-50）+ 蓝色边条（border-blue-500），完全对齐自动化SOP按钮视觉语言
 * - 保持原有高度（py-3）不变，避免布局跳动与肌肉记忆破坏
 * - 通过函数统一生成类名，确保未来扩展时风格一致
 */
const getMenuItemClass = (id) => {
  const base = 'w-full flex items-center space-x-3 px-4 py-3 text-sm transition-colors border-l-4 border-transparent';
  const active = 'bg-blue-300 text-slate-800 border-blue-500 font-medium';
  const inactive = 'text-slate-700 hover:bg-slate-50';
  return `${base} ${activeSection.value === id ? active : inactive}`;
};
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <!-- 顶部导航 -->
    <NavBar />

    <!-- 主要内容区域 -->
    <div class="flex h-[calc(100vh-64px)]">
      <!-- 左侧导航菜单 -->
      <div class="w-56 bg-white border-r border-slate-200 overflow-y-auto">
        <div class="p-4">
          <h2 class="text-base font-semibold text-slate-700 mb-4">配置导航</h2>
          <div class="space-y-1">
            <button
              v-for="item in menuItems"
              :key="item.id"
              @click="activeSection = item.id"
              :class="getMenuItemClass(item.id)"
            >
              <i :class="`${item.icon} text-base`"></i>
              <span>{{ item.label }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧配置区域 -->
      <div class="flex-1 overflow-y-auto bg-[#F5F7FA]">
        <div class="max-w-5xl mx-auto p-8">
          <!-- AI接入设置 -->
          <AiAccessSetting v-if="activeSection === 'ai-access'" />

          <!-- 智能体管理 -->
          <AgentManagement v-else-if="activeSection === 'agent-management'" />

          <!-- 朋友圈评论设置 -->
          <MomentsReview v-else-if="activeSection === 'moments-review'" />

          <!-- 话术组配置 -->
          <ScriptGroupConfig v-else-if="activeSection === 'tag-group'" />

          <!-- AI回复配置 -->
          <AiReplyConfig v-else-if="activeSection === 'ai-reply'" />

          <!-- 外部API配置 -->
          <ExternalApiConfig v-else-if="activeSection === 'external-api'" />

          <!-- 预警配置 -->
          <AlertConfig v-else-if="activeSection === 'forecast'" />

          <!-- 休息时间设置 -->
          <RestTimeSetting v-else-if="activeSection === 'rest-time'" />
        </div>
      </div>
    </div>
  </div>
</template>
