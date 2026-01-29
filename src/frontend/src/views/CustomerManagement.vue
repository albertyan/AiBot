<script setup>
import { ref, computed } from 'vue';
import NavBar from '../components/NavBar.vue';
import SyncSettingsModal from '../components/SyncSettingsModal.vue';

const activeTab = ref('friends');
const selectedCustomers = ref([]);
const searchQuery = ref('');
const filterDropdownOpen = ref(false);

// Settings Modal State
const isSettingsModalVisible = ref(false);

const customers = [
  { id: '1', name: "'Qv", wechatId: '62dcbb88', avatar: 'Q', color: 'bg-purple-500' },
  { id: '2', name: '+熊韦', wechatId: '69146682', avatar: '+', color: 'bg-purple-500' },
  { id: '3', name: '画中画', wechatId: '8fc5505', avatar: '画', color: 'bg-purple-500' },
  { id: '4', name: '1158', wechatId: '6048b3a', avatar: '1', color: 'bg-purple-500' },
  { id: '5', name: '123', wechatId: '202cb962', avatar: '1', color: 'bg-purple-500' },
  { id: '6', name: '13508765833', wechatId: '2348da5a', avatar: '1', color: 'bg-purple-500', tag: '前冠' },
  { id: '7', name: '13642811919', wechatId: '129532f2', avatar: '1', color: 'bg-purple-500', tag: '前冠' },
];

/** Toggle a single customer's selection */
const toggleCustomerSelection = (id) => {
  if (selectedCustomers.value.includes(id)) {
    selectedCustomers.value = selectedCustomers.value.filter((cid) => cid !== id);
  } else {
    selectedCustomers.value = [...selectedCustomers.value, id];
  }
};

/** Select all / deselect all customers */
const selectAll = () => {
  if (selectedCustomers.value.length === customers.length) {
    selectedCustomers.value = [];
  } else {
    selectedCustomers.value = customers.map((c) => c.id);
  }
};

/** Filter customers based on the current search query. */
const filteredCustomers = computed(() => {
  return searchQuery.value
    ? customers.filter((c) =>
        c.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        c.wechatId.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    : customers;
});

/** Get the actual customer objects for selected IDs */
const selectedCustomerObjects = computed(() => {
  return selectedCustomers.value
    .map((id) => customers.find((c) => c.id === id))
    .filter((c) => c !== undefined);
});
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <!-- 顶部导航 -->
    <NavBar />

    <!-- 主要内容区域 -->
    <div class="flex h-[calc(100vh-64px)]">
      <!-- 左侧客户列表 - 30% -->
      <div class="w-[30%] bg-white border-r border-slate-200 flex flex-col">
        <!-- 标签切换 -->
        <div class="border-b border-slate-200">
          <div class="flex">
            <button
              @click="activeTab = 'friends'"
              :class="`flex-1 py-3 text-sm font-medium transition-colors ${
                activeTab === 'friends'
                  ? 'text-[#4A90E2] bg-[#4A90E2]/5 border-b-2 border-[#4A90E2]'
                  : 'text-slate-500 hover:text-slate-700'
              }`"
            >
              好友
            </button>
            <button
              @click="activeTab = 'groups'"
              :class="`flex-1 py-3 text-sm font-medium transition-colors ${
                activeTab === 'groups'
                  ? 'text-[#4A90E2] bg-[#4A90E2]/5 border-b-2 border-[#4A90E2]'
                  : 'text-slate-500 hover:text-slate-700'
              }`"
            >
              群聊
            </button>
          </div>
        </div>

        <!-- 搜索框 -->
        <div class="p-4 border-b border-slate-200">
          <div class="relative">
            <i class="ri-search-line absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
            <input
              type="text"
              placeholder="搜索好友或群聊"
              v-model="searchQuery"
              class="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
          </div>
        </div>

        <!-- 客户统计和全选 -->
        <div class="px-4 py-3 border-b border-slate-200 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-sm text-slate-600">
              好友 (<span class="font-semibold">{{ customers.length }}</span>)
            </span>
          </div>
          <button
            @click="selectAll"
            class="text-xs text-[#4A90E2] hover:text-[#357ABD] font-medium transition-colors"
          >
            全选
          </button>
        </div>

        <!-- 客户列表 -->
        <div class="flex-1 overflow-y-auto">
          <div
            v-for="customer in filteredCustomers"
            :key="customer.id"
            @click="toggleCustomerSelection(customer.id)"
            :class="`px-4 py-3 border-b border-slate-100 hover:bg-slate-50 cursor-pointer transition-colors ${
              selectedCustomers.includes(customer.id)
                ? 'bg-[#4A90E2]/5 border-l-4 border-l-[#4A90E2]'
                : ''
            }`"
          >
            <div class="flex items-center space-x-3">
              <div class="relative">
                <div
                  :class="`w-10 h-10 ${customer.color} rounded-lg flex items-center justify-center text-white font-semibold text-sm`"
                >
                  {{ customer.avatar }}
                </div>
                <div v-if="customer.tag" class="absolute -top-1 -right-1 w-4 h-4 bg-orange-400 rounded-full flex items-center justify-center">
                  <i class="ri-vip-crown-fill text-white text-[8px]"></i>
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2">
                  <div class="text-sm font-medium text-slate-800 truncate">{{ customer.name }}</div>
                  <span v-if="customer.tag" class="text-xs text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                    {{ customer.tag }}
                  </span>
                </div>
                <div class="text-xs text-slate-400 truncate">{{ customer.wechatId }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧操作区域 - 70% -->
      <div class="flex-1 bg-[#F5F7FA] flex flex-col">
        <!-- 顶部筛选区域 -->
        <div class="bg-white border-b border-slate-200 p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-slate-800">选择目标</h2>
            <div class="relative">
              <button
                @click="filterDropdownOpen = !filterDropdownOpen"
                class="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-700 hover:bg-slate-50 transition-colors flex items-center space-x-2"
              >
                <span>全部</span>
                <i class="ri-arrow-down-s-line text-base"></i>
              </button>

              <div v-if="filterDropdownOpen" class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 py-2 z-10">
                <button class="w-full px-4 py-2 text-left text-sm text-[#4A90E2] hover:bg-slate-50 transition-colors">
                  全部
                </button>
                <button class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                  未分组 (1109)
                </button>
                <button class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                  前冠 (195)
                </button>
                <button class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                  楼市通 (30)
                </button>
                <button class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                  云南前冠 (11)
                </button>
                <button class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                  中软 (1)
                </button>
                <button class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                  博美 (1)
                </button>
                <button class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                  车领主 (1)
                </button>
              </div>
            </div>
          </div>

          <!-- 已选择的客户 -->
          <div class="mb-4">
            <div class="flex items-center space-x-2 mb-3">
              <span class="text-sm text-slate-600">已选择的好友</span>
              <span class="w-6 h-6 bg-[#4A90E2] text-white rounded-full flex items-center justify-center text-xs font-semibold">
                {{ selectedCustomers.length }}
              </span>
            </div>

            <div class="flex flex-wrap gap-3">
              <div
                v-for="customer in selectedCustomerObjects"
                :key="customer.id"
                class="flex items-center space-x-2 bg-blue-50 border border-blue-200 rounded-lg px-3 py-2"
              >
                <div
                  :class="`w-8 h-8 ${customer.color} rounded-lg flex items-center justify-center text-white font-semibold text-xs`"
                >
                  {{ customer.avatar }}
                </div>
                <span class="text-sm text-slate-700">{{ customer.name }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 批量操作区域 -->
        <div class="flex-1 p-6">
          <h3 class="text-base font-semibold text-slate-800 mb-4">批量操作</h3>

          <div class="grid grid-cols-3 gap-4">
            <!-- 群发消息 -->
            <button class="bg-gradient-to-br from-[#4A90E2] to-[#357ABD] rounded-xl p-6 text-white hover:shadow-lg transition-all group">
              <div class="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <i class="ri-message-3-line text-2xl"></i>
              </div>
              <div class="text-left">
                <div class="font-semibold mb-1">群发消息</div>
              </div>
            </button>

            <!-- 批量拉群 -->
            <button class="bg-white rounded-xl p-6 border-2 border-slate-200 hover:border-[#4A90E2] hover:shadow-md transition-all group">
              <div class="w-12 h-12 bg-[#4A90E2]/10 rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <i class="ri-group-line text-2xl text-[#4A90E2]"></i>
              </div>
              <div class="text-left">
                <div class="font-semibold text-slate-800 mb-1">批量拉群</div>
              </div>
            </button>

            <!-- 自动跟单 -->
            <button class="bg-white rounded-xl p-6 border-2 border-slate-200 hover:border-[#4A90E2] hover:shadow-md transition-all group">
              <div class="w-12 h-12 bg-[#4A90E2]/10 rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <i class="ri-user-follow-line text-2xl text-[#4A90E2]"></i>
              </div>
              <div class="text-left">
                <div class="font-semibold text-slate-800 mb-1">自动跟单</div>
              </div>
            </button>
          </div>

          <!-- 设置按钮 -->
          <div class="mt-6 flex justify-end">
            <button 
              @click="isSettingsModalVisible = true"
              class="px-6 py-3 bg-white border border-slate-200 rounded-lg text-slate-700 hover:bg-slate-50 transition-colors flex items-center space-x-2"
            >
              <i class="ri-settings-3-line text-base"></i>
              <span class="text-sm font-medium">设置</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 同步通讯录设置弹窗 -->
    <SyncSettingsModal v-model="isSettingsModalVisible" />
  </div>
</template>
