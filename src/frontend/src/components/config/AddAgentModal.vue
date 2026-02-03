<script setup>
import { ref, computed } from 'vue';
import { Modal, Select, Input, Switch, message } from 'ant-design-vue';

/**
 * 添加智能体弹窗
 * 为什么采用“平台→动态字段”的方案：
 * - 不同平台参数差异较大，用字段映射可以按平台灵活扩展而不破坏表单结构
 * - 将通用字段（名称、默认接待）与平台特有字段解耦，避免耦合导致维护成本上升
 */
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'confirm']);

// 平台选项：先支持常见平台，后续按您的要求扩展具体字段
const platformOptions = [
  { label: '字节 Coze', value: 'coze' },
  { label: 'Dify', value: 'dify' },
  { label: '腾讯元宝', value: 'yuanbao' },
  // { label: 'OpenAI', value: 'openai' },
  // { label: '阿里 通义千问', value: 'qwen' },
  
];

// 按平台映射所需字段；优先只放通用需求，具体差异将根据您的指引逐步补齐
// 设计原因：通过配置驱动显示，避免在模板中写大量 v-if 造成可读性下降
const platformFieldMap = {
  yuanbao: ['botId', 'token'],
  coze: ['botId'],
  openai: ['token'],
  qwen: ['token'],
  dify: ['apiKey'],
};

const form = ref({
  platform: 'coze',
  name: '',
  botId: '',
  token: '',
  apiKey: '',
  isDefault: false,
});

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

const currentFields = computed(() => platformFieldMap[form.value.platform] ?? []);

/**
 * 提交表单
 * 为什么在前端做校验：
 * - 交互即时反馈可以减少来回请求，提高体验
 * - 仅校验必要项，避免过度约束阻塞用户操作
 */
const handleSubmit = () => {
  if (!form.value.name.trim()) {
    message.warning('请输入智能体名称');
    return;
  }
  if (currentFields.value.includes('botId') && !form.value.botId.trim()) {
    message.warning('请输入 Bot ID');
    return;
  }
  if (currentFields.value.includes('token') && !form.value.token.trim()) {
    message.warning('请输入 Token');
    return;
  }
  if (currentFields.value.includes('apiKey') && !form.value.apiKey.trim()) {
    message.warning('请输入 API 秘钥');
    return;
  }
  emit('confirm', { ...form.value });
  visible.value = false;
  // 重置表单，原因：避免上一次填写内容影响下一次添加
  form.value = {
    platform: 'yuanbao',
    name: '',
    botId: '',
    token: '',
    apiKey: '',
    isDefault: false,
  };
};

const handleCancel = () => {
  visible.value = false;
};
</script>

<template>
  <Modal
    :open="visible"
    title="添加智能体"
    :footer="null"
    :width="520"
    centered
    @cancel="handleCancel"
  >
    <div class="space-y-4 pt-2">
      <!-- 平台选择 -->
      <div class="flex items-center">
        <span class="w-24 text-slate-700">平台</span>
        <div class="flex-1">
          <Select
            v-model:value="form.platform"
            :options="platformOptions"
            class="w-full"
            placeholder="请选择平台"
          />
        </div>
      </div>

      <!-- 智能体名称 -->
      <div class="flex items-center">
        <span class="w-24 text-slate-700"><span class="text-red-500 mr-1">*</span>智能体名称</span>
        <div class="flex-1">
          <Input v-model:value="form.name" placeholder="请输入智能体名称" />
        </div>
      </div>

      <!-- Bot ID（按平台显示） -->
      <div v-if="currentFields.includes('botId')" class="flex items-center">
        <span class="w-24 text-slate-700"><span class="text-red-500 mr-1">*</span>Bot ID</span>
        <div class="flex-1">
          <Input v-model:value="form.botId" placeholder="请输入 Bot ID" />
        </div>
      </div>

      <!-- Token（按平台显示） -->
      <div v-if="currentFields.includes('token')" class="flex items-center">
        <span class="w-24 text-slate-700">Token</span>
        <div class="flex-1">
          <Input v-model:value="form.token" placeholder="请输入秘钥字符串" />
        </div>
      </div>

      <!-- API Key（按平台显示） -->
      <div v-if="currentFields.includes('apiKey')" class="flex items-center">
        <span class="w-24 text-slate-700"><span class="text-red-500 mr-1">*</span>API 秘钥</span>
        <div class="flex-1">
          <Input v-model:value="form.apiKey" placeholder="请输入 API 秘钥" />
        </div>
      </div>

      <!-- 默认接待 -->
      <div class="flex items-center">
        <span class="w-24 text-slate-700">默认接待</span>
        <div class="flex-1">
          <Switch v-model:checked="form.isDefault" />
        </div>
      </div>

      <div class="flex justify-end pt-2">
        <button
          @click="handleCancel"
          class="px-5 py-2 border border-slate-300 rounded-lg text-slate-700 hover:bg-slate-50 transition-colors mr-2"
        >
          取消
        </button>
        <button
          @click="handleSubmit"
          class="px-5 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg transition-colors"
        >
          添加智能体
        </button>
      </div>
    </div>
  </Modal>
</template>
