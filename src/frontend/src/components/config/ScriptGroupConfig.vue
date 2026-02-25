<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { message } from 'ant-design-vue';
import { getGreetingConfig, saveGreetingConfig, getAgents } from '../../api/setting';
import AddScriptModal from './AddScriptModal.vue';

const scriptGroups = ref([]);
const isInitializing = ref(true);

const saveConfig = async () => {
  if (isInitializing.value) return;

  try {
    const config = {
      greeting_config: scriptGroups.value.map(group => ({
        name: group.name,
        greetings: group.scripts
      }))
    };
    const res = await saveGreetingConfig(config);
    if (res.code === 200) {
      message.success('配置已保存');
    } else {
      message.error('保存失败: ' + res.msg);
    }
  } catch (error) {
    console.error('保存失败:', error);
    message.error('保存失败');
  }
};

onMounted(async () => {
  try {
    const res = await getGreetingConfig();
    if (res.code === 200 && res.data) {
      scriptGroups.value = res.data.map((group, index) => ({
        id: String(index + 1),
        name: group.name,
        scripts: group.greetings || []
      }));
    }
  } catch (error) {
    console.error('获取话术配置失败:', error);
    message.error('获取话术配置失败');
  }

  // 获取智能体列表
  try {
    const agentsRes = await getAgents();
    if (agentsRes.code === 200 && agentsRes.data && agentsRes.data.agents) {
      agents.value = agentsRes.data.agents;
    }
  } catch (error) {
    console.error('获取智能体列表失败:', error);
  } finally {
    setTimeout(() => {
      isInitializing.value = false;
    }, 100);
  }
});

watch(scriptGroups, () => {
  saveConfig();
}, { deep: true });

const showAddScriptGroup = ref(false);
const newScriptGroupName = ref('');

// 添加话术相关状态
const showAddScriptModal = ref(false);
const currentEditingGroupId = ref(null);

// 智能体列表
const agents = ref([]);

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

const openAddScriptModal = (groupId) => {
  currentEditingGroupId.value = groupId;
  showAddScriptModal.value = true;
};

const handleAddScript = (newScript) => {
  const group = scriptGroups.value.find(g => g.id === currentEditingGroupId.value);
  if (group && newScript) {
    group.scripts.push(newScript);
  }
  // Modal will close itself via v-model binding updates
};

const removeScript = (group, index) => {
  if (group && group.scripts) {
    group.scripts.splice(index, 1);
  }
};

const removeScriptGroup = (index) => {
  scriptGroups.value.splice(index, 1);
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-slate-800">话术组配置（可配合智能体）</h1>
      <div class="space-x-3">
        <button
          @click="showAddScriptGroup = true"
          class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
        >
          添加话术组
        </button>
      </div>
    </div>

    <!-- 话术组列表 -->
    <div class="space-y-4">
      <div v-for="(group, groupIndex) in scriptGroups" :key="group.id" class="bg-white rounded-lg shadow-sm p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-slate-800">{{ group.name }}</h3>
          <button 
            @click="removeScriptGroup(groupIndex)"
            class="w-8 h-8 flex items-center justify-center text-red-500 hover:bg-red-50 rounded-lg transition-colors"
            title="删除话术组"
          >
            <i class="ri-delete-bin-line"></i>
          </button>
        </div>
        <div class="space-y-3">
          <div v-for="(script, index) in group.scripts" :key="index" class="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors group">
            <div class="flex items-center space-x-3 overflow-hidden">
              <!-- 类型标签 -->
              <span v-if="script.type === 'file'" class="flex-shrink-0 px-2.5 py-1 text-xs font-medium text-orange-600 bg-orange-100 rounded-md border border-orange-200">文件</span>
              <span v-else-if="script.type === 'text'" class="flex-shrink-0 px-2.5 py-1 text-xs font-medium text-green-600 bg-green-100 rounded-md border border-green-200">文本</span>
              <span v-else-if="script.type === 'agent'" class="flex-shrink-0 px-2.5 py-1 text-xs font-medium text-slate-600 bg-slate-200 rounded-md border border-slate-300">智能体</span>
              <!-- 内容 -->
              <p class="text-sm text-slate-700 truncate select-all">{{ script.content }}</p>
            </div>
            
            <button 
              @click.stop="removeScript(group, index)"
              class="w-8 h-8 flex items-center justify-center text-white bg-red-400 hover:bg-red-500 rounded-full transition-colors flex-shrink-0 opacity-0 group-hover:opacity-100 focus:opacity-100 cursor-pointer"
              title="删除"
            >
              <i class="ri-delete-bin-line text-sm"></i>
            </button>
          </div>
        </div>
        <button 
          @click="openAddScriptModal(group.id)"
          class="w-full mt-4 px-4 py-2 border-2 border-dashed border-slate-300 hover:border-[#4A90E2] text-slate-600 hover:text-[#4A90E2] rounded-lg text-sm font-medium transition-colors"
        >
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

    <!-- 添加话术内容弹窗 -->
    <AddScriptModal
      v-model="showAddScriptModal"
      :agents="agents"
      @submit="handleAddScript"
    />
  </div>
</template>
