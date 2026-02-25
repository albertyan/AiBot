<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  agents: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue', 'submit']);

const scriptType = ref('text'); // text, file, agent
const scriptContent = ref('');
const selectedAgent = ref('');
const agentPrompt = ref('请按要求生成话术');
const selectedFile = ref(null);

// Watch for modal opening to reset fields
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    resetFields();
  }
});

const resetFields = () => {
  scriptType.value = 'text';
  scriptContent.value = '';
  selectedAgent.value = '';
  agentPrompt.value = '请按要求生成话术';
  selectedFile.value = null;
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
  }
};

const close = () => {
  emit('update:modelValue', false);
};

const handleSubmit = () => {
  let newScript = null;
  if (scriptType.value === 'text') {
    const content = scriptContent.value.trim();
    if (content) {
      newScript = { type: 'text', content };
    }
  } else if (scriptType.value === 'agent') {
    const agent = props.agents.find(a => a.id === selectedAgent.value);
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
    emit('submit', newScript);
    close();
  }
};
</script>

<template>
  <div v-if="modelValue" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-lg mx-4">
      <div class="flex items-center justify-between p-6 border-b border-slate-200">
        <h2 class="text-xl font-semibold text-slate-800">添加话术内容</h2>
        <button
          @click="close"
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
                <option v-for="agent in props.agents" :key="agent.id" :value="agent.id">{{ agent.name }}</option>
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
          @click="close"
          class="px-6 py-2.5 bg-white border border-slate-300 text-slate-700 rounded-lg font-medium hover:bg-slate-50 transition-colors whitespace-nowrap"
        >
          取消
        </button>
        <button
          @click="handleSubmit"
          class="px-6 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg font-medium transition-colors whitespace-nowrap"
        >
          确认
        </button>
      </div>
    </div>
  </div>
</template>