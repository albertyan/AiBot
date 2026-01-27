<script setup>
import { ref } from 'vue';
import NavBar from '../components/NavBar.vue';

const activeSection = ref('ai-access');
const cozeToken = ref('');
const difyUrl = ref('');
const commentLimit = ref(10);
const commentPerFriend = ref(2);
const interactionMode = ref('点赞&评论');
const selectedAgent = ref('');
const blacklistText = ref('');

// 话术组配置状态
const scriptGroups = ref([
  { id: '1', name: '话术组1', scripts: ['你好，很高兴认识你！', '最近怎么样？'] },
]);
const showAddScriptGroup = ref(false);
const newScriptGroupName = ref('');
const newScript = ref('');

// AI回复配置状态
const mergeReply = ref('不合并');
const monitorInterval = ref(5);
const aiOnTop = ref(false);
const transferKeywords = ref('');
const transferWechatNickname = ref('');

// 外部API配置状态
const apiIdentifier = ref('');
const apiUrl = ref('');
const apiKey = ref('');
const apiDescription = ref('');

// 预警配置状态
const alertEmail = ref('');
const enableEmailAlert = ref(true);
const alertFrequency = ref('立即通知');

// 休息时间设置状态
const restStartTime = ref('00:00');
const restEndTime = ref('05:30');
const autoAddFriend = ref(true);
const autoPassFriend = ref(true);
const enableRestTime = ref(true);

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

const agents = [
  { id: '1', name: '过敏', botId: '75326*****55496' },
];

const safeParseInt = (value, fallback) => {
  const parsed = parseInt(value);
  return isNaN(parsed) ? fallback : Math.max(1, parsed);
};

// 生成时间选项
const generateTimeOptions = () => {
  const options = [];
  for (let h = 0; h < 24; h++) {
    for (let m = 0; m < 60; m += 30) {
      const hour = h.toString().padStart(2, '0');
      const minute = m.toString().padStart(2, '0');
      options.push(`${hour}:${minute}`);
    }
  }
  return options;
};

const handleAddScriptGroup = () => {
  if (newScriptGroupName.value.trim()) {
    scriptGroups.value.push({
      id: Date.now().toString(),
      name: newScriptGroupName.value,
      scripts: [],
    });
    newScriptGroupName.value = '';
    showAddScriptGroup.value = false;
  }
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
          <div v-if="activeSection === 'ai-access'" class="space-y-6">
            <h1 class="text-2xl font-bold text-slate-800">AI接入配置</h1>

            <!-- Coze平台 -->
            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="flex items-center justify-between mb-6">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
                    <i class="ri-robot-line text-white text-lg"></i>
                  </div>
                  <h2 class="text-lg font-semibold text-slate-800">Coze平台</h2>
                </div>
                <button class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors">
                  清除全部缓存
                </button>
              </div>

              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">Coze Token</label>
                  <div class="relative">
                    <input
                      type="password"
                      v-model="cozeToken"
                      placeholder="请输入Coze Token"
                      class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                    <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                      <i class="ri-eye-line"></i>
                    </button>
                  </div>
                  <p class="text-xs text-orange-500 mt-2">token已使用 176 天，如果永久期限，记得到期及时更换</p>
                </div>
              </div>
            </div>

            <!-- Dify平台 -->
            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="flex items-center space-x-3 mb-6">
                <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
                  <i class="ri-robot-2-line text-white text-lg"></i>
                </div>
                <h2 class="text-lg font-semibold text-slate-800">Dify平台</h2>
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">服务器地址</label>
                <input
                  type="text"
                  v-model="difyUrl"
                  placeholder="如果是本地则默认可输入：http://localhost/v1"
                  class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                />
              </div>
            </div>
          </div>

          <!-- 智能体管理 -->
          <div v-else-if="activeSection === 'agent-management'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h1 class="text-2xl font-bold text-slate-800">智能体管理</h1>
              <button class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors">
                测试
              </button>
            </div>

            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="space-y-4">
                <div v-for="agent in agents" :key="agent.id" class="flex items-center justify-between p-4 border border-slate-200 rounded-lg">
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
                      <i class="ri-robot-line text-white text-lg"></i>
                    </div>
                    <div>
                      <div class="text-sm font-semibold text-slate-800">{{ agent.name }}</div>
                      <div class="text-xs text-slate-500">Bot ID: {{ agent.botId }}</div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button class="px-3 py-1.5 bg-green-50 text-green-600 rounded text-xs font-medium hover:bg-green-100 transition-colors">
                      默认
                    </button>
                    <button class="w-8 h-8 flex items-center justify-center text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                      <i class="ri-delete-bin-line"></i>
                    </button>
                  </div>
                </div>
              </div>

              <button class="w-full mt-4 px-4 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors">
                添加智能体
              </button>
            </div>
          </div>

          <!-- 朋友圈评论设置 -->
          <div v-else-if="activeSection === 'moments-review'" class="space-y-6">
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

          <!-- 话术组配置 -->
          <div v-else-if="activeSection === 'tag-group'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h1 class="text-2xl font-bold text-slate-800">话术组配置（可配合智能体）</h1>
              <button
                @click="showAddScriptGroup = true"
                class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
              >
                添加话术组
              </button>
            </div>

            <!-- 话术组列表 -->
            <div class="space-y-4">
              <div v-for="group in scriptGroups" :key="group.id" class="bg-white rounded-lg shadow-sm p-6">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-semibold text-slate-800">{{ group.name }}</h3>
                  <button class="w-8 h-8 flex items-center justify-center text-red-500 hover:bg-red-50 rounded-lg transition-colors">
                    <i class="ri-delete-bin-line"></i>
                  </button>
                </div>
                <div class="space-y-2">
                  <div v-for="(script, index) in group.scripts" :key="index" class="flex items-start space-x-3 p-3 bg-slate-50 rounded-lg">
                    <span class="text-sm text-slate-500 mt-0.5">{{ index + 1 }}.</span>
                    <p class="flex-1 text-sm text-slate-700">{{ script }}</p>
                    <button class="text-slate-400 hover:text-red-500 transition-colors">
                      <i class="ri-close-line"></i>
                    </button>
                  </div>
                </div>
                <button class="w-full mt-4 px-4 py-2 border-2 border-dashed border-slate-300 hover:border-[#4A90E2] text-slate-600 hover:text-[#4A90E2] rounded-lg text-sm font-medium transition-colors">
                  + 添加话术
                </button>
              </div>
            </div>

            <!-- 添加话术组弹窗 -->
            <div v-if="showAddScriptGroup" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
              <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
                <div class="flex items-center justify-between p-6 border-b border-slate-200">
                  <h2 class="text-xl font-semibold text-slate-800">添加话术组</h2>
                  <button
                    @click="showAddScriptGroup = false"
                    class="w-8 h-8 flex items-center justify-center hover:bg-slate-100 rounded-lg transition-colors"
                  >
                    <i class="ri-close-line text-xl text-slate-600"></i>
                  </button>
                </div>
                <div class="p-6 space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-2">话术组名称</label>
                    <input
                      type="text"
                      v-model="newScriptGroupName"
                      placeholder="请输入话术组名称"
                      class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                  </div>
                </div>
                <div class="flex items-center justify-end space-x-3 p-6 border-t border-slate-200">
                  <button
                    @click="showAddScriptGroup = false"
                    class="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 rounded-lg font-medium hover:bg-slate-50 transition-colors whitespace-nowrap"
                  >
                    取消
                  </button>
                  <button
                    @click="handleAddScriptGroup"
                    class="px-6 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg font-medium transition-colors whitespace-nowrap"
                  >
                    确定
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- AI回复配置 -->
          <div v-else-if="activeSection === 'ai-reply'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h1 class="text-2xl font-bold text-slate-800">AI回复配置</h1>
              <button class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors whitespace-nowrap">
                保存设置
              </button>
            </div>

            <div class="bg-white rounded-lg shadow-sm p-6">
              <!-- 提示信息 -->
              <div class="flex items-start space-x-3 bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <i class="ri-information-fill text-blue-500 text-xl mt-0.5"></i>
                <div class="text-sm text-blue-700">
                  聊天记录是自动保存本地data文件夹
                </div>
              </div>

              <div class="space-y-6">
                <!-- 消息合并回复 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">消息合并回复</label>
                  <div class="relative">
                    <select
                      v-model="mergeReply"
                      class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
                    >
                      <option value="不合并">不合并</option>
                      <option value="合并">合并</option>
                    </select>
                    <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                  </div>
                  <button class="mt-2 text-sm text-slate-500 hover:text-slate-700 flex items-center space-x-1">
                    <i class="ri-question-line"></i>
                    <span>查看说明</span>
                  </button>
                </div>

                <!-- 消息监听间隔 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">消息监听间隔(秒)</label>
                  <div class="flex items-center space-x-3">
                    <button
                      @click="monitorInterval = Math.max(1, monitorInterval - 1)"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
                    >
                      <i class="ri-subtract-line text-slate-600"></i>
                    </button>
                    <input
                      type="number"
                      v-model.number="monitorInterval"
                      @change="monitorInterval = safeParseInt($event.target.value, 1)"
                      class="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-center text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                    <button
                      @click="monitorInterval += 1"
                      class="w-10 h-10 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center justify-center transition-colors"
                    >
                      <i class="ri-add-line text-slate-600"></i>
                    </button>
                  </div>
                  <button class="mt-2 text-sm text-slate-500 hover:text-slate-700 flex items-center space-x-1">
                    <i class="ri-question-line"></i>
                    <span>查看说明</span>
                  </button>
                </div>

                <!-- AI智能体上下文 -->
                <div>
                  <div class="flex items-center justify-between mb-3">
                    <label class="text-sm font-medium text-slate-700">AI智能体上下文</label>
                    <div class="flex items-center space-x-2">
                      <span class="text-sm text-slate-600">{{ aiOnTop ? '开启' : '关闭' }}</span>
                      <button
                        @click="aiOnTop = !aiOnTop"
                        class="relative w-12 h-6 rounded-full transition-colors"
                        :class="aiOnTop ? 'bg-[#4A90E2]' : 'bg-slate-300'"
                      >
                        <span
                          class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform"
                          :class="aiOnTop ? 'translate-x-6' : ''"
                        ></span>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- 转人工配置 -->
                <div class="pt-4 border-t border-slate-200">
                  <h3 class="text-base font-semibold text-slate-800 mb-4">转人工配置</h3>
                  
                  <!-- 话术词 -->
                  <div class="mb-6">
                    <div class="flex items-center justify-between mb-3">
                      <label class="text-sm font-medium text-slate-700">话术词</label>
                      <button class="px-3 py-1.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded text-xs font-medium transition-colors whitespace-nowrap">
                        + 添加
                      </button>
                    </div>
                    <p class="text-xs text-slate-500 mb-3">当AI回复中含中话术词时，将触发转人工通知</p>
                    <textarea
                      v-model="transferKeywords"
                      placeholder="请输入话术词，多个词用逗号分隔"
                      rows="3"
                      class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
                    ></textarea>
                  </div>

                  <!-- 接收通知的微信昵称 -->
                  <div>
                    <label class="block text-sm font-medium text-slate-700 mb-3">接收通知的微信昵称</label>
                    <p class="text-xs text-slate-500 mb-3">转人工通知将发送给此微信</p>
                    <input
                      type="text"
                      v-model="transferWechatNickname"
                      placeholder="请输入用于接收转人工通知的备用微信昵称"
                      class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 外部API配置 -->
          <div v-else-if="activeSection === 'external-api'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h1 class="text-2xl font-bold text-slate-800">外部API配置</h1>
              <button class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap">
                保存配置
              </button>
            </div>

            <div class="bg-white rounded-lg shadow-sm p-6">
              <!-- 提示信息 -->
              <div class="flex items-start space-x-3 bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <i class="ri-information-fill text-blue-500 text-xl mt-0.5"></i>
                <div class="text-sm text-blue-700">
                  定制API需要对接调试，可联系客服咨询
                </div>
              </div>

              <div class="space-y-6">
                <!-- API标识符 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">API标识符</label>
                  <input
                    type="text"
                    v-model="apiIdentifier"
                    placeholder="请输入API标识符"
                    class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                  />
                  <p class="text-xs text-slate-500 mt-2">用于识别不同的API接口</p>
                </div>

                <!-- API地址 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">API地址</label>
                  <input
                    type="url"
                    v-model="apiUrl"
                    placeholder="https://api.example.com/endpoint"
                    class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                  />
                </div>

                <!-- API密钥 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">API密钥</label>
                  <div class="relative">
                    <input
                      type="password"
                      v-model="apiKey"
                      placeholder="请输入API密钥"
                      class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    />
                    <button class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                      <i class="ri-eye-line"></i>
                    </button>
                  </div>
                </div>

                <!-- API描述 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">API描述</label>
                  <textarea
                    v-model="apiDescription"
                    placeholder="请输入API的功能描述和使用说明"
                    rows="4"
                    class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
                  ></textarea>
                </div>

                <!-- 测试按钮 -->
                <div class="flex items-center space-x-3 pt-4">
                  <button class="px-6 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium transition-colors whitespace-nowrap">
                    测试连接
                  </button>
                  <span class="text-sm text-slate-500">测试API是否可以正常连接</span>
                </div>
              </div>
            </div>

            <!-- API列表 -->
            <div class="bg-white rounded-lg shadow-sm p-6">
              <h3 class="text-base font-semibold text-slate-800 mb-4">已配置的API</h3>
              <div class="text-center py-12">
                <i class="ri-link text-5xl text-slate-300 mb-3"></i>
                <div class="text-sm text-slate-400">暂无已配置的API</div>
              </div>
            </div>
          </div>

          <!-- 预警配置 -->
          <div v-else-if="activeSection === 'forecast'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h1 class="text-2xl font-bold text-slate-800">预警配置</h1>
              <button class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap">
                保存设置
              </button>
            </div>

            <div class="bg-white rounded-lg shadow-sm p-6">
              <!-- 提示信息 -->
              <div class="flex items-start space-x-3 bg-orange-50 border border-orange-200 rounded-lg p-4 mb-6">
                <i class="ri-alarm-warning-fill text-orange-500 text-xl mt-0.5"></i>
                <div class="text-sm text-orange-700">
                  当自动回复挂掉时会发送邮件提醒，请确保邮箱地址正确
                </div>
              </div>

              <div class="space-y-6">
                <!-- 启用邮件预警 -->
                <div>
                  <div class="flex items-center justify-between mb-4">
                    <label class="text-sm font-medium text-slate-700">启用邮件预警</label>
                    <div class="flex items-center space-x-2">
                      <span class="text-sm text-slate-600">{{ enableEmailAlert ? '已启用' : '已禁用' }}</span>
                      <button
                        @click="enableEmailAlert = !enableEmailAlert"
                        class="relative w-12 h-6 rounded-full transition-colors"
                        :class="enableEmailAlert ? 'bg-[#4A90E2]' : 'bg-slate-300'"
                      >
                        <span
                          class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform"
                          :class="enableEmailAlert ? 'translate-x-6' : ''"
                        ></span>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- 预警邮箱 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">预警邮箱</label>
                  <input
                    type="email"
                    v-model="alertEmail"
                    placeholder="请输入接收预警通知的邮箱地址"
                    class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
                    :disabled="!enableEmailAlert"
                  />
                  <p class="text-xs text-slate-500 mt-2">系统异常时将向此邮箱发送预警通知</p>
                </div>

                <!-- 预警频率 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-3">预警频率</label>
                  <div class="relative">
                    <select
                      v-model="alertFrequency"
                      class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
                      :disabled="!enableEmailAlert"
                    >
                      <option value="立即通知">立即通知</option>
                      <option value="每5分钟">每5分钟</option>
                      <option value="每15分钟">每15分钟</option>
                      <option value="每30分钟">每30分钟</option>
                      <option value="每小时">每小时</option>
                    </select>
                    <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                  </div>
                  <p class="text-xs text-slate-500 mt-2">设置预警通知的发送频率</p>
                </div>

                <!-- 预警条件 -->
                <div class="pt-4 border-t border-slate-200">
                  <h3 class="text-base font-semibold text-slate-800 mb-4">预警条件</h3>
                  <div class="space-y-3">
                    <label class="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
                      <input
                        type="checkbox"
                        checked
                        class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                        :disabled="!enableEmailAlert"
                      />
                      <div class="flex-1">
                        <div class="text-sm font-medium text-slate-700">AI回复服务停止</div>
                        <div class="text-xs text-slate-500">当AI自动回复服务停止运行时发送预警</div>
                      </div>
                    </label>
                    <label class="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
                      <input
                        type="checkbox"
                        checked
                        class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                        :disabled="!enableEmailAlert"
                      />
                      <div class="flex-1">
                        <div class="text-sm font-medium text-slate-700">API连接失败</div>
                        <div class="text-xs text-slate-500">当外部API连接失败时发送预警</div>
                      </div>
                    </label>
                    <label class="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
                      <input
                        type="checkbox"
                        class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                        :disabled="!enableEmailAlert"
                      />
                      <div class="flex-1">
                        <div class="text-sm font-medium text-slate-700">系统资源异常</div>
                        <div class="text-xs text-slate-500">当系统资源占用过高时发送预警</div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- 测试预警 -->
                <div class="flex items-center space-x-3 pt-4">
                  <button 
                    class="px-6 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium transition-colors whitespace-nowrap"
                    :disabled="!enableEmailAlert"
                  >
                    发送测试邮件
                  </button>
                  <span class="text-sm text-slate-500">测试预警邮件是否能正常发送</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 休息时间设置 -->
          <div v-else-if="activeSection === 'rest-time'" class="space-y-6">
            <div class="flex items-center justify-between">
              <h1 class="text-2xl font-bold text-slate-800">休息时间设置</h1>
              <button class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap">
                保存设置
              </button>
            </div>

            <div class="bg-white rounded-lg shadow-sm p-6">
              <!-- 启用休息时间 -->
              <div class="mb-6">
                <div class="flex items-center justify-between mb-4">
                  <label class="text-sm font-medium text-slate-700">启用休息时间</label>
                  <div class="flex items-center space-x-2">
                    <span class="text-sm text-slate-600">{{ enableRestTime ? '已启用' : '已禁用' }}</span>
                    <button
                      @click="enableRestTime = !enableRestTime"
                      class="relative w-12 h-6 rounded-full transition-colors"
                      :class="enableRestTime ? 'bg-[#4A90E2]' : 'bg-slate-300'"
                    >
                      <span
                        class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform"
                        :class="enableRestTime ? 'translate-x-6' : ''"
                      ></span>
                    </button>
                  </div>
                </div>
                <p class="text-xs text-slate-500">启用后，在休息时间段内将暂停执行已勾选的任务</p>
              </div>

              <!-- 休息时间显示 -->
              <div class="mb-6 p-6 bg-gradient-to-r from-blue-50 to-teal-50 rounded-lg border border-blue-100">
                <div class="flex items-center justify-center space-x-4 mb-4">
                  <div class="text-center">
                    <div class="text-3xl font-bold text-[#4A90E2]">{{ restStartTime }}</div>
                    <div class="text-xs text-slate-600 mt-1">开始时间</div>
                  </div>
                  <div class="text-2xl text-slate-400">-</div>
                  <div class="text-center">
                    <div class="text-3xl font-bold text-[#4A90E2]">{{ restEndTime }}</div>
                    <div class="text-xs text-slate-600 mt-1">结束时间</div>
                  </div>
                </div>
                
                <!-- 时间轴可视化 -->
                <div class="relative h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div 
                    class="absolute h-full bg-[#4A90E2] rounded-full"
                    style="left: 0%; width: 22.9%"
                  ></div>
                </div>
                <div class="flex justify-between text-xs text-slate-500 mt-2">
                  <span>00:00</span>
                  <span>06:00</span>
                  <span>12:00</span>
                  <span>18:00</span>
                  <span>24:00</span>
                </div>
              </div>

              <div class="space-y-6">
                <!-- 开始时间 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">开始时间</label>
                  <div class="relative">
                    <select
                      v-model="restStartTime"
                      class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
                      :disabled="!enableRestTime"
                    >
                      <option v-for="time in generateTimeOptions()" :key="time" :value="time">{{ time }}</option>
                    </select>
                    <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                  </div>
                </div>

                <!-- 结束时间 -->
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">结束时间</label>
                  <div class="relative">
                    <select
                      v-model="restEndTime"
                      class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
                      :disabled="!enableRestTime"
                    >
                      <option v-for="time in generateTimeOptions()" :key="time" :value="time">{{ time }}</option>
                    </select>
                    <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
                  </div>
                </div>

                <!-- 应用到的任务 -->
                <div class="pt-4 border-t border-slate-200">
                  <h3 class="text-base font-semibold text-slate-800 mb-4">应用到的任务</h3>
                  <p class="text-xs text-slate-500 mb-4">选择在休息时间内需要暂停的任务</p>
                  
                  <div class="space-y-3">
                    <label class="flex items-center justify-between p-4 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
                      <div class="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          v-model="autoAddFriend"
                          class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                          :disabled="!enableRestTime"
                        />
                        <div>
                          <div class="text-sm font-medium text-slate-700">自动加好友</div>
                          <div class="text-xs text-slate-500">休息时间内暂停自动添加好友</div>
                        </div>
                      </div>
                      <span v-if="autoAddFriend" class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded whitespace-nowrap">
                        已应用
                      </span>
                    </label>

                    <label class="flex items-center justify-between p-4 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
                      <div class="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          v-model="autoPassFriend"
                          class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                          :disabled="!enableRestTime"
                        />
                        <div>
                          <div class="text-sm font-medium text-slate-700">自动通过好友</div>
                          <div class="text-xs text-slate-500">休息时间内暂停自动通过好友申请</div>
                        </div>
                      </div>
                      <span v-if="autoPassFriend" class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded whitespace-nowrap">
                        已应用
                      </span>
                    </label>

                    <label class="flex items-center justify-between p-4 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
                      <div class="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                          :disabled="!enableRestTime"
                        />
                        <div>
                          <div class="text-sm font-medium text-slate-700">朋友圈自动评论</div>
                          <div class="text-xs text-slate-500">休息时间内暂停朋友圈自动评论</div>
                        </div>
                      </div>
                    </label>

                    <label class="flex items-center justify-between p-4 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
                      <div class="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                          :disabled="!enableRestTime"
                        />
                        <div>
                          <div class="text-sm font-medium text-slate-700">AI自动回复</div>
                          <div class="text-xs text-slate-500">休息时间内暂停AI自动回复消息</div>
                        </div>
                      </div>
                    </label>
                  </div>

                  <div class="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <div class="flex items-start space-x-2">
                      <i class="ri-information-fill text-blue-500 text-sm mt-0.5"></i>
                      <p class="text-xs text-blue-700">
                        未勾选的任务不会受休息时间限制，将继续正常运行
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
