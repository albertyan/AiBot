<script setup>
import { ref } from 'vue';
import ImportListModal from '../ImportListModal.vue';

const addDailyLimit = ref(10);
const addCheckInterval = ref(30);
const maxAddPerTime = ref(1);
const verificationMessage = ref('');
const multiWechatLoopAdd = ref(false);
const showImportModal = ref(false);

const safeParseInt = (value, fallback) => {
  const parsed = parseInt(value);
  return isNaN(parsed) ? fallback : Math.max(1, parsed);
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

const handleImportSuccess = (data) => {
  console.log('Imported friend list:', data);
  // 这里可以处理导入的数据，例如显示在列表中或者提示用户
};
</script>

<template>
  <div class="flex-1 flex">
    <!-- 添加好友配置区域 -->
    <div class="w-[45%] bg-white border-r border-slate-200 overflow-y-auto">
      <div class="p-6">
        <h2 class="text-lg font-semibold text-slate-800 mb-6">添加好友配置</h2>

        <!-- 顶部标签切换 -->
        <div class="flex items-center space-x-2 mb-6">
          <button 
            @click="showImportModal = true"
            class="px-4 py-2 bg-[#4A90E2] text-white rounded-lg text-sm font-medium hover:bg-[#357ABD] transition-colors"
          >
            导入名单
          </button>
          <button class="px-4 py-2 bg-slate-100 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-200 transition-colors">
            记录
          </button>
          <!-- <button class="px-4 py-2 bg-slate-100 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-200 transition-colors">
            操作日志
          </button> -->
        </div>

        <!-- 导入名单弹窗 -->
        <ImportListModal
          v-model:open="showImportModal"
          @success="handleImportSuccess"
        />

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
  </div>
</template>
