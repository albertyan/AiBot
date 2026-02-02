<script setup>
import { ref } from 'vue';

const commentLimit = ref(10);
const commentPerFriend = ref(2);
const interactionMode = ref('点赞&评论');
const selectedAgent = ref('');
const blacklistText = ref('');

const safeParseInt = (value, fallback) => {
  const parsed = parseInt(value);
  return isNaN(parsed) ? fallback : Math.max(1, parsed);
};
</script>

<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-slate-800">朋友圈评论设置</h1>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="space-y-6">
        <!-- 总评论条数限制 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-3">总评论条数限制</label>
          <div class="flex items-center space-x-3">
            <button
              @click="commentLimit = Math.max(1, commentLimit - 1)"
              class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
            >
              <i class="ri-subtract-line text-slate-600"></i>
            </button>
            <input
              type="number"
              v-model.number="commentLimit"
              @change="commentLimit = safeParseInt($event.target.value, 1)"
              class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
            <button
              @click="commentLimit += 1"
              class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
            >
              <i class="ri-add-line text-slate-600"></i>
            </button>
          </div>
        </div>

        <!-- 单好友评论次数 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-3">单好友评论次数</label>
          <div class="flex items-center space-x-3">
            <button
              @click="commentPerFriend = Math.max(1, commentPerFriend - 1)"
              class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
            >
              <i class="ri-subtract-line text-slate-600"></i>
            </button>
            <input
              type="number"
              v-model.number="commentPerFriend"
              @change="commentPerFriend = safeParseInt($event.target.value, 1)"
              class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
            <button
              @click="commentPerFriend += 1"
              class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
            >
              <i class="ri-add-line text-slate-600"></i>
            </button>
          </div>
        </div>

        <!-- 互动模式 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-3">互动模式</label>
          <div class="relative">
            <select
              v-model="interactionMode"
              class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
            >
              <option value="点赞&评论">点赞&评论</option>
              <option value="仅点赞">仅点赞</option>
              <option value="仅评论">仅评论</option>
            </select>
            <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
          </div>
        </div>

        <!-- 选择智能体 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-3">选择智能体</label>
          <div class="relative">
            <select
              v-model="selectedAgent"
              class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
            >
              <option value="">请选择智能体</option>
              <option value="过敏">过敏</option>
            </select>
            <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
          </div>
        </div>

        <!-- 黑名单 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-3">黑名单</label>
          <textarea
            v-model="blacklistText"
            placeholder="黑名单用户默认不评论和点赞，多个黑名单中用逗号，隔开"
            rows="4"
            class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
          ></textarea>
        </div>

        <!-- 保存按钮 -->
        <div class="flex justify-end pt-4">
          <button class="px-6 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg font-medium transition-colors">
            保存设置
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
