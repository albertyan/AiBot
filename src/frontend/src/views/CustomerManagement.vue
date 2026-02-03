<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import NavBar from '../components/NavBar.vue';
import SyncSettingsModal from '../components/SyncSettingsModal.vue';
import SetGroupTagsModal from '../components/SetGroupTagsModal.vue';
import { getFriends, getGroups, getFriendTags, getGroupTags } from '../api/custom';

const activeTab = ref('friends');
const selectedFriendIds = ref([]);
const selectedGroupIds = ref([]);
const searchQuery = ref('');
const filterDropdownOpen = ref(false);
const currentFilter = ref('全部');
const isLoading = ref(false);

// Settings Modal State
const isSettingsModalVisible = ref(false);
const isSetGroupTagsModalVisible = ref(false);

const friends = ref([]);
const groups = ref([]);
const friendTags = ref([{ name: '全部', count: null }]);
const groupTags = ref([{ name: '全部', count: null }]);

const colors = ['bg-[#6366f1]', 'bg-[#f59e0b]', 'bg-[#10b981]', 'bg-[#ef4444]', 'bg-[#8b5cf6]', 'bg-[#ec4899]'];
const getColor = (name) => {
  if (!name) return colors[0];
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return colors[Math.abs(hash) % colors.length];
};

const fetchData = async () => {
  isLoading.value = true;
  try {
    const [friendsRes, groupsRes, friendTagsRes, groupTagsRes] = await Promise.all([
      getFriends(),
      getGroups(),
      getFriendTags(),
      getGroupTags()
    ]);

    if (friendsRes.code === 200) {
      friends.value = friendsRes.data.map(f => {
        const name = f.name;
        return {
          id: f.id,
          name: name,
          wechatId: f.wxid,
          avatar: name[0]?.toUpperCase() || '?',
          color: getColor(name),
          tag: f.tag
        };
      });
    }

    if (groupsRes.code === 200) {
      groups.value = groupsRes.data.map(g => {
        const name = g.name;
        return {
          id: g.id,
          name: name,
          wechatId: g.name, // Groups don't have wxid exposed yet
          avatar: '群',
          color: getColor(name),
          tag: g.tag,
          count: 0 // Backend doesn't provide member count yet
        };
      });
    }

    if (friendTagsRes.code === 200) {
      friendTags.value = [
        { name: '全部', count: null },
        ...friendTagsRes.data.map(t => ({
          name: t.tag,
          count: t.contact_count
        }))
      ];
    }

    // Process group tags
    if (groupTagsRes.code === 200) {
      // Calculate counts from groups list since backend only returns tag names
      const tagCounts = {};
      groups.value.forEach(g => {
        if (g.tag) {
          tagCounts[g.tag] = (tagCounts[g.tag] || 0) + 1;
        } else {
           // Handle untagged or '未分组' if needed, but for now stick to backend tags
        }
      });

      groupTags.value = [
        { name: '全部', count: null },
        ...groupTagsRes.data.map(t => ({
          name: t,
          count: tagCounts[t] || 0
        }))
      ];
    }

  } catch (error) {
    console.error('Failed to fetch data:', error);
    message.error('获取数据失败');
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchData();
});

// Current list based on active tab
const currentList = computed(() => activeTab.value === 'friends' ? friends.value : groups.value);

// Current tags based on active tab
const currentTags = computed(() => activeTab.value === 'friends' ? friendTags.value : groupTags.value);

/** Toggle a single item's selection */
const toggleSelection = (id) => {
  const targetArray = activeTab.value === 'friends' ? selectedFriendIds : selectedGroupIds;
  
  if (targetArray.value.includes(id)) {
    targetArray.value = targetArray.value.filter((cid) => cid !== id);
  } else {
    targetArray.value = [...targetArray.value, id];
  }
};

/** Select all / deselect all items in current filtered list */
const selectAll = () => {
  const currentIds = filteredList.value.map(item => item.id);
  const targetArray = activeTab.value === 'friends' ? selectedFriendIds : selectedGroupIds;
  
  const allSelected = currentIds.every(id => targetArray.value.includes(id));
  
  if (allSelected) {
    // Deselect current visible items
    targetArray.value = targetArray.value.filter(id => !currentIds.includes(id));
  } else {
    // Select all current visible items
    const newIds = currentIds.filter(id => !targetArray.value.includes(id));
    targetArray.value = [...targetArray.value, ...newIds];
  }
};

/** Clear all selections */
const clearSelection = () => {
  selectedFriendIds.value = [];
  selectedGroupIds.value = [];
};

/** Remove a specific friend from selection */
const deselectFriend = (id) => {
  selectedFriendIds.value = selectedFriendIds.value.filter(cid => cid !== id);
};

/** Remove a specific group from selection */
const deselectGroup = (id) => {
  selectedGroupIds.value = selectedGroupIds.value.filter(cid => cid !== id);
};

/** Filter list based on the current search query and selected tag. */
const filteredList = computed(() => {
  let list = currentList.value;

  // 1. Filter by Tag
  if (currentFilter.value !== '全部') {
    list = list.filter(item => {
      if (!item.tag) return false;
      // Split by comma or Chinese comma, trim whitespace
      const tags = item.tag.split(/[,，]/).map(t => t.trim());
      return tags.includes(currentFilter.value);
    });
  }

  // 2. Filter by Search Query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    list = list.filter((c) =>
      c.name.toLowerCase().includes(query) ||
      c.wechatId.toLowerCase().includes(query)
    );
  }
  
  return list;
});

/** Get the actual objects for selected IDs */
const selectedFriendObjects = computed(() => {
  return selectedFriendIds.value
    .map((id) => friends.value.find((c) => c.id === id))
    .filter((c) => c !== undefined);
});

const selectedGroupObjects = computed(() => {
  return selectedGroupIds.value
    .map((id) => groups.value.find((c) => c.id === id))
    .filter((c) => c !== undefined);
});

const selectedFriendSet = computed(() => new Set(selectedFriendIds.value));
const selectedGroupSet = computed(() => new Set(selectedGroupIds.value));

const isSelected = (id) => {
  if (activeTab.value === 'friends') {
    return selectedFriendSet.value.has(id);
  } else {
    return selectedGroupSet.value.has(id);
  }
};

const handleTagSelect = (tagName) => {
  currentFilter.value = tagName;
  filterDropdownOpen.value = false;
};

// Reset filter when tab changes
watch(activeTab, () => {
  currentFilter.value = '全部';
});

// Computed property to check if only groups are selected
const canSetGroupTags = computed(() => {
  return selectedGroupIds.value.length > 0 && selectedFriendIds.value.length === 0;
});
</script>

<template>
  <div class="h-screen overflow-hidden bg-slate-50 flex flex-col">
    <!-- 顶部导航 -->
    <NavBar />

    <!-- 顶部 Tab 栏 (Sticky) -->
    <div class="bg-white px-6 py-3 border-b border-slate-200 flex items-center justify-between flex-none z-10">
      <div class="flex space-x-2 bg-slate-100 p-1 rounded-lg">
        <button
          @click="activeTab = 'friends'"
          :class="`px-6 py-1.5 text-sm font-medium rounded-md transition-all ${
            activeTab === 'friends'
              ? 'bg-[#2563eb] text-white shadow-sm'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200'
          }`"
        >
          好友
        </button>
        <button
          @click="activeTab = 'groups'"
          :class="`px-6 py-1.5 text-sm font-medium rounded-md transition-all ${
            activeTab === 'groups'
              ? 'bg-[#2563eb] text-white shadow-sm'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200'
          }`"
        >
          群聊
        </button>
      </div>
      
      <!-- Right Side Actions -->
      <div class="relative">
        <button
          @click="filterDropdownOpen = !filterDropdownOpen"
          class="px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-700 hover:bg-slate-50 transition-colors flex items-center space-x-2"
        >
          <span>{{ currentFilter }}</span>
          <i class="ri-arrow-down-s-line text-base"></i>
        </button>
        <div v-if="filterDropdownOpen" class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 py-2 z-10">
           <button 
            v-for="tag in currentTags"
            :key="tag.name"
            @click="handleTagSelect(tag.name)"
            class="w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-50 transition-colors flex justify-between"
           >
            <span>{{ tag.name }}</span>
            <span v-if="tag.count !== null" class="text-slate-400 text-xs">({{ tag.count }})</span>
           </button>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="flex-1 flex overflow-hidden">
      <!-- 左侧列表 - 30% -->
      <div class="w-[320px] flex-none bg-white border-r border-slate-200 flex flex-col">
        <!-- 搜索框 -->
        <div class="p-4 pb-2">
          <div class="relative">
            <i class="ri-search-line absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-lg"></i>
            <input
              type="text"
              :placeholder="activeTab === 'friends' ? '搜索好友' : '搜索群聊'"
              v-model="searchQuery"
              class="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#2563eb]/20 focus:border-[#2563eb] transition-all"
            />
          </div>
        </div>

        <!-- 列表头 -->
        <div class="px-4 py-3 flex items-center justify-between">
          <span class="text-sm font-medium text-slate-700">
            {{ activeTab === 'friends' ? '好友' : '群聊' }} ({{ filteredList.length }})
          </span>
          <button
            @click="selectAll"
            class="text-sm text-[#2563eb] hover:text-[#1d4ed8] font-medium transition-colors"
          >
            全选
          </button>
        </div>

        <!-- 列表内容 -->
        <div class="flex-1 overflow-y-auto px-3 pb-4 space-y-2 custom-scrollbar">
          <div
            v-for="item in filteredList"
            :key="item.id"
            @click="toggleSelection(item.id)"
            :class="`p-3 rounded-xl border transition-all cursor-pointer flex items-center space-x-3 group relative ${
              isSelected(item.id)
                ? 'bg-[#2563eb]/5 border-[#2563eb]'
                : 'bg-white border-transparent shadow-sm border-slate-100 hover:border-[#2563eb]/30'
            }`"
          >
            <!-- New Badge -->
            <div v-if="item.isNew" class="absolute top-3 left-3 -ml-1 -mt-1 w-2.5 h-2.5 bg-yellow-400 rounded-full border-2 border-white z-10"></div>
            
            <!-- Avatar -->
            <div
              :class="`w-12 h-12 ${item.color} rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-sm flex-none`"
            >
              {{ item.avatar }}
            </div>
            
            <!-- Info -->
            <div class="flex-1 min-w-0">
              <div class="font-medium text-slate-800 text-base mb-0.5 truncate">{{ item.name }}</div>
              <div class="flex items-center space-x-2">
                <span class="text-xs text-slate-400 font-mono">{{ item.wechatId }}</span>
                <span v-if="item.tag" class="text-[10px] px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded border border-slate-200">{{ item.tag }}</span>
              </div>
            </div>

            <!-- Checkbox (Visual) -->
             <div :class="`w-5 h-5 rounded-full border flex items-center justify-center transition-colors ${
               isSelected(item.id) ? 'bg-[#2563eb] border-[#2563eb]' : 'border-slate-300'
             }`">
                <i v-if="isSelected(item.id)" class="ri-check-line text-white text-xs"></i>
             </div>
          </div>
        </div>
      </div>

      <!-- 右侧操作区域 -->
      <div class="flex-1 bg-[#F5F7FA] flex flex-col overflow-hidden p-4 space-y-4">
        <!-- 顶部：选择目标区域 (Card) -->
        <div class="flex-1 bg-white rounded-2xl shadow-sm border border-slate-200 flex flex-col min-h-0">
          <!-- 标题栏 (Fixed) -->
          <div class="flex-none px-6 py-4 border-b border-slate-100 flex items-center justify-between">
            <h2 class="text-lg font-bold text-slate-800">已选目标</h2>
            <div class="flex items-center space-x-3" v-if="selectedFriendIds.length > 0 || selectedGroupIds.length > 0">
               <button 
                 v-if="canSetGroupTags"
                 @click="isSetGroupTagsModalVisible = true"
                 class="px-3 py-1.5 text-xs font-medium text-[#2563eb] bg-[#2563eb]/10 rounded hover:bg-[#2563eb]/20 transition-colors"
               >
                 设置群标签
               </button>
               <button @click="clearSelection" class="text-xs text-red-500 hover:text-red-600 font-medium">
                 清空
               </button>
            </div>
          </div>

          <!-- 内容区域 (Scrollable) -->
          <div class="flex-1 overflow-y-auto p-6 custom-scrollbar">
            <!-- Empty State -->
            <div v-if="selectedFriendIds.length === 0 && selectedGroupIds.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 pb-20">
              <div class="w-20 h-20 bg-slate-100 rounded-2xl flex items-center justify-center mb-4">
                <i class="ri-file-list-3-line text-4xl text-slate-300"></i>
              </div>
              <p class="text-lg font-medium text-slate-500 mb-1">选择好友或群聊</p>
              <p class="text-sm text-slate-400">进行批量操作</p>
            </div>

            <div v-else class="space-y-6">
              <!-- 已选择的好友 -->
              <div v-if="selectedFriendIds.length > 0">
                <div class="flex items-center space-x-2 mb-3">
                  <span class="text-sm font-medium text-slate-600">已选择的好友</span>
                  <span class="bg-[#2563eb] text-white text-xs font-bold px-2 py-0.5 rounded-full">{{ selectedFriendIds.length }}</span>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
                  <div 
                    v-for="item in (selectedFriendObjects.length > 6 ? selectedFriendObjects.slice(0, 5) : selectedFriendObjects)" 
                    :key="item.id"
                    class="flex items-center p-2 bg-white border-l-4 border-l-[#2563eb] border-y border-r border-slate-200 rounded shadow-sm relative group"
                  >
                    <div class="flex-1 min-w-0 px-2">
                      <div class="text-sm font-medium text-slate-800 truncate">{{ item.name }}</div>
                      <div class="text-xs text-slate-400 truncate">{{ item.wechatId }}</div>
                    </div>
                    <button 
                      @click="deselectFriend(item.id)"
                      class="w-8 h-8 flex items-center justify-center text-slate-400 hover:text-red-500 transition-colors -mr-1 hover:bg-red-50 rounded-full"
                      aria-label="移除好友"
                    >
                      <i class="ri-close-line text-lg"></i>
                    </button>
                  </div>
                  <!-- Summary Card -->
                  <div 
                    v-if="selectedFriendObjects.length > 6"
                    class="flex items-center justify-center p-2 bg-slate-50 border border-dashed border-slate-300 rounded shadow-sm h-full"
                  >
                    <span class="text-slate-500 text-sm font-medium">...等{{ selectedFriendObjects.length }}人</span>
                  </div>
                </div>
              </div>

              <!-- 已选择的群聊 -->
              <div v-if="selectedGroupIds.length > 0">
                <div class="flex items-center space-x-2 mb-3">
                  <span class="text-sm font-medium text-slate-600">已选择的群聊</span>
                  <span class="bg-[#2563eb] text-white text-xs font-bold px-2 py-0.5 rounded-full">{{ selectedGroupIds.length }}</span>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
                  <div 
                    v-for="item in (selectedGroupObjects.length > 6 ? selectedGroupObjects.slice(0, 5) : selectedGroupObjects)" 
                    :key="item.id"
                    class="flex items-center p-2 bg-white border-l-4 border-l-[#10b981] border-y border-r border-slate-200 rounded shadow-sm relative group"
                  >
                    <div class="flex-1 min-w-0 px-2">
                      <div class="text-sm font-medium text-slate-800 truncate">{{ item.name }}</div>
                      <div class="text-xs text-slate-400 truncate">{{ item.wechatId }}</div>
                    </div>
                    <button 
                      @click="deselectGroup(item.id)"
                      class="w-8 h-8 flex items-center justify-center text-slate-400 hover:text-red-500 transition-colors -mr-1 hover:bg-red-50 rounded-full"
                      aria-label="移除群聊"
                    >
                      <i class="ri-close-line text-lg"></i>
                    </button>
                  </div>
                  <!-- Summary Card -->
                  <div 
                    v-if="selectedGroupObjects.length > 6"
                    class="flex items-center justify-center p-2 bg-slate-50 border border-dashed border-slate-300 rounded shadow-sm h-full"
                  >
                    <span class="text-slate-500 text-sm font-medium">...等{{ selectedGroupObjects.length }}个群</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 批量操作区域 (Fixed at bottom) -->
        <div class="flex-none bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
          <h3 class="text-lg font-semibold text-slate-800 mb-6">批量操作</h3>

          <div class="flex h-40 border border-slate-200 rounded-xl overflow-hidden divide-x divide-slate-200">
            <!-- 左侧：群发消息 -->
            <button class="flex-1 flex flex-col items-center justify-center bg-[#2563eb] text-white hover:bg-[#1d4ed8] transition-colors group">
              <div class="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <i class="ri-message-3-line text-3xl text-white"></i>
              </div>
              <span class="font-bold text-lg">群发消息</span>
            </button>

            <!-- 中间：功能按钮 -->
            <div class="w-64 flex flex-col p-4 space-y-3 justify-center bg-white">
              <button class="flex-1 flex items-center justify-center space-x-3 border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-colors bg-slate-50/50">
                <i class="ri-group-line text-lg text-slate-400"></i>
                <span class="text-slate-600 font-medium">批量拉群</span>
              </button>
              <button class="flex-1 flex items-center justify-center space-x-3 border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-colors bg-slate-50/50">
                <i class="ri-user-follow-line text-lg text-slate-400"></i>
                <span class="text-slate-600 font-medium">自动跟单</span>
              </button>
            </div>

            <!-- 右侧：设置 -->
            <button 
              @click="isSettingsModalVisible = true"
              class="w-40 flex flex-col items-center justify-center hover:bg-slate-50 transition-colors bg-slate-50/30 group"
            >
              <div class="mb-2 group-hover:rotate-90 transition-transform duration-500">
                <i class="ri-settings-3-line text-3xl text-slate-400"></i>
              </div>
              <span class="text-slate-600 font-medium">设置</span>
            </button>
          </div>
          
          <div class="mt-3 flex items-center text-slate-400 text-xs">
            <i class="ri-information-fill mr-1"></i>
            <span>部分操作仅支持好友</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 同步通讯录设置弹窗 -->
    <SyncSettingsModal 
      v-model="isSettingsModalVisible" 
      @sync-success="fetchData"
    />
    
    <!-- 设置群标签弹窗 -->
    <SetGroupTagsModal 
      v-model="isSetGroupTagsModalVisible"
      :selected-groups="selectedGroupObjects"
      @success="fetchData"
    />
  </div>
</template>

<style scoped>
/* 自定义滚动条样式 */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e2e8f0;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #cbd5e1;
}
</style>
