<script setup>
import { ref } from 'vue';
import { message } from 'ant-design-vue';
import TagSelectModal from '../TagSelectModal.vue';

// 朋友圈运营配置状态
const showTagModal = ref(false);
const selectedTags = ref([]);
const totalPosts = ref(10);
const postsPerGroup = ref(3);
const intervalMinutes = ref(30);
const stopCondition = ref('终止本次任务');
const interactionMode = ref('点赞&评论');
const intelligentBody = ref('过敏');
const multiWechatLoop = ref(false);

const safeParseInt = (value, fallback) => {
  const parsed = parseInt(value);
  return isNaN(parsed) ? fallback : Math.max(1, parsed);
};

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
                <option value="终止本次任务">终止本次任务</option>
                <option value="继续执行">继续执行</option>
                <option value="暂停等待">暂停等待</option>
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
                <option value="点赞&评论">点赞&评论</option>
                <option value="仅点赞">仅点赞</option>
                <option value="仅评论">仅评论</option>
              </select>
              <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
            </div>
          </div>

          <!-- 标签 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">标签(非必须)</label>
            <button
              class="w-full px-4 py-2.5 bg-[#5B6EE1] hover:bg-[#4A5DD0] text-white rounded-lg text-sm font-medium transition-colors flex items-center justify-center space-x-2"
              @click="showTagModal = true"
            >
              <span>{{ selectedTags.length > 0 ? `已选择 ${selectedTags.length} 个标签` : '选择标签' }}</span>
              <i v-if="selectedTags.length > 0" class="ri-check-line"></i>
            </button>
          </div>

          <!-- 选择智能体 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">选择智能体</label>
            <div class="relative">
              <select
                v-model="intelligentBody"
                class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
              >
                <option value="过敏">过敏</option>
                <option value="智能体1">智能体1</option>
                <option value="智能体2">智能体2</option>
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
