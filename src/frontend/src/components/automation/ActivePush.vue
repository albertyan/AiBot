<script setup>
import { ref, onMounted } from 'vue';
import { getFriendTags } from '../../api/custom';

const activeTab = ref('tasks');
const showTaskModal = ref(false);
const sendTime = ref('immediate');
const selectedTags = ref([]);
const selectedInterval = ref('10-30');
const tags = ref([]);

const fetchTags = async () => {
  try {
    const res = await getFriendTags();
    if (res.code === 200) {
      tags.value = res.data;
    }
  } catch (error) {
    console.error('获取标签失败:', error);
  }
};

onMounted(() => {
  fetchTags();
});

const toggleTag = (tag) => {
  if (selectedTags.value.includes(tag)) {
    selectedTags.value = selectedTags.value.filter((t) => t !== tag);
  } else {
    selectedTags.value.push(tag);
  }
};

const handleCreateTask = () => {
  showTaskModal.value = false;
  // 这里可以添加创建任务的逻辑
};
</script>

<template>
  <div class="flex-1 flex">
    <!-- 左侧任务列表区域 -->
    <div class="w-80 bg-white border-r border-slate-200 flex flex-col">
      <!-- 标签切换 -->
      <div class="flex border-b border-slate-200">
        <button
          @click="activeTab = 'tasks'"
          class="flex-1 py-3 text-sm font-medium transition-colors"
          :class="activeTab === 'tasks' ? 'text-[#4A90E2] border-b-2 border-[#4A90E2]' : 'text-slate-600 hover:text-slate-800'"
        >
          主动推送群发任务
        </button>
        <button
          @click="activeTab = 'logs'"
          class="flex-1 py-3 text-sm font-medium transition-colors"
          :class="activeTab === 'logs' ? 'text-[#4A90E2] border-b-2 border-[#4A90E2]' : 'text-slate-600 hover:text-slate-800'"
        >
          操作日志
        </button>
      </div>

      <!-- 新建任务按钮 -->
      <div class="p-4 border-b border-slate-200">
        <button
          @click="showTaskModal = true"
          class="w-full py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors"
        >
          新建任务
        </button>
      </div>

      <!-- 任务列表 -->
      <div class="flex-1 overflow-y-auto p-4">
        <div class="text-center py-16">
          <i class="ri-inbox-line text-6xl text-slate-300 mb-3"></i>
          <div class="text-sm text-slate-400">暂无任务</div>
        </div>
      </div>
    </div>

    <!-- 右侧操作日志区域 -->
    <div class="flex-1 bg-[#F5F7FA] p-6">
      <div class="bg-white rounded-lg shadow-sm h-full p-6">
        <h2 class="text-lg font-semibold text-slate-800 mb-4">操作日志</h2>
        <div class="text-center py-16">
          <i class="ri-file-list-line text-6xl text-slate-300 mb-3"></i>
          <div class="text-sm text-slate-400">暂无操作日志</div>
        </div>
      </div>
    </div>

    <!-- 新建推送任务弹窗 -->
    <div v-if="showTaskModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-3xl mx-4 max-h-[90vh] overflow-y-auto">
        <!-- 弹窗头部 -->
        <div class="flex items-center justify-between p-6 border-b border-slate-200">
          <h2 class="text-xl font-semibold text-slate-800">新建推送任务</h2>
          <button
            @click="showTaskModal = false"
            class="w-8 h-8 flex items-center justify-center hover:bg-slate-100 rounded-lg transition-colors"
          >
            <i class="ri-close-line text-xl text-slate-600"></i>
          </button>
        </div>

        <!-- 弹窗内容 -->
        <div class="p-6 space-y-6">
          <!-- 警告提示 -->
          <div class="flex items-start space-x-3 bg-orange-50 border border-orange-200 rounded-lg p-4">
            <i class="ri-error-warning-fill text-orange-500 text-xl mt-0.5"></i>
            <div class="text-sm text-orange-700">
              建议单次群发不超过40个目标，如果人数较多可分批次推送。
            </div>
          </div>

          <!-- 发送时间 -->
          <div>
            <div class="flex items-center space-x-2 mb-3">
              <i class="ri-time-line text-[#4A90E2]"></i>
              <label class="text-sm font-medium text-slate-700">发送时间:</label>
            </div>
            <div class="flex items-center space-x-6">
              <label class="flex items-center space-x-2 cursor-pointer">
                <input
                  type="radio"
                  name="sendTime"
                  value="immediate"
                  v-model="sendTime"
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]"
                />
                <span class="text-sm text-slate-700">立即发送</span>
              </label>
              <label class="flex items-center space-x-2 cursor-pointer">
                <input
                  type="radio"
                  name="sendTime"
                  value="scheduled"
                  v-model="sendTime"
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]"
                />
                <span class="text-sm text-slate-700">定时发送</span>
              </label>
            </div>
          </div>

          <!-- 好友标签 -->
          <div>
            <div class="flex items-center space-x-2 mb-3">
              <i class="ri-home-smile-line text-[#4A90E2]"></i>
              <label class="text-sm font-medium text-slate-700">好友标签:</label>
            </div>
            <div class="grid grid-cols-4 gap-3">
              <label v-for="tagItem in tags" :key="tagItem.tag" class="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  :checked="selectedTags.includes(tagItem.tag)"
                  @change="toggleTag(tagItem.tag)"
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                />
                <span class="text-sm text-slate-700">{{ tagItem.tag }}</span>
              </label>
            </div>
          </div>

          <!-- 激活话术 -->
          <div>
            <div class="flex items-center space-x-2 mb-3">
              <i class="ri-chat-smile-3-line text-[#4A90E2]"></i>
              <label class="text-sm font-medium text-slate-700">激活话术:</label>
            </div>
            <div class="flex items-center space-x-6 mb-3">
              <label class="flex items-center space-x-2 cursor-pointer">
                <input
                  type="radio"
                  name="scriptType"
                  checked
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]"
                />
                <span class="text-sm text-slate-700">话术组</span>
              </label>
            </div>
            <select class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent">
              <option>选择话术组</option>
            </select>
          </div>

          <!-- 发送间隔 -->
          <div>
            <div class="flex items-center space-x-2 mb-3">
              <i class="ri-time-line text-[#4A90E2]"></i>
              <label class="text-sm font-medium text-slate-700">发送间隔:</label>
            </div>
            <div class="flex items-center space-x-6">
              <label
                v-for="interval in [
                  { value: '3-8', label: '3-8秒' },
                  { value: '10-30', label: '10-30秒' },
                  { value: '30-60', label: '30-60秒' },
                ]"
                :key="interval.value"
                class="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="radio"
                  name="interval"
                  :value="interval.value"
                  v-model="selectedInterval"
                  class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]"
                />
                <span class="text-sm text-slate-700">{{ interval.label }}</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 弹窗底部按钮 -->
        <div class="flex items-center justify-end space-x-3 p-6 border-t border-slate-200">
          <button
            @click="showTaskModal = false"
            class="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 rounded-lg font-medium hover:bg-slate-50 transition-colors"
          >
            取消
          </button>
          <button
            @click="handleCreateTask"
            class="px-6 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg font-medium transition-colors"
          >
            创建任务
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
