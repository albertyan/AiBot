<script setup>
import { ref, computed, watch } from 'vue';
import { Modal, Input, message } from 'ant-design-vue';
import { setGroupTags } from '../api/custom';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  selectedGroups: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue', 'confirm', 'success']);

const tagName = ref('');
const maxLength = 10;
const isSubmitting = ref(false);

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

const groupNames = computed(() => {
  return props.selectedGroups.map(g => g.name).join('，');
});

const handleOk = async () => {
  if (!tagName.value) {
    message.warning('请输入标签名称');
    return;
  }
  
  if (isSubmitting.value) return;
  isSubmitting.value = true;
  
  try {
    const groupNamesList = props.selectedGroups.map(g => g.name);
    const res = await setGroupTags(groupNamesList, tagName.value);
    
    if (res.code === 200) {
      message.success(res.message || `已为 ${props.selectedGroups.length} 个群聊设置标签: ${tagName.value}`);
      emit('confirm', tagName.value);
      emit('success');
      visible.value = false;
      tagName.value = ''; // Reset
    } else {
      message.error(res.message || '设置群标签失败');
    }
  } catch (error) {
    message.error(error.message || '设置群标签发生错误');
  } finally {
    isSubmitting.value = false;
  }
};

const handleCancel = () => {
  visible.value = false;
  tagName.value = ''; // Reset
};

// Character count helper
const charCount = computed(() => tagName.value.length);
</script>

<template>
  <Modal
    v-model:open="visible"
    title="设置群标签"
    :width="600"
    :footer="null"
    @cancel="handleCancel"
    centered
  >
    <div class="pt-2 pb-6">
      <!-- 提示文本 -->
      <div class="mb-6 text-sm text-slate-500 leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-100">
        <p>批量设置群标签，以便绑定AI智能体进行回复</p>
        <p>如果群聊已绑定标签，重新设置会直接覆盖~</p>
      </div>

      <!-- 表单内容 -->
      <div class="space-y-6 px-2">
        <!-- 群聊列表 -->
        <div class="flex">
          <span class="w-12 text-sm font-medium text-slate-700 pt-0.5 flex-none">群聊：</span>
          <div class="text-sm text-slate-600 leading-relaxed break-all">
            {{ groupNames }}
          </div>
        </div>

        <!-- 标签输入 -->
        <div class="flex items-center">
          <span class="w-12 text-sm font-medium text-slate-700 flex-none">标签：</span>
          <div class="flex-1 relative">
            <Input
              v-model:value="tagName"
              placeholder="请输入标签（1-10个字符，支持中英文/数字）"
              :maxlength="maxLength"
              allow-clear
            />
            <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-slate-400">
              {{ charCount }} / {{ maxLength }}
            </span>
          </div>
        </div>
      </div>

      <!-- 底部按钮 -->
      <div class="flex justify-center space-x-4 mt-8">
        <button
          @click="handleCancel"
          class="px-8 py-2 border border-slate-200 rounded text-sm text-slate-600 hover:bg-slate-50 transition-colors"
        >
          取消
        </button>
        <button
          @click="handleOk"
          :disabled="isSubmitting"
          class="px-8 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded text-sm transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          <i v-if="isSubmitting" class="ri-loader-4-line animate-spin mr-1"></i>
          {{ isSubmitting ? '提交中...' : '确认' }}
        </button>
      </div>
    </div>
  </Modal>
</template>

<style scoped>
:deep(.ant-modal-content) {
  border-radius: 12px;
  padding: 24px;
}
:deep(.ant-modal-header) {
  margin-bottom: 0;
  border-bottom: none;
}
:deep(.ant-modal-title) {
  font-size: 18px;
  font-weight: 600;
  text-align: center;
}
:deep(.ant-input) {
  border-radius: 4px;
  padding-right: 50px; /* Space for character count */
}
</style>
