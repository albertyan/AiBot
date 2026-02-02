<script setup>
import { ref, computed, onMounted } from 'vue';
import { getGreetingConfig, saveGreetingConfig } from '../../api/setting';

const scriptGroups = ref([]);

const handleSaveConfig = async () => {
  try {
    const config = {
      greeting_config: scriptGroups.value.map(group => ({
        name: group.name,
        greetings: group.scripts
      }))
    };
    const res = await saveGreetingConfig(config);
    if (res.code === 200) {
      alert('保存成功');
    } else {
      alert('保存失败: ' + res.message);
    }
  } catch (error) {
    console.error('保存失败:', error);
    alert('保存失败');
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
  }
});
const showAddScriptGroup = ref(false);
const newScriptGroupName = ref('');

// 添加话术相关状态
const showAddScriptModal = ref(false);
const currentEditingGroupId = ref(null);
const scriptType = ref('text'); // text, file, agent
const scriptContent = ref('');
const selectedAgent = ref('');
const agentPrompt = ref('');
const selectedFile = ref(null);

// 模拟智能体列表
const agents = ref([
  { id: '1', name: '过敏', botId: '75326*****55496' },
]);

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
  scriptType.value = 'text';
  scriptContent.value = '';
  selectedAgent.value = '';
  agentPrompt.value = '';
  selectedFile.value = null;
  showAddScriptModal.value = true;
};

const closeAddScriptModal = () => {
  showAddScriptModal.value = false;
  currentEditingGroupId.value = null;
};

const handleSaveScript = () => {
  const group = scriptGroups.value.find(g => g.id === currentEditingGroupId.value);
  if (!group) return;

  let newScript = null;
  if (scriptType.value === 'text') {
    const content = scriptContent.value.trim();
    if (content) {
      newScript = { type: 'text', content };
    }
  } else if (scriptType.value === 'agent') {
    const agent = agents.value.find(a => a.id === selectedAgent.value);
    if (agent) {
      const prompt = agentPrompt.value.trim();
      newScript = { type: 'agent', content: `${agent.name} - ${prompt}`, agentId: agent.id, prompt };
    }
  } else if (scriptType.value === 'file') {
    if (selectedFile.value) {
      newScript = { type: 'file', content: selectedFile.value.name, file: selectedFile.value };
    }
  }

  if (newScript) {
    group.scripts.push(newScript);
    closeAddScriptModal();
  }
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
  }
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
          @click="handleSaveConfig"
          class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
        >
          保存配置
        </button>
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
    <div v-if="showAddScriptModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-lg mx-4">
        <div class="flex items-center justify-between p-6 border-b border-slate-200">
          <h2 class="text-xl font-semibold text-slate-800">添加话术内容</h2>
          <button
            @click="closeAddScriptModal"
            class="w-8 h-8 flex items-center justify-center hover:bg-slate-100 rounded-lg transition-colors"
          >
            <i class="ri-close-line text-xl text-slate-600"></i>
          </button>
        </div>
        
        <div class="p-6 space-y-6">
          <!-- 类型选择 -->
          <div class="flex items-center space-x-6">
            <label class="text-sm font-medium text-slate-700 w-12 text-right">类型</label>
            <div class="flex items-center space-x-6">
              <label class="flex items-center space-x-2 cursor-pointer">
                <input type="radio" v-model="scriptType" value="text" class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]">
                <span class="text-sm text-slate-700">文本</span>
              </label>
              <label class="flex items-center space-x-2 cursor-pointer">
                <input type="radio" v-model="scriptType" value="file" class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]">
                <span class="text-sm text-slate-700">文件</span>
              </label>
              <label class="flex items-center space-x-2 cursor-pointer">
                <input type="radio" v-model="scriptType" value="agent" class="w-4 h-4 text-[#4A90E2] border-slate-300 focus:ring-[#4A90E2]">
                <span class="text-sm text-slate-700">智能体</span>
              </label>
            </div>
          </div>

          <!-- 智能体配置 -->
          <template v-if="scriptType === 'agent'">
            <!-- 智能体选择 -->
            <div class="flex items-center space-x-6">
              <label class="text-sm font-medium text-slate-700 w-12 text-right">智能体</label>
              <div class="flex-1 relative">
                 <select
                  v-model="selectedAgent"
                  class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
                >
                  <option value="">请选择智能体</option>
                  <option v-for="agent in agents" :key="agent.id" :value="agent.id">{{ agent.name }}</option>
                </select>
                <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
              </div>
            </div>

            <!-- 提示词输入 -->
            <div class="flex items-start space-x-6">
              <label class="text-sm font-medium text-slate-700 w-12 text-right mt-2">提示词</label>
              <div class="flex-1 relative">
                <textarea
                  v-model="agentPrompt"
                  placeholder="请按要求生成话术"
                  rows="4"
                  maxlength="500"
                  class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
                ></textarea>
                <div class="absolute bottom-3 right-3 text-xs text-slate-400">
                  {{ agentPrompt.length }}/500
                </div>
              </div>
            </div>
          </template>

          <!-- 内容输入 (文本/文件) -->
          <div v-else class="flex items-start space-x-6">
            <label class="text-sm font-medium text-slate-700 w-12 text-right mt-2">内容</label>
            
            <div class="flex-1">
              <!-- 文本输入 -->
              <div v-if="scriptType === 'text'" class="relative">
                <textarea
                  v-model="scriptContent"
                  placeholder="请输入话术文本"
                  rows="4"
                  maxlength="300"
                  class="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent resize-none"
                ></textarea>
                <div class="absolute bottom-3 right-3 text-xs text-slate-400">
                  {{ scriptContent.length }}/300
                </div>
              </div>

              <!-- 文件上传 -->
              <div v-else-if="scriptType === 'file'" class="border border-slate-300 rounded-lg p-4">
                 <input type="file" @change="handleFileChange" class="block w-full text-sm text-slate-500
                    file:mr-4 file:py-2 file:px-4
                    file:rounded-full file:border-0
                    file:text-sm file:font-semibold
                    file:bg-blue-50 file:text-[#4A90E2]
                    hover:file:bg-blue-100
                  "/>
                  <div v-if="selectedFile" class="mt-2 text-sm text-slate-600">
                    已选文件: {{ selectedFile.name }}
                  </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-end space-x-3 p-6 border-t border-slate-200">
          <button
            @click="closeAddScriptModal"
            class="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 rounded-lg font-medium hover:bg-slate-50 transition-colors whitespace-nowrap"
          >
            取消
          </button>
          <button
            @click="handleSaveScript"
            class="px-6 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg font-medium transition-colors whitespace-nowrap"
          >
            确认
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
