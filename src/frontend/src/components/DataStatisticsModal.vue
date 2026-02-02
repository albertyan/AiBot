<script setup>
import { computed } from 'vue';
import { Modal } from 'ant-design-vue';

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

const stats = [
  { label: '今日会话', value: '128', change: '+12%', type: 'up', color: 'text-blue-600', bg: 'bg-blue-50', icon: 'ri-message-3-line' },
  { label: '自动回复', value: '1,024', change: '+5%', type: 'up', color: 'text-green-600', bg: 'bg-green-50', icon: 'ri-robot-line' },
  { label: '人工干预', value: '45', change: '-2%', type: 'down', color: 'text-orange-600', bg: 'bg-orange-50', icon: 'ri-user-voice-line' },
  { label: '平均响应', value: '1.2s', change: '-0.3s', type: 'up', color: 'text-purple-600', bg: 'bg-purple-50', icon: 'ri-timer-flash-line' }
];

const handleCancel = () => {
  visible.value = false;
};
</script>

<template>
  <Modal
    v-model:open="visible"
    title="数据统计"
    :width="700"
    :footer="null"
    @cancel="handleCancel"
    centered
    class="data-statistics-modal"
  >
    <div class="py-4">
      <!-- 核心指标卡片 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div v-for="(stat, index) in stats" :key="index" class="bg-slate-50 rounded-xl p-4 border border-slate-100">
          <div class="flex items-center justify-between mb-2">
            <div :class="`w-8 h-8 rounded-lg ${stat.bg} flex items-center justify-center ${stat.color}`">
              <i :class="stat.icon"></i>
            </div>
            <span :class="`text-xs font-medium ${stat.type === 'up' ? 'text-green-500' : 'text-red-500'}`">
              {{ stat.change }}
            </span>
          </div>
          <div class="text-2xl font-bold text-slate-800 mb-1">{{ stat.value }}</div>
          <div class="text-xs text-slate-500">{{ stat.label }}</div>
        </div>
      </div>

      <!-- 图表区域 (Mock) -->
      <div class="bg-white border border-slate-100 rounded-xl p-4 shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-bold text-slate-700">近7日回复趋势</h3>
          <div class="flex space-x-2">
            <span class="flex items-center text-xs text-slate-500">
              <span class="w-2 h-2 rounded-full bg-blue-500 mr-1"></span> 自动
            </span>
            <span class="flex items-center text-xs text-slate-500">
              <span class="w-2 h-2 rounded-full bg-orange-400 mr-1"></span> 人工
            </span>
          </div>
        </div>
        
        <div class="h-48 flex items-end justify-between space-x-2 px-2">
          <div v-for="i in 7" :key="i" class="flex-1 flex flex-col justify-end space-y-1 group cursor-pointer">
            <div class="w-full bg-orange-100 rounded-t relative group-hover:bg-orange-200 transition-colors" :style="`height: ${Math.random() * 30 + 10}%`"></div>
            <div class="w-full bg-blue-100 rounded-t relative group-hover:bg-blue-200 transition-colors" :style="`height: ${Math.random() * 50 + 30}%`"></div>
            <div class="text-[10px] text-center text-slate-400 mt-2">{{ i }}日</div>
          </div>
        </div>
      </div>
    </div>
  </Modal>
</template>
