<script setup>
import { ref, computed, watch } from 'vue';
import { Modal } from 'ant-design-vue';
import { getFriendTags } from '../api/custom';

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  initialSelectedTags: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:open', 'confirm']);

const visible = computed({
  get: () => props.open,
  set: (val) => emit('update:open', val)
});

const tags = ref([]);
const loading = ref(false);
const localSelectedTags = ref([]);

const fetchTags = async () => {
  loading.value = true;
  try {
    const res = await getFriendTags();
    if (res.code === 200) {
      tags.value = res.data;
    }
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

watch(() => props.open, (val) => {
  if (val) {
    localSelectedTags.value = [...props.initialSelectedTags];
    fetchTags();
  }
});

const toggleTag = (tagName) => {
  if (localSelectedTags.value.includes(tagName)) {
    localSelectedTags.value = localSelectedTags.value.filter(t => t !== tagName);
  } else {
    localSelectedTags.value.push(tagName);
  }
};

const handleReset = () => {
  localSelectedTags.value = [];
};

const handleConfirm = () => {
  emit('confirm', localSelectedTags.value);
  visible.value = false;
};
</script>

<template>
  <Modal
    v-model:open="visible"
    title="选择标签"
    :footer="null"
    width="500px"
    centered
    :destroyOnClose="true"
  >
    <div class="py-4">
      <div v-if="loading" class="text-center py-8 text-slate-500 flex flex-col items-center">
        <i class="ri-loader-4-line animate-spin text-2xl mb-2"></i>
        <span>加载中...</span>
      </div>
      <div v-else class="space-y-3 max-h-[400px] overflow-y-auto px-1">
        <div
          v-for="tag in tags"
          :key="tag.tag"
          class="flex items-center justify-between p-3 border border-slate-200 rounded-lg hover:bg-slate-50 cursor-pointer transition-colors select-none"
          @click="toggleTag(tag.tag)"
          :class="{'border-[#5B6EE1] bg-blue-50/30': localSelectedTags.includes(tag.tag)}"
        >
          <div class="flex items-center space-x-3">
            <div
              class="w-5 h-5 rounded border flex items-center justify-center transition-colors"
              :class="localSelectedTags.includes(tag.tag) ? 'bg-[#5B6EE1] border-[#5B6EE1]' : 'border-slate-300 bg-white'"
            >
              <i v-if="localSelectedTags.includes(tag.tag)" class="ri-check-line text-white text-xs"></i>
            </div>
            <span class="text-slate-700 font-medium">{{ tag.tag }}</span>
          </div>
          <span class="text-slate-400 text-sm">({{ tag.contact_count }})</span>
        </div>
        <div v-if="tags.length === 0 && !loading" class="text-center text-slate-400 py-8">
          <i class="ri-inbox-line text-3xl mb-2 block"></i>
          暂无标签数据
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
      <button
        @click="handleReset"
        class="px-6 py-2 bg-[#FF7875] hover:bg-[#FF4D4F] text-white rounded-lg text-sm font-medium transition-colors"
      >
        重置
      </button>
      <div class="flex items-center space-x-3">
        <button
          @click="visible = false"
          class="px-6 py-2 border border-slate-300 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors"
        >
          取消
        </button>
        <button
          @click="handleConfirm"
          class="px-6 py-2 bg-[#5B6EE1] hover:bg-[#4A5DD0] text-white rounded-lg text-sm font-medium transition-colors"
        >
          确定
        </button>
      </div>
    </div>
  </Modal>
</template>
