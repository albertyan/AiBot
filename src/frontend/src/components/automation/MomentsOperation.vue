<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { getAgents } from '../../api/setting';
import TagSelectModal from '../TagSelectModal.vue';

// 朋友圈运营配置状态
const showTagModal = ref(false);
const selectedTags = ref([]);
const totalPosts = ref(10);
const postsPerGroup = ref(3);
const intervalMinutes = ref(30);
const stopCondition = ref('stop_task');
const interactionMode = ref('like_and_comment');
const intelligentBody = ref('');
const multiWechatLoop = ref(false);
const agents = ref([]);

const safeParseInt = (value, fallback) => {
  const parsed = parseInt(value);
  return isNaN(parsed) ? fallback : Math.max(1, parsed);
};

onMounted(async () => {
  try {
    const res = await getAgents();
    if (res.code === 200 && res.data && res.data.agents) {
      agents.value = res.data.agents;
      if (agents.value.length > 0) {
        intelligentBody.value = agents.value[0].id;
      }
    }
  } catch (error) {
    console.error('获取智能体列表失败:', error);
    message.error('获取智能体列表失败');
  }
});

const handleStartMomentsTask = () => {
  if (totalPosts.value < 1 || postsPerGroup.value < 1 || intervalMinutes.value < 1) {
    message.warning('请确保所有数值均大于 0');
    return;
  }
  console.log('Task started with config:', {
    totalPosts: totalPosts.value,
    postsPerGroup: postsPerGroup.value,
    intervalMinutes: intervalMinutes.value,
    stopCondition: stopCondition.value,
    interactionMode: interactionMode.value,
    intelligentBody: intelligentBody.value,
    multiWechatLoop: multiWechatLoop.value,
    selectedTags: selectedTags.value,
  });
};

const handleTagConfirm = (tags) => {
  selectedTags.value = tags;
};
</script>

<template>
  <div class="flex-1 flex">
    <!-- 配置区域 -->
    <div class="w-[45%] bg-white border-r border-slate-200 overflow-y-auto">
      <div class="p-6">
        <h2 class="text-lg font-semibold text-slate-800 mb-6">自动评论朋友圈配置</h2>

        <div class="space-y-6">
          <!-- 总评论上限 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">总评论上限</label>
            <div class="flex items-center space-x-3">
              <button
                @click="totalPosts = Math.max(1, totalPosts - 1)"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-subtract-line text-slate-600"></i>
              </button>
              <input
                type="number"
                v-model="totalPosts"
                @input="totalPosts = safeParseInt($event.target.value, 1)"
                class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
              />
              <button
                @click="totalPosts += 1"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-add-line text-slate-600"></i>
              </button>
            </div>
          </div>

          <!-- 单好友次数 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">单好友次数</label>
            <div class="flex items-center space-x-3">
              <button
                @click="postsPerGroup = Math.max(1, postsPerGroup - 1)"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-subtract-line text-slate-600"></i>
              </button>
              <input
                type="number"
                v-model="postsPerGroup"
                @input="postsPerGroup = safeParseInt($event.target.value, 1)"
                class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
              />
              <button
                @click="postsPerGroup += 1"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-add-line text-slate-600"></i>
              </button>
            </div>
          </div>

          <!-- 循环间隔 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">循环间隔(分钟)</label>
            <div class="flex items-center space-x-3">
              <button
                @click="intervalMinutes = Math.max(1, intervalMinutes - 10)"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-subtract-line text-slate-600"></i>
              </button>
              <input
                type="number"
                v-model="intervalMinutes"
                @input="intervalMinutes = safeParseInt($event.target.value, 1)"
                class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
              />
              <button
                @click="intervalMinutes += 10"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-add-line text-slate-600"></i>
              </button>
            </div>
          </div>

          <!-- 到达上次位置 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">到达上次位置</label>
            <div class="relative">
              <select
                v-model="stopCondition"
                class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
              >
                <option value="stop_task">终止本次任务</option>
                <option value="skip_continue">跳过并继续</option>
              </select>
              <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
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
                <option value="like_and_comment">点赞&评论</option>
                <option value="like_only">仅点赞</option>
                <option value="comment_only">仅评论</option>
              </select>
              <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
            </div>
          </div>

          <!-- 标签 -->
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-slate-700">标签(非必须)</label>
            <div class="flex flex-col items-end space-y-2">
              <button
                class="px-6 py-2 bg-gradient-to-r from-[#5B6EE1] to-[#8B5CF6] hover:from-[#4A5DD0] hover:to-[#7C3AED] text-white rounded-lg text-sm font-medium transition-all shadow-sm"
                @click="showTagModal = true"
              >
                选择标签
              </button>
              <div v-if="selectedTags.length > 0" class="px-4 py-1.5 bg-purple-50 border border-purple-100 rounded-lg text-sm text-purple-700">
                已选: {{ selectedTags.join(', ') }}
              </div>
            </div>
          </div>

          <!-- 选择智能体 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">选择智能体</label>
            <div class="relative">
              <select
                v-model="intelligentBody"
                class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
              >
                <option value="" disabled>请选择智能体</option>
                <option v-for="agent in agents" :key="agent.id" :value="agent.id">{{ agent.name }}</option>
              </select>
              <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
            </div>
          </div>

          <!-- 多微信循环 -->
          <div>
            <label class="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                v-model="multiWechatLoop"
                class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
              />
              <span class="text-sm text-slate-700">多微信循环</span>
            </label>
          </div>

          <!-- 启动任务按钮 -->
          <div class="pt-4">
            <button
              class="w-full px-6 py-3 bg-gradient-to-r from-[#4A90E2] to-[#357ABD] hover:shadow-lg text-white rounded-lg font-medium transition-all flex items-center justify-center space-x-2"
              @click="handleStartMomentsTask"
            >
              <i class="ri-play-circle-line text-lg"></i>
              <span>启动任务</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作日志区域 -->
    <div class="flex-1 bg-[#F5F7FA] overflow-y-auto">
      <div class="p-6">
        <h2 class="text-lg font-semibold text-slate-800 mb-6">操作日志</h2>

        <!-- 空状态 -->
        <div class="flex flex-col items-center justify-center py-24">
          <div class="w-32 h-32 bg-white rounded-full flex items-center justify-center mb-6 shadow-sm">
            <i class="ri-inbox-line text-6xl text-slate-300"></i>
          </div>
          <div class="text-base text-slate-500 mb-2">最近没有新的操作记录</div>
          <div class="text-sm text-slate-400">启动任务后，操作记录将显示在这里</div>
        </div>
      </div>
    </div>
  </div>

  <TagSelectModal
    v-model:open="showTagModal"
    :initial-selected-tags="selectedTags"
    @confirm="handleTagConfirm"
  />
</template>
