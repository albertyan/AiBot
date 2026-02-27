<script setup>
import { ref, computed, onMounted } from 'vue';
import { Modal, Input, Tooltip, message } from 'ant-design-vue';
import AiAssistantModal from './AiAssistantModal.vue';
import { getAiConfig, saveAiAgent, deleteAiAgent } from '../api/aisale';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

const assistants = ref([]);

const loadAssistants = async () => {
  try {
    const res = await getAiConfig();
    const staffList = res?.data?.config?.staffList;
    if (Array.isArray(staffList)) {
      assistants.value = staffList.map(item => ({
        ...item,
        tag: item.chatType === 'group' ? '群聊' : '单聊'
      }));
    } else {
      assistants.value = [];
    }
  } catch (error) {
    console.error(error);
    assistants.value = [];
  }
};

// Assistant Modal State
const isAssistantModalVisible = ref(false);
const currentAssistant = ref(null);

const handleAddAssistant = () => {
  currentAssistant.value = null;
  isAssistantModalVisible.value = true;
};

const handleEditAssistant = (assistant) => {
  currentAssistant.value = {
    id: assistant.id,
    name: assistant.name,
    chatType: assistant.chatType === 'group' ? 'group' : 'single',
    agentId: assistant.agentId,
    selectedTags: Array.isArray(assistant.selectedTags) ? assistant.selectedTags : []
  };
  isAssistantModalVisible.value = true;
};

const handleAssistantSave = async (data) => {
  try {
    const payload = {
      id: data?.id,
      name: data?.name,
      chatType: data?.chatType,
      agentId: data?.agentId,
      selectedTags: data?.selectedTags
    };
    const res = await saveAiAgent(payload);
    if (res?.code === 200) {
      message.success('保存成功');
      await loadAssistants();
    } else {
      message.error(res?.msg || '保存失败');
    }
  } catch (error) {
    console.error(error);
    message.error('保存失败');
  } finally {
    isAssistantModalVisible.value = false;
  }
};

const handleDeleteAssistant = (assistant) => {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除AI助理 "${assistant.name}" 吗？`,
    okText: '确认',
    cancelText: '取消',
    async onOk() {
      try {
        const res = await deleteAiAgent(assistant.id);
        if (res?.code === 200) {
          message.success('删除成功');
          await loadAssistants();
        } else {
          message.error(res?.msg || '删除失败');
        }
      } catch (error) {
        console.error(error);
        message.error('删除失败');
      }
    }
  });
};

// General Config State
const isGeneralConfigExpanded = ref(false);
const autoGreeting = ref(false);
const groupReplyAtOnly = ref(false);
const groupIgnoreList = ref('');
const whitelistEnabled = ref(false);
const whitelistText = ref('');
const identifyFile = ref(true);
const fileTypes = ref({
  word: false,
  pdf: true,
  excel: false,
  image: true
});
const fileDirectory = ref('D:\\WeChat Files\\albertyan');

// Filter Words
const filterWords = ref(['退订', '投诉', '人工']);
const showAddWordInput = ref(false);
const newFilterWord = ref('');

const handleAddFilterWord = () => {
  if (newFilterWord.value.trim()) {
    if (!filterWords.value.includes(newFilterWord.value.trim())) {
      filterWords.value.push(newFilterWord.value.trim());
    }
    newFilterWord.value = '';
    showAddWordInput.value = false;
  }
};

const removeFilterWord = (word) => {
  filterWords.value = filterWords.value.filter(w => w !== word);
};

const handleCancel = () => {
  visible.value = false;
};

const handleSave = () => {
  // Logic to save configuration
  visible.value = false;
};

onMounted(() => {
  loadAssistants();
});
</script>

<template>
  <Modal
    v-model:open="visible"
    title="AI助理配置"
    :width="600"
    :footer="null"
    @cancel="handleCancel"
    centered
    class="ai-config-modal"
  >
    <div class="flex flex-col items-center justify-center mb-6 mt-[-10px]">
      <span class="text-xs text-slate-400">配置修改后，立即生效！</span>
    </div>

    <div class="space-y-4">
      <!-- AI助理配置 Card -->
      <div class="border border-slate-200 rounded-xl p-5 bg-white shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-slate-800 text-base">AI助理配置</h3>
          <button 
            @click="handleAddAssistant"
            class="px-3 py-1 bg-[#2563eb] text-white text-xs rounded-md hover:bg-[#1d4ed8] transition-colors flex items-center space-x-1"
          >
            <i class="ri-add-line"></i>
            <span>AI助理</span>
          </button>
        </div>
        
        <p class="text-xs text-slate-400 mb-4">配置不同场景下的AI助理</p>

        <div class="space-y-3">
          <div 
            v-for="assistant in assistants" 
            :key="assistant.id"
            class="flex items-center justify-between p-3 border border-slate-100 rounded-lg hover:bg-slate-50 transition-colors group"
          >
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-[#2563eb]">
                <i class="ri-robot-2-line text-xl"></i>
              </div>
              <div>
                <div class="font-medium text-slate-800 text-sm">{{ assistant.name }}</div>
                <div class="inline-block px-1.5 py-0.5 bg-green-100 text-green-600 text-[10px] rounded border border-green-200 mt-0.5">
                  {{ assistant.tag }}
                </div>
              </div>
            </div>

            <div class="flex items-center space-x-4">
              <!-- Toggle Switch -->
              <div class="flex flex-col items-end">
                <div 
                  class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors cursor-pointer"
                  :class="assistant.enabled ? 'bg-[#2563eb]' : 'bg-slate-200'"
                  @click="assistant.enabled = !assistant.enabled"
                >
                  <span
                    class="inline-block h-4 w-4 transform rounded-full bg-white transition transition-transform"
                    :class="assistant.enabled ? 'translate-x-6' : 'translate-x-1'"
                  />
                </div>
              </div>
              
              <div class="flex items-center space-x-2 text-slate-400">
                <button 
                  @click="handleEditAssistant(assistant)"
                  class="p-1 hover:text-[#2563eb] transition-colors"
                >
                  <i class="ri-edit-line text-lg"></i>
                </button>
                <button 
                  @click="handleDeleteAssistant(assistant)"
                  class="p-1 hover:text-red-500 transition-colors"
                >
                  <i class="ri-delete-bin-line text-lg"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 通用配置 Card -->
      <div 
        class="border border-slate-200 rounded-xl bg-white shadow-sm transition-all duration-300"
      >
        <!-- Header (Click to toggle) -->
        <div 
          @click="isGeneralConfigExpanded = !isGeneralConfigExpanded"
          class="p-5 flex items-center justify-between cursor-pointer hover:bg-slate-50 rounded-xl"
          :class="{ 'rounded-b-none border-b border-slate-100': isGeneralConfigExpanded }"
        >
          <span class="font-bold text-slate-800 text-base">通用配置 <span class="text-sm font-normal text-slate-500">（修改完后记得点保存）</span></span>
          <i class="ri-arrow-down-s-line text-slate-400 text-xl transition-transform duration-300" :class="{ 'rotate-180': isGeneralConfigExpanded }"></i>
        </div>

        <!-- Expanded Content -->
        <div v-show="isGeneralConfigExpanded" class="p-6 space-y-8">
          
          <!-- 自动打招呼 -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="font-bold text-slate-700">自动打招呼</div>
              <div 
                class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors cursor-pointer"
                :class="autoGreeting ? 'bg-[#2563eb]' : 'bg-slate-200'"
                @click="autoGreeting = !autoGreeting"
              >
                <span
                  class="inline-block h-4 w-4 transform rounded-full bg-white transition transition-transform"
                  :class="autoGreeting ? 'translate-x-6' : 'translate-x-1'"
                />
              </div>
            </div>
            <div class="text-sm text-slate-400">当检测到对方通过了你的好友申请后，则自动发送话术组内容</div>
            <div class="h-px bg-slate-100 w-full mt-4"></div>
          </div>

          <!-- 群聊配置 -->
          <div class="space-y-4">
            <div>
              <div class="font-bold text-slate-700 mb-2">群聊配置</div>
              <div class="text-sm text-slate-400">设置群聊中的回复行为和忽略规则</div>
            </div>

            <label class="flex items-center space-x-2 cursor-pointer w-fit">
              <input type="checkbox" v-model="groupReplyAtOnly" class="w-4 h-4 text-[#2563eb] rounded border-slate-300 focus:ring-[#2563eb]">
              <span class="text-sm text-slate-600">群聊被@时才回复</span>
            </label>

            <div class="space-y-1">
              <input 
                v-model="groupIgnoreList"
                type="text" 
                placeholder="录入群聊同事名单，会自动忽略群中同事的消息(仅微信3.9使用)"
                class="w-full px-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-[#2563eb] placeholder-slate-300"
              >
              <div class="text-xs text-slate-400">多个同事名单用双斜杠"//"分隔开，输入后自动保存。</div>
            </div>
             <div class="h-px bg-slate-100 w-full mt-4"></div>
          </div>

          <!-- 白名单 -->
          <div class="space-y-3">
             <div class="flex items-center justify-between">
              <div class="font-bold text-slate-700">白名单</div>
              <div 
                class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors cursor-pointer"
                :class="whitelistEnabled ? 'bg-[#2563eb]' : 'bg-slate-200'"
                @click="whitelistEnabled = !whitelistEnabled"
              >
                <span
                  class="inline-block h-4 w-4 transform rounded-full bg-white transition transition-transform"
                  :class="whitelistEnabled ? 'translate-x-6' : 'translate-x-1'"
                />
              </div>
            </div>
            <div class="text-sm text-slate-400">开启后，仅回复白名单中的好友或群聊</div>
            
            <div class="space-y-1" v-if="whitelistEnabled">
              <textarea 
                v-model="whitelistText"
                rows="3"
                placeholder="输入好友昵称或群名并用双斜杠&quot;//&quot;隔开，如：张三//测试一群"
                class="w-full px-4 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-[#2563eb] placeholder-slate-300 resize-none"
              ></textarea>
              <div class="text-xs text-slate-400">输入好友昵称或群名并用双斜杠"//"隔开，如：张三//测试一群</div>
            </div>

            <div class="h-px bg-slate-100 w-full mt-4"></div>
          </div>

          <!-- 回复过滤词 -->
          <div class="space-y-3">
             <div class="flex items-center justify-between">
              <div class="font-bold text-slate-700">回复过滤词</div>
              <button 
                v-if="!showAddWordInput"
                @click="showAddWordInput = true"
                class="px-3 py-1.5 bg-[#2563eb] text-white text-xs font-medium rounded hover:bg-[#1d4ed8] transition-colors"
              >
                添加过滤词
              </button>
            </div>
            <div class="text-sm text-slate-400">AI生成的回复中包含过滤词（全匹配）时，将不会发送给用户</div>
            
            <!-- Filter Words List -->
            <div class="flex flex-wrap gap-2 mt-2">
              <div 
                v-for="word in filterWords" 
                :key="word"
                class="px-3 py-1 bg-red-50 text-red-600 rounded-lg text-sm border border-red-100 flex items-center space-x-2"
              >
                <span>{{ word }}</span>
                <i 
                  @click="removeFilterWord(word)"
                  class="ri-close-line cursor-pointer hover:text-red-800"
                ></i>
              </div>

              <!-- Input for new word -->
              <div v-if="showAddWordInput" class="flex items-center space-x-2">
                <input
                  v-model="newFilterWord"
                  @keyup.enter="handleAddFilterWord"
                  @blur="handleAddFilterWord"
                  type="text"
                  placeholder="输入过滤词"
                  class="w-32 px-2 py-1 border border-slate-300 rounded text-sm focus:outline-none focus:border-[#2563eb]"
                  ref="inputRef"
                  autofocus
                />
              </div>
            </div>

            <div class="h-px bg-slate-100 w-full mt-4"></div>
          </div>

          <!-- 识别文件 -->
          <div class="space-y-6">
             <div class="flex items-center justify-between">
              <div class="font-bold text-slate-700">识别文件</div>
              <div 
                class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors cursor-pointer"
                :class="identifyFile ? 'bg-[#2563eb]' : 'bg-slate-200'"
                @click="identifyFile = !identifyFile"
              >
                <span
                  class="inline-block h-4 w-4 transform rounded-full bg-white transition transition-transform"
                  :class="identifyFile ? 'translate-x-6' : 'translate-x-1'"
                />
              </div>
            </div>
            <div class="text-sm text-slate-400 -mt-2">开启后可以识别消息的文件并上传到Coze</div>

            <div class="bg-slate-100 rounded-lg p-5 space-y-5">
               <div>
                 <div class="text-sm font-bold text-slate-700 mb-3">文件类型</div>
                 <div class="flex items-center space-x-6">
                   <label class="flex items-center space-x-2 cursor-pointer">
                     <input type="checkbox" v-model="fileTypes.word" class="w-4 h-4 text-[#2563eb] rounded border-slate-300 focus:ring-[#2563eb]">
                     <span class="text-sm text-slate-600">Word</span>
                   </label>
                   <label class="flex items-center space-x-2 cursor-pointer">
                     <input type="checkbox" v-model="fileTypes.pdf" class="w-4 h-4 text-[#2563eb] rounded border-slate-300 focus:ring-[#2563eb]">
                     <span class="text-sm text-slate-600 text-[#2563eb]">PDF</span>
                   </label>
                   <label class="flex items-center space-x-2 cursor-pointer">
                     <input type="checkbox" v-model="fileTypes.excel" class="w-4 h-4 text-[#2563eb] rounded border-slate-300 focus:ring-[#2563eb]">
                     <span class="text-sm text-slate-600">Excel</span>
                   </label>
                   <label class="flex items-center space-x-2 cursor-pointer">
                     <input type="checkbox" v-model="fileTypes.image" class="w-4 h-4 text-[#2563eb] rounded border-slate-300 focus:ring-[#2563eb]">
                     <span class="text-sm text-slate-600 text-[#2563eb]">图片</span>
                   </label>
                 </div>
               </div>

               <div>
                 <div class="flex items-center space-x-2 mb-2">
                   <span class="text-sm font-bold text-slate-700">文件目录</span>
                   <Tooltip>
                     <template #title>
                       示例：D:\ProgramData\tencent_cache\WeChat Files\ABC123，注意！！最后一个目录一定是当前登录的微信号
                     </template>
                     <button 
                       class="w-5 h-5 rounded-full bg-slate-800 text-white flex items-center justify-center text-[10px] font-bold cursor-help hover:bg-slate-700 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500"
                       aria-label="查看帮助"
                     >
                       ?
                     </button>
                   </Tooltip>
                 </div>
                 <input 
                    v-model="fileDirectory"
                    type="text"
                    class="w-full bg-white border border-[#2563eb] rounded px-3 py-2 text-sm text-slate-600 focus:outline-none focus:ring-1 focus:ring-[#2563eb]"
                 />
               </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- AI Assistant Edit/Add Modal -->
    <AiAssistantModal 
      v-model="isAssistantModalVisible" 
      :assistant-data="currentAssistant"
      @save="handleAssistantSave"
    />

    <!-- Footer Buttons -->
    <div class="flex justify-end space-x-3 mt-8">
      <button 
        @click="handleCancel"
        class="px-5 py-2 border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50 hover:text-slate-800 transition-colors text-sm font-medium"
      >
        取消
      </button>
      <button 
        @click="handleSave"
        class="px-5 py-2 bg-[#2563eb] text-white rounded-lg hover:bg-[#1d4ed8] shadow-sm hover:shadow transition-colors text-sm font-medium"
      >
        保存配置
      </button>
    </div>
  </Modal>
</template>

<style scoped>
/* Optional: Customize modal header if needed */
:deep(.ant-modal-title) {
  text-align: center;
  font-weight: 700;
  font-size: 1.125rem;
}
:deep(.ant-modal-close) {
  top: 16px;
  right: 16px;
}
</style>
