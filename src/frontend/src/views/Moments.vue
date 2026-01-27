<script setup>
import { ref } from 'vue';
import NavBar from '../components/NavBar.vue';

const showTaskForm = ref(false);
const currentStep = ref(1);
const taskName = ref('');
const executionType = ref('fixed');
const executionTime = ref('');
const frequency = ref('weekly');
const selectedDays = ref([1, 2, 3, 4, 5]);
const contentType = ref('text');
const textContent = ref('');
const publishType = ref('order');
const selectedAccount = ref('albertyan');

const tasks = ref([
  { id: '1', name: '1201-元旦发圈推广计划', time: '每周一至五 09:00', status: 'active' },
  { id: '2', name: '产品促销活动', time: '每天 14:00', status: 'paused' },
  { id: '3', name: '节日祝福', time: '每周日 10:00', status: 'active' },
]);

const toggleDay = (day) => {
  if (selectedDays.value.includes(day)) {
    selectedDays.value = selectedDays.value.filter((d) => d !== day);
  } else {
    selectedDays.value = [...selectedDays.value, day];
  }
};

const handleNextStep = () => {
  if (currentStep.value === 1) {
    currentStep.value = 2;
  } else {
    // 提交任务
    showTaskForm.value = false;
    currentStep.value = 1;
    taskName.value = '';
    executionTime.value = '';
    textContent.value = '';
  }
};

const handleCancel = () => {
  showTaskForm.value = false;
  currentStep.value = 1;
  taskName.value = '';
  executionTime.value = '';
  textContent.value = '';
};
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <!-- 顶部导航 -->
    <NavBar />

    <!-- 主要内容区域 -->
    <div class="flex h-[calc(100vh-64px)]">
      <!-- 左侧任务列表 -->
      <div class="w-20 bg-white border-r border-slate-200 flex flex-col items-center py-6">
        <div class="flex-1 w-full overflow-y-auto">
          <button class="w-full py-4 border-b border-slate-200 hover:bg-slate-50 transition-colors">
            <i class="ri-menu-line text-slate-600 text-xl"></i>
          </button>
        </div>

        <button
          @click="showTaskForm = true"
          class="w-12 h-12 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg flex items-center justify-center mt-6 transition-colors"
        >
          <i class="ri-add-line text-2xl"></i>
        </button>
      </div>

      <!-- 主内容区 -->
      <div class="flex-1 bg-[#F5F7FA] overflow-y-auto">
        <div v-if="!showTaskForm" class="p-8">
          <!-- 页面标题 -->
          <div class="mb-6">
            <div class="flex items-center justify-between mb-2">
              <h1 class="text-2xl font-bold text-slate-800">朋友圈任务</h1>
              <button class="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm text-[#4A90E2] hover:bg-slate-50 transition-colors">
                发圈日志
              </button>
            </div>
            <div class="flex items-center space-x-2 text-sm">
              <span class="text-slate-600">今日自动发圈:</span>
              <span class="text-[#4A90E2] font-semibold">0 条</span>
            </div>
            <div class="text-xs text-orange-500 mt-1">发朋友圈仅支持 4.0 以上微信</div>
          </div>

          <!-- 任务列表 -->
          <div class="space-y-4">
            <div
              v-for="task in tasks"
              :key="task.id"
              class="bg-white rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow border border-slate-200"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <h3 class="text-base font-semibold text-slate-800 mb-2">{{ task.name }}</h3>
                  <div class="flex items-center space-x-4 text-sm text-slate-500">
                    <div class="flex items-center space-x-1">
                      <i class="ri-time-line"></i>
                      <span>{{ task.time }}</span>
                    </div>
                    <div class="flex items-center space-x-1">
                      <div
                        class="w-2 h-2 rounded-full"
                        :class="task.status === 'active' ? 'bg-teal-500' : 'bg-slate-400'"
                      ></div>
                      <span>{{ task.status === 'active' ? '运行中' : '已暂停' }}</span>
                    </div>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <button class="w-9 h-9 flex items-center justify-center bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">
                    <i class="ri-edit-line text-slate-600"></i>
                  </button>
                  <button class="w-9 h-9 flex items-center justify-center bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">
                    <i class="ri-delete-bin-line text-slate-600"></i>
                  </button>
                  <button class="w-9 h-9 flex items-center justify-center bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">
                    <i 
                      :class="task.status === 'active' ? 'ri-pause-line' : 'ri-play-line'"
                      class="text-slate-600"
                    ></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="p-8">
          <!-- 步骤指示器 -->
          <div class="max-w-4xl mx-auto mb-8">
            <div class="flex items-center justify-center space-x-4">
              <div class="flex flex-col items-center">
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center text-white font-semibold mb-2"
                  :class="currentStep === 1 ? 'bg-[#4A90E2]' : 'bg-teal-500'"
                >
                  <i v-if="currentStep > 1" class="ri-check-line text-lg"></i>
                  <span v-else>1</span>
                </div>
                <span class="text-sm text-slate-600">设置执行计划</span>
              </div>
              <div class="w-32 h-0.5 bg-slate-300 mb-6"></div>
              <div class="flex flex-col items-center">
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center font-semibold mb-2"
                  :class="currentStep === 2 ? 'bg-[#4A90E2] text-white' : 'bg-slate-200 text-slate-500'"
                >
                  2
                </div>
                <span class="text-sm text-slate-600">配置发圈素材</span>
              </div>
            </div>
          </div>

          <!-- 表单内容 -->
          <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-sm p-8">
            <div v-if="currentStep === 1" class="space-y-6">
              <!-- 计划名称 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  计划名称
                </label>
                <input
                  type="text"
                  v-model="taskName"
                  placeholder="请输入计划名称，如：1201-元旦发圈推广计划"
                  class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                />
              </div>

              <!-- 执行方式 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-3">
                  执行方式
                </label>
                <div class="flex items-center space-x-6">
                  <label class="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="radio"
                      name="executionType"
                      value="fixed"
                      v-model="executionType"
                      class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]"
                    />
                    <span class="text-sm text-slate-700">固定时间</span>
                  </label>
                  <label class="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="radio"
                      name="executionType"
                      value="multiple"
                      v-model="executionType"
                      class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]"
                    />
                    <span class="text-sm text-slate-700">时间段(发多条)</span>
                  </label>
                </div>
              </div>

              <!-- 时间选择 -->
              <div>
                <input
                  type="time"
                  v-model="executionTime"
                  class="px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                />
              </div>

              <!-- 执行周期 -->
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-3">
                  执行周期
                </label>
                <div class="flex items-center space-x-6 mb-4">
                  <label class="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="radio"
                      name="frequency"
                      value="daily"
                      v-model="frequency"
                      class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]"
                    />
                    <span class="text-sm text-slate-700">每天</span>
                  </label>
                  <label class="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="radio"
                      name="frequency"
                      value="weekly"
                      v-model="frequency"
                      class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]"
                    />
                    <span class="text-sm text-slate-700">每周</span>
                  </label>
                </div>

                <!-- 星期选择 -->
                <div v-if="frequency === 'weekly'" class="flex items-center space-x-3">
                  <label
                    v-for="day in [
                      { value: 1, label: '一' },
                      { value: 2, label: '二' },
                      { value: 3, label: '三' },
                      { value: 4, label: '四' },
                      { value: 5, label: '五' },
                      { value: 6, label: '六' },
                      { value: 0, label: '日' },
                    ]"
                    :key="day.value"
                    class="flex items-center space-x-1.5 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      :checked="selectedDays.includes(day.value)"
                      @change="toggleDay(day.value)"
                      class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                    />
                    <span class="text-sm text-slate-700">{{ day.label }}</span>
                  </label>
                </div>
              </div>
            </div>

            <div v-else class="space-y-6">
              <!-- 添加素材组 -->
              <div>
                <button class="flex items-center space-x-2 text-[#4A90E2] hover:text-[#357ABD] transition-colors">
                  <i class="ri-add-circle-line text-lg"></i>
                  <span class="text-sm font-medium">添加素材组</span>
                </button>
              </div>

              <!-- 素材文件类型选择 -->
              <div class="bg-[#2C3E50] rounded-lg p-6">
                <h3 class="text-white text-base font-medium mb-4">请选择素材文件类型</h3>
                <div class="text-sm text-slate-300 mb-4">选择素材文件类型，可预览素材组</div>
                
                <!-- 内容类型标签 -->
                <div class="flex items-center space-x-2 mb-6">
                  <button
                    v-for="type in [
                      { value: 'text', label: '纯文字' },
                      { value: 'image', label: '图片' },
                      { value: 'video', label: '视频' },
                      { value: 'link', label: '链接' },
                    ]"
                    :key="type.value"
                    @click="contentType = type.value"
                    class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
                    :class="contentType === type.value ? 'bg-[#4A90E2] text-white' : 'bg-[#34495E] text-slate-300 hover:bg-[#3D5266]'"
                  >
                    {{ type.label }}
                  </button>
                </div>

                <!-- 发布方式 -->
                <div class="mb-6">
                  <label class="block text-white text-sm font-medium mb-3">发布方式</label>
                  <div class="flex items-center space-x-6">
                    <label class="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="radio"
                        name="publishType"
                        value="order"
                        v-model="publishType"
                        class="w-4 h-4 text-[#4A90E2] border-slate-400 focus:ring-[#4A90E2]"
                      />
                      <span class="text-sm text-slate-300">按顺序发布</span>
                    </label>
                    <label class="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="radio"
                        name="publishType"
                        value="random"
                        v-model="publishType"
                        class="w-4 h-4 text-[#4A90E2] border-slate-400 focus:ring-[#4A90E2]"
                      />
                      <span class="text-sm text-slate-300">随机发布</span>
                    </label>
                  </div>
                </div>

                <!-- 选择账号 -->
                <div>
                  <label class="block text-white text-sm font-medium mb-3">选择账号</label>
                  <div class="relative">
                    <select
                      v-model="selectedAccount"
                      class="w-full px-4 py-2.5 bg-[#34495E] border border-[#4A5A6A] rounded-lg text-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
                    >
                      <option value="albertyan">albertyan</option>
                      <option value="user2">用户2</option>
                      <option value="user3">用户3</option>
                    </select>
                    <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                  </div>
                </div>
              </div>

              <!-- 内容编辑区域 -->
              <div class="space-y-4">
                <!-- 文字内容 -->
                <div v-if="contentType === 'text'">
                  <label class="block text-sm font-medium text-slate-700 mb-2">
                    发圈内容
                  </label>
                  <textarea
                    v-model="textContent"
                    placeholder="请输入朋友圈内容..."
                    rows="8"
                    class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
                  ></textarea>
                  <div class="text-xs text-slate-400 mt-1">
                    {{ textContent.length }} / 500 字符
                  </div>
                </div>

                <!-- 图片上传区域 -->
                <div v-if="contentType === 'image'">
                  <label class="block text-sm font-medium text-slate-700 mb-2">
                    上传图片
                  </label>
                  <div class="border-2 border-dashed border-slate-300 rounded-lg p-12 text-center hover:border-[#4A90E2] transition-colors cursor-pointer">
                    <i class="ri-image-add-line text-5xl text-slate-400 mb-3"></i>
                    <div class="text-sm text-slate-600 mb-1">点击或拖拽图片到此处上传</div>
                    <div class="text-xs text-slate-400">
                      支持 JPG、PNG 格式，最多9张
                    </div>
                  </div>
                </div>

                <!-- 视频上传区域 -->
                <div v-if="contentType === 'video'">
                  <label class="block text-sm font-medium text-slate-700 mb-2">
                    上传视频
                  </label>
                  <div class="border-2 border-dashed border-slate-300 rounded-lg p-12 text-center hover:border-[#4A90E2] transition-colors cursor-pointer">
                    <i class="ri-video-add-line text-5xl text-slate-400 mb-3"></i>
                    <div class="text-sm text-slate-600 mb-1">点击或拖拽视频到此处上传</div>
                    <div class="text-xs text-slate-400">
                      支持 MP4 格式，大小不超过 100MB
                    </div>
                  </div>
                </div>

                <!-- 链接输入 -->
                <div v-if="contentType === 'link'">
                  <label class="block text-sm font-medium text-slate-700 mb-2">
                    链接地址
                  </label>
                  <input
                    type="url"
                    placeholder="请输入链接地址"
                    class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                  />
                  <div class="mt-3">
                    <label class="block text-sm font-medium text-slate-700 mb-2">
                      链接标题
                    </label>
                    <input
                      type="text"
                      placeholder="请输入链接标题"
                      class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- 底部按钮 -->
            <div class="flex items-center justify-between mt-8 pt-6 border-t border-slate-200">
              <button
                v-if="currentStep === 2"
                @click="currentStep = 1"
                class="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 rounded-lg font-medium hover:bg-slate-50 transition-colors"
              >
                上一步
              </button>
              <button
                v-else
                @click="handleCancel"
                class="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 rounded-lg font-medium hover:bg-slate-50 transition-colors"
              >
                取消
              </button>
              <button
                @click="handleNextStep"
                class="px-8 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg font-medium transition-colors"
              >
                {{ currentStep === 1 ? '下一步' : '生成任务' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>