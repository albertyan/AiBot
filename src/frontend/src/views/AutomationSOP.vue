<script setup>
import { ref } from 'vue';
import NavBar from '../components/NavBar.vue';
import ActivePush from '../components/automation/ActivePush.vue';
import AutoPassFriend from '../components/automation/AutoPassFriend.vue';
import AddFriendConfig from '../components/automation/AddFriendConfig.vue';
import MomentsOperation from '../components/automation/MomentsOperation.vue';
import AutoFollowUp from '../components/automation/AutoFollowUp.vue';

const activeFeature = ref('moments');

const operations = [
  { id: 'moments', icon: 'ri-loader-2-line', name: '朋友圈运营', color: 'bg-blue-500' },
  { id: 'push', icon: 'ri-send-plane-line', name: '主动推送', color: 'bg-teal-500' },
  { id: 'add', icon: 'ri-user-add-line', name: '自动通过好友', color: 'bg-blue-500' },
  { id: 'follow', icon: 'ri-user-follow-line', name: '添加好友配置', color: 'bg-blue-500' },
  { id: 'follow_up', icon: 'ri-bar-chart-line', name: '自动跟单', color: 'bg-blue-500' },
];
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <NavBar />

    <!-- 主要内容区域 -->
    <div class="flex h-[calc(100vh-64px)]">
      <!-- 左侧功能菜单 -->
      <div class="w-24 bg-white border-r border-slate-200 flex flex-col items-center py-6">
        <div class="text-sm font-medium text-slate-700 mb-6">功能</div>
        <div class="flex-1 w-full space-y-4">
          <button
            v-for="op in operations"
            :key="op.id"
            @click="activeFeature = op.id"
            class="w-full flex flex-col items-center justify-center py-4 hover:bg-slate-50 transition-colors"
            :class="{ 'bg-blue-50 border-l-4 border-blue-500': activeFeature === op.id }"
          >
            <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-2" :class="op.color">
              <i :class="[op.icon, 'text-white text-xl']"></i>
            </div>
            <span v-if="op.name" class="text-xs text-slate-600">{{ op.name }}</span>
          </button>
        </div>
      </div>

      <!-- 主内容区 -->
      <ActivePush v-if="activeFeature === 'push'" />
      <AutoPassFriend v-else-if="activeFeature === 'add'" />
      <AddFriendConfig v-else-if="activeFeature === 'follow'" />
      <AutoFollowUp v-else-if="activeFeature === 'follow_up'" />
      <MomentsOperation v-else />
    </div>
  </div>
</template>
