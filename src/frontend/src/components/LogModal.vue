<script setup>
import { Modal } from 'ant-design-vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const handleClose = () => {
  emit('update:modelValue', false);
};
</script>

<template>
  <Modal
    :open="modelValue"
    @update:open="$emit('update:modelValue', $event)"
    title="自动回复日志"
    :footer="null"
    width="800px"
    @cancel="handleClose"
    :maskClosable="true"
    centered
    :bodyStyle="{ padding: '0 24px 24px 24px' }"
  >
    <div class="min-h-[300px] flex flex-col">
      <!-- Table Header -->
      <div class="grid grid-cols-5 gap-4 py-4 border-b border-slate-100 text-sm font-bold text-slate-400 text-center">
        <div>时间</div>
        <div>用户</div>
        <div>类型</div>
        <div>AI回复</div>
        <div>状态</div>
      </div>
      
      <!-- Empty State -->
      <div class="flex-1 flex items-center justify-center text-slate-400 text-sm">
        暂无数据
      </div>
    </div>
  </Modal>
</template>

<style scoped>
:deep(.ant-modal-title) {
  font-weight: 500;
  font-size: 1rem;
  color: #334155;
}
:deep(.ant-modal-header) {
  border-bottom: none;
  padding: 20px 24px 10px;
}
:deep(.ant-modal-close) {
  top: 16px;
  right: 16px;
}
</style>
