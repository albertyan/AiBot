<script setup>
import { ref, onMounted } from 'vue';
import { Select } from 'ant-design-vue';
import { getGroups } from '../../api/custom';

const dailyLimit = ref(100);
const checkInterval = ref(10);
const maxFriendsPerPass = ref(5);
const selectedGreetingScript = ref('');
const selectedAutoGroup = ref(undefined);
const friendTag = ref('');
const autoPassEnabled = ref(false);
const groups = ref([]);

const fetchGroups = async () => {
  try {
    const res = await getGroups();
    if (res.code === 200) {
      // console.log('Groups data:', res.data);
      groups.value = res.data.map(group => ({
        label: group.name,
        value: group.name
      }));
    }
  } catch (error) {
    console.error('Failed to fetch groups:', error);
  }
};

onMounted(() => {
  fetchGroups();
});

const safeParseInt = (value, fallback) => {
  const parsed = parseInt(value);
  return isNaN(parsed) ? fallback : Math.max(1, parsed);
};

const handleStartAutoPassTask = () => {
  if (dailyLimit.value < 1 || checkInterval.value < 1 || maxFriendsPerPass.value < 1) {
    alert('请确保所有数值均大于 0');
    return;
  }
  autoPassEnabled.value = true;
  console.log('Auto pass task started with config:', {
    dailyLimit: dailyLimit.value,
    checkInterval: checkInterval.value,
    maxFriendsPerPass: maxFriendsPerPass.value,
    selectedGreetingScript: selectedGreetingScript.value,
    selectedAutoGroup: selectedAutoGroup.value,
    friendTag: friendTag.value,
  });
};
</script>

<template>
  <div class="flex-1 flex">
    <!-- 自动通过好友配置区域 -->
    <div class="w-[45%] bg-white border-r border-slate-200 overflow-y-auto">
      <div class="p-6">
        <h2 class="text-lg font-semibold text-slate-800 mb-6">自动通过好友配置</h2>

        <!-- 提示信息 -->
        <div class="flex items-start space-x-3 bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <i class="ri-information-fill text-blue-500 text-xl mt-0.5"></i>
          <div class="text-sm text-blue-700">
            00:00-05:30为休息时间，暂停执行任务，可前往配置页修改
          </div>
        </div>

        <div class="space-y-6">
          <!-- 每日通过上限 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">每日通过上限</label>
            <div class="flex items-center space-x-3">
              <button
                @click="dailyLimit = Math.max(1, dailyLimit - 10)"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-subtract-line text-slate-600"></i>
              </button>
              <input
                type="number"
                v-model="dailyLimit"
                @input="dailyLimit = safeParseInt($event.target.value, 1)"
                class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
              />
              <button
                @click="dailyLimit += 10"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-add-line text-slate-600"></i>
              </button>
            </div>
          </div>

          <!-- 检查间隔(分钟) -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">检查间隔(分钟)</label>
            <div class="flex items-center space-x-3">
              <button
                @click="checkInterval = Math.max(1, checkInterval - 5)"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-subtract-line text-slate-600"></i>
              </button>
              <input
                type="number"
                v-model="checkInterval"
                @input="checkInterval = safeParseInt($event.target.value, 1)"
                class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
              />
              <button
                @click="checkInterval += 5"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-add-line text-slate-600"></i>
              </button>
            </div>
          </div>

          <!-- 通过好友单次最大处理 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">通过好友单次最大处理</label>
            <div class="flex items-center space-x-3">
              <button
                @click="maxFriendsPerPass = Math.max(1, maxFriendsPerPass - 1)"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-subtract-line text-slate-600"></i>
              </button>
              <input
                type="number"
                v-model="maxFriendsPerPass"
                @input="maxFriendsPerPass = safeParseInt($event.target.value, 1)"
                class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
              />
              <button
                @click="maxFriendsPerPass += 1"
                class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
              >
                <i class="ri-add-line text-slate-600"></i>
              </button>
            </div>
          </div>

          <!-- 打招呼话术 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">打招呼话术</label>
            <div class="relative">
              <select
                v-model="selectedGreetingScript"
                class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
              >
                <option value="">选择打招呼话术组</option>
                <option value="话术1">话术组1</option>
                <option value="话术2">话术组2</option>
              </select>
              <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
            </div>
          </div>

          <!-- 自动拉群 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">自动拉群</label>
            <div class="relative">
              <Select
                v-model:value="selectedAutoGroup"
                show-search
                placeholder="选择目标群聊"
                :options="groups"
                :filter-option="(input, option) => option.label.toLowerCase().indexOf(input.toLowerCase()) >= 0"
                class="w-full"
                style="height: 42px;"
              />
            </div>
          </div>

          <!-- 好友标签 -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">好友标签</label>
            <input
              type="text"
              v-model="friendTag"
              placeholder="请输入标签"
              class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
          </div>

          <!-- 启动任务按钮 -->
          <div class="pt-4">
            <button
              class="w-full px-6 py-3 bg-gradient-to-r from-[#4A90E2] to-[#357ABD] hover:shadow-lg text-white rounded-lg font-medium transition-all flex items-center justify-center space-x-2"
              @click="handleStartAutoPassTask"
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
</template>
