<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { Modal, Input, Radio, Select, Checkbox, Button, message } from 'ant-design-vue';
import { getAgents } from '../api/setting';
import { getFriendTags } from '../api/custom';
import { get_current_user } from '../stores/user';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  assistantData: {
    type: Object,
    default: () => null
  }
});

const emit = defineEmits(['update:modelValue', 'save']);

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

// Form State
const formData = ref({
  name: '',
  chatType: 'single', // single or group
  agentId: undefined,
  selectedTags: [] // Array of tag strings
});

const agentOptions = ref([]);

const loadAgents = async () => {
  try {
    const res = await getAgents();
    const list = res?.data?.agents;
    if (Array.isArray(list)) {
      agentOptions.value = list.map(a => ({
        label: a.name,
        value: a.id
      })).filter(o => o.label && o.value);
    } else {
      agentOptions.value = [];
    }
  } catch (error) {
    console.error(error);
    agentOptions.value = [];
    message.error('获取智能体列表失败');
  }
};

const availableTags = ref([
  { label: '未分组', value: '未分组' },
]);

const loadTags = async () => {
  try {
    const user = get_current_user();
    if (!user) return;
    const wxNumber = user.wxNumber;
    if (!wxNumber) return;

    const res = await getFriendTags(wxNumber);
    const tags = res?.data;
      if (Array.isArray(tags)) {
        availableTags.value = [
          { label: '未分组', value: '未分组' },
          ...tags.map(t => ({
            label: t.tag,
            value: t.tag
          }))
        ];
      }
  } catch (error) {
    console.error(error);
    message.error('获取好友标签失败');
  }
};

// Initialize form when opening
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (agentOptions.value.length === 0) {
      loadAgents();
    }
    loadTags();
    if (props.assistantData) {
      // Edit mode
      formData.value = {
        name: props.assistantData.name || '',
        chatType: props.assistantData.chatType || props.assistantData.scope || 'single',
        agentId: props.assistantData.agentId,
        selectedTags: props.assistantData.selectedTags
          ? [...props.assistantData.selectedTags]
          : (props.assistantData.tags ? [...props.assistantData.tags] : [])
      };
    } else {
      // Create mode - reset
      formData.value = {
        name: '',
        chatType: 'single',
        agentId: undefined,
        selectedTags: []
      };
    }
  }
});

onMounted(() => {
  loadAgents();
});

const handleResetTags = () => {
  formData.value.selectedTags = [];
};

const handleCancel = () => {
  visible.value = false;
};

const handleSave = () => {
  if (!formData.value.name) {
    message.warning('请输入员工名称');
    return;
  }
  if (!formData.value.agentId) {
    message.warning('请选择智能体');
    return;
  }
  
  emit('save', { ...formData.value, id: props.assistantData?.id });
  visible.value = false;
};
</script>

<template>
  <Modal
    v-model:open="visible"
    :title="props.assistantData ? '编辑AI助理' : '新增AI助理'"
    :width="500"
    :footer="null"
    @cancel="handleCancel"
    centered
    class="ai-assistant-modal"
  >
    <div class="py-4 space-y-5">
      
      <!-- 员工名称 -->
      <div class="border border-slate-100 rounded-lg p-4 shadow-sm bg-white">
        <div class="flex items-center mb-3">
          <div class="w-1 h-4 bg-[#2563eb] rounded-full mr-2"></div>
          <span class="font-bold text-slate-700">*员工名称</span>
        </div>
        <Input 
          v-model:value="formData.name" 
          placeholder="请输入员工名称" 
          class="w-full"
        />
      </div>

      <!-- 回复范围 -->
      <div class="border border-slate-100 rounded-lg p-4 shadow-sm bg-white">
        <div class="flex items-center mb-3">
          <div class="w-1 h-4 bg-[#2563eb] rounded-full mr-2"></div>
          <span class="font-bold text-slate-700">*回复范围</span>
        </div>
        <Radio.Group v-model:value="formData.chatType" class="w-full">
          <div class="flex space-x-8">
            <Radio value="single">
              <span class="text-[#2563eb] font-medium" :class="formData.chatType === 'single' ? 'text-[#2563eb]' : 'text-slate-600'">单聊</span>
            </Radio>
            <Radio value="group">
              <span class="font-medium" :class="formData.chatType === 'group' ? 'text-[#2563eb]' : 'text-slate-600'">群聊</span>
            </Radio>
          </div>
        </Radio.Group>
      </div>

      <!-- 选择智能体 -->
      <div class="border border-slate-100 rounded-lg p-4 shadow-sm bg-white">
        <div class="flex items-center mb-3">
          <div class="w-1 h-4 bg-[#2563eb] rounded-full mr-2"></div>
          <span class="font-bold text-slate-700">*选择智能体</span>
        </div>
        <Select
          v-model:value="formData.agentId"
          placeholder="请选择智能体"
          class="w-full"
          :options="agentOptions"
        />
      </div>

      <!-- 好友标签 -->
      <div class="border border-slate-100 rounded-lg p-4 shadow-sm bg-white">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center">
            <div class="w-1 h-4 bg-[#2563eb] rounded-full mr-2"></div>
            <span class="font-bold text-slate-700">好友标签</span>
          </div>
          <Button 
            type="primary" 
            size="small" 
            class="bg-orange-400 border-none hover:bg-orange-500 text-xs px-2 h-7"
            @click="handleResetTags"
          >
            重置标签
          </Button>
        </div>
        <div class="text-xs text-slate-400 mb-3 ml-3">不选会作为兜底AI助理，回复所有好友</div>
        
        <div class="border border-slate-100 rounded p-3 min-h-[50px]">
          <Checkbox.Group v-model:value="formData.selectedTags" class="w-full">
            <div class="grid grid-cols-3 gap-2">
              <Checkbox 
                v-for="tag in availableTags" 
                :key="tag.value" 
                :value="tag.value"
              >
                <span :class="formData.selectedTags.includes(tag.value) ? 'text-[#2563eb]' : 'text-slate-600'">{{ tag.label }}</span>
              </Checkbox>
            </div>
          </Checkbox.Group>
        </div>
      </div>

    </div>

    <!-- Footer Buttons -->
    <div class="flex justify-end space-x-3 mt-4 pt-2 border-t border-slate-100">
      <Button @click="handleCancel" class="w-20">取消</Button>
      <Button type="primary" @click="handleSave" class="w-20 bg-[#2563eb]">确认</Button>
    </div>
  </Modal>
</template>

<style scoped>
:deep(.ant-modal-content) {
  border-radius: 12px;
  padding: 0;
  overflow: hidden;
}
:deep(.ant-modal-header) {
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}
:deep(.ant-modal-body) {
  padding: 24px;
  background-color: #fafafa; /* Slight gray background for body to make white cards pop */
}
:deep(.ant-input), :deep(.ant-select-selector) {
  border-radius: 6px;
}
</style>
