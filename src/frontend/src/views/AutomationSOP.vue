<script setup>
import { ref } from 'vue';
import NavBar from '../components/NavBar.vue';

const activeFeature = ref('moments');
const activeTab = ref('tasks');
const showTaskModal = ref(false);
const sendTime = ref('immediate');
const selectedTags = ref([]);
const selectedInterval = ref('10-30');

// 朋友圈运营配置状态
const totalPosts = ref(10);
const postsPerGroup = ref(3);
const intervalMinutes = ref(30);
const stopCondition = ref('终止本次任务');
const interactionMode = ref('点赞&评论');
const intelligentBody = ref('过敏');
const multiWechatLoop = ref(false);

// 自动通过好友配置状态
const dailyLimit = ref(100);
const checkInterval = ref(10);
const maxFriendsPerPass = ref(5);
const selectedGreetingScript = ref('');
const selectedAutoGroup = ref('');
const friendTag = ref('');
const autoPassEnabled = ref(false);

// 添加好友配置状态
const addDailyLimit = ref(10);
const addCheckInterval = ref(30);
const maxAddPerTime = ref(1);
const verificationMessage = ref('');
const multiWechatLoopAdd = ref(false);

const tags = ['未分组', '箭冠', '楼市通', '云南箭冠', '中软', '博美', '车领主', '邻居'];

const toggleTag = (tag) => {
  if (selectedTags.value.includes(tag)) {
    selectedTags.value = selectedTags.value.filter((t) => t !== tag);
  } else {
    selectedTags.value.push(tag);
  }
};

const operations = [
  { id: 'moments', icon: 'ri-loader-2-line', name: '朋友圈运营', color: 'bg-blue-500' },
  { id: 'push', icon: 'ri-send-plane-line', name: '主动推送', color: 'bg-teal-500' },
  { id: 'add', icon: 'ri-user-add-line', name: '自动通过好友', color: 'bg-blue-500' },
  { id: 'follow', icon: 'ri-user-follow-line', name: '添加好友配置', color: 'bg-blue-500' },
  { id: 'stats', icon: 'ri-bar-chart-line', name: '', color: 'bg-slate-600' },
];

// ---------- Helper Functions ----------
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

const handleStartAddFriendTask = () => {
  if (addDailyLimit.value < 1 || addCheckInterval.value < 1 || maxAddPerTime.value < 1) {
    alert('请确保所有数值均大于 0');
    return;
  }
  console.log('Add friend task started with config:', {
    addDailyLimit: addDailyLimit.value,
    addCheckInterval: addCheckInterval.value,
    maxAddPerTime: maxAddPerTime.value,
    verificationMessage: verificationMessage.value,
    multiWechatLoopAdd: multiWechatLoopAdd.value,
  });
};

const handleStartMomentsTask = () => {
  if (totalPosts.value < 1 || postsPerGroup.value < 1 || intervalMinutes.value < 1) {
    alert('请确保所有数值均大于 0');
    return;
  }
  console.log('Task started with config:', {
    totalPosts: totalPosts.value,
    postsPerGroup: postsPerGroup.value,
    intervalMinutes: intervalMinutes.value,
    stopCondition: stopCondition.value,
    interactionMode: interactionMode.value,
    selectedTags: selectedTags.value,
    intelligentBody: intelligentBody.value,
    multiWechatLoop: multiWechatLoop.value,
  });
};

const handleCreateTask = () => {
  setShowTaskModal.value = false;
  // 这里可以添加创建任务的逻辑
};
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
      <div class="flex-1 flex">
        <!-- 主动推送 -->
        <template v-if="activeFeature === 'push'">
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
        </template>

        <!-- 自动通过好友 -->
        <template v-else-if="activeFeature === 'add'">
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
                    <select
                      v-model="selectedAutoGroup"
                      class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
                    >
                      <option value="">选择目标群聊</option>
                      <option value="群聊1">群聊1</option>
                      <option value="群聊2">群聊2</option>
                    </select>
                    <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
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
        </template>

        <!-- 添加好友配置 -->
        <template v-else-if="activeFeature === 'follow'">
          <!-- 添加好友配置区域 -->
          <div class="w-[45%] bg-white border-r border-slate-200 overflow-y-auto">
            <div class="p-6">
              <h2 class="text-lg font-semibold text-slate-800 mb-6">添加好友配置</h2>

              <!-- 顶部标签切换 -->
              <div class="flex items-center space-x-2 mb-6">
                <button class="px-4 py-2 bg-[#4A90E2] text-white rounded-lg text-sm font-medium">
                  导入名单
                </button>
                <button class="px-4 py-2 bg-slate-100 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-200 transition-colors">
                  记录
                </button>
                <button class="px-4 py-2 bg-slate-100 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-200 transition-colors">
                  操作日志
                </button>
              </div>

              <!-- 名单剩余可添加 -->
              <div class="flex items-center space-x-2 mb-6">
                <i class="ri-refresh-line text-slate-600"></i>
                <span class="text-sm text-slate-700">名单剩余可添加</span>
                <span class="text-lg font-bold text-slate-800">0</span>
                <span class="text-sm text-slate-700">人</span>
              </div>

              <!-- 提示信息 -->
              <div class="flex items-start space-x-3 bg-slate-100 border border-slate-200 rounded-lg p-4 mb-6">
                <i class="ri-information-fill text-slate-500 text-xl mt-0.5"></i>
                <div class="text-sm text-slate-600">
                  00:00-05:30为休息时间，暂停执行任务，可前往配置页修改
                </div>
              </div>

              <div class="space-y-6">
                <!-- 每日添加上限 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">每日添加上限</label>
                  <div class="flex items-center space-x-3">
                    <button
                      @click="addDailyLimit = Math.max(1, addDailyLimit - 1)"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
                    >
                      <i class="ri-subtract-line text-slate-600"></i>
                    </button>
                    <input
                      type="number"
                      v-model="addDailyLimit"
                      @input="addDailyLimit = safeParseInt($event.target.value, 1)"
                      class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                    <button
                      @click="addDailyLimit += 1"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
                    >
                      <i class="ri-add-line text-slate-600"></i>
                    </button>
                  </div>
                </div>

                <!-- 添加间隔(分钟) -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">添加间隔(分钟)</label>
                  <div class="flex items-center space-x-3">
                    <button
                      @click="addCheckInterval = Math.max(1, addCheckInterval - 5)"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
                    >
                      <i class="ri-subtract-line text-slate-600"></i>
                    </button>
                    <input
                      type="number"
                      v-model="addCheckInterval"
                      @input="addCheckInterval = safeParseInt($event.target.value, 1)"
                      class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                    <button
                      @click="addCheckInterval += 5"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
                    >
                      <i class="ri-add-line text-slate-600"></i>
                    </button>
                  </div>
                </div>

                <!-- 添加好友单次添加人数 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">添加好友<br />单次添加人数</label>
                  <div class="flex items-center space-x-3">
                    <button
                      @click="maxAddPerTime = Math.max(1, maxAddPerTime - 1)"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
                    >
                      <i class="ri-subtract-line text-slate-600"></i>
                    </button>
                    <input
                      type="number"
                      v-model="maxAddPerTime"
                      @input="maxAddPerTime = safeParseInt($event.target.value, 1)"
                      class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                    <button
                      @click="maxAddPerTime += 1"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
                    >
                      <i class="ri-add-line text-slate-600"></i>
                    </button>
                  </div>
                </div>

                <!-- 验证消息 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">验证消息</label>
                  <textarea
                    v-model="verificationMessage"
                    placeholder="请输入添加好友时的验证消息"
                    rows="4"
                    class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
                  ></textarea>
                </div>

                <!-- 多微信循环 -->
                <div>
                  <label class="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      v-model="multiWechatLoopAdd"
                      class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                    />
                    <span class="text-sm text-slate-700">多微信循环</span>
                  </label>
                </div>

                <!-- 启动任务按钮 -->
                <div class="pt-4">
                  <button
                    class="w-full px-6 py-3 bg-gradient-to-r from-[#4A90E2] to-[#357ABD] hover:shadow-lg text-white rounded-lg font-medium transition-all flex items-center justify-center space-x-2"
                    @click="handleStartAddFriendTask"
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
        </template>

        <!-- 默认/其他功能 (自动评论朋友圈配置) -->
        <template v-else>
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
                    class="w-full px-4 py-2.5 bg-[#5B6EE1] hover:bg-[#4A5DD0] text-white rounded-lg text-sm font-medium transition-colors"
                    @click="console.log('Open tag selector')"
                  >
                    选择标签
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
        </template>
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
                <label v-for="tag in tags" :key="tag" class="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    :checked="selectedTags.includes(tag)"
                    @change="toggleTag(tag)"
                    class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                  />
                  <span class="text-sm text-slate-700">{{ tag }}</span>
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
  </div>
</template>
