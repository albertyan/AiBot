<script setup>
import { ref, computed, onMounted } from 'vue';
import { Modal, message, Upload, Select } from 'ant-design-vue';

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:open', 'success']);

const visible = computed({
  get: () => props.open,
  set: (val) => emit('update:open', val)
});

const activeTab = ref('excel');
const fileList = ref([]);
const uploading = ref(false);
const agentList = ref([]);
const selectedAgent = ref(null);
const canSubmit = computed(() => {
  // 为什么分场景校验：不同导入方式对输入要求不同，统一校验能避免误触发
  if (activeTab.value === 'excel') {
    return fileList.value.length > 0;
  }
  if (activeTab.value === 'agent') {
    return !!selectedAgent.value;
  }
  if (activeTab.value === 'api') {
    return false; // API 导入未实现，避免误操作
  }
  return false;
});

const handleCancel = () => {
  visible.value = false;
  fileList.value = [];
  selectedAgent.value = null;
};

const handleUpload = async () => {
  // 为什么分支处理：不同导入方式调用后端接口不同，分支更清晰与可维护
  if (activeTab.value === 'excel') {
    if (fileList.value.length === 0) {
      message.warning('请先选择文件');
      return;
    }

    const formData = new FormData();
    formData.append('file', fileList.value[0].originFileObj);

    uploading.value = true;
    try {
      const response = await fetch('/api/autosop/upload_friend_list', {
        method: 'POST',
        body: formData
      });
      
      const result = await response.json();
      
      if (result.code === 200) {
        message.success('导入成功');
        emit('success', result.data);
        handleCancel();
      } else {
        message.error(result.msg || '导入失败');
      }
    } catch (error) {
      message.error('上传出错: ' + error.message);
    } finally {
      uploading.value = false;
    }
    return;
  }

  if (activeTab.value === 'agent') {
    // 为什么先占位提示：后端未提供智能体拉取接口，防止误导用户
    message.warning('智能体导入尚未接通后端，请先配置接口');
    return;
  }

  if (activeTab.value === 'api') {
    message.warning('API 导入功能开发中');
    return;
  }
};

const beforeUpload = (file) => {
  const isExcelOrCsv = 
    file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
    file.type === 'application/vnd.ms-excel' ||
    file.name.endsWith('.csv');
    
  if (!isExcelOrCsv) {
    message.error('只支持 xlsx, xls, csv 格式文件!');
    return Upload.LIST_IGNORE;
  }
  
  fileList.value = [file];
  return false; // 阻止自动上传
};

const handleRemove = () => {
  fileList.value = [];
};

onMounted(async () => {
  // 为什么使用后端 /api/agents：统一来源，避免前端硬编码智能体列表
  try {
    const res = await fetch('/api/agents');
    const data = await res.json();
    const list = Array.isArray(data?.agents) ? data.agents : [];
    agentList.value = list.map(a => ({ label: a, value: a }));
  } catch (e) {
    // 拉取失败不阻塞弹窗使用，用户可稍后重试
    agentList.value = [];
  }
});
</script>

<template>
  <Modal
    v-model:open="visible"
    title="导入微信号/手机号名单"
    :footer="null"
    width="600px"
    centered
    :destroyOnClose="true"
  >
    <div class="py-2">
      <!-- 顶部 Tab -->
      <div class="flex border-b border-slate-200 mb-6">
        <button
          @click="activeTab = 'excel'"
          class="px-6 py-3 text-sm font-medium transition-colors relative"
          :class="activeTab === 'excel' ? 'text-[#4A90E2]' : 'text-slate-600 hover:text-slate-800'"
        >
          Excel导入
          <div v-if="activeTab === 'excel'" class="absolute bottom-0 left-0 right-0 h-0.5 bg-[#4A90E2]"></div>
        </button>
        <button
          @click="activeTab = 'agent'"
          class="px-6 py-3 text-sm font-medium transition-colors relative"
          :class="activeTab === 'agent' ? 'text-[#4A90E2]' : 'text-slate-600 hover:text-slate-800'"
        >
          智能体导入
          <div v-if="activeTab === 'agent'" class="absolute bottom-0 left-0 right-0 h-0.5 bg-[#4A90E2]"></div>
        </button>
        <button
          @click="activeTab = 'api'"
          class="px-6 py-3 text-sm font-medium transition-colors relative"
          :class="activeTab === 'api' ? 'text-[#4A90E2]' : 'text-slate-600 hover:text-slate-800'"
        >
          API导入
          <div v-if="activeTab === 'api'" class="absolute bottom-0 left-0 right-0 h-0.5 bg-[#4A90E2]"></div>
        </button>
      </div>

      <!-- Excel 导入内容 -->
      <div v-if="activeTab === 'excel'" class="space-y-6">
        <!-- 提示信息 -->
        <div class="flex items-center justify-between bg-blue-50 border border-blue-100 rounded-lg p-4">
          <div class="flex items-center space-x-2">
            <i class="ri-information-fill text-[#4A90E2] text-lg"></i>
            <span class="text-sm text-slate-700">将名单录入到表格中，然后导入即可</span>
          </div>
          <button class="text-sm text-[#4A90E2] hover:text-[#357ABD] font-medium">
            复制模板下载地址
          </button>
        </div>

        <!-- 文件上传区域 -->
        <div class="py-4">
          <Upload
            :file-list="fileList"
            :before-upload="beforeUpload"
            @remove="handleRemove"
            accept=".xlsx,.xls,.csv"
            :max-count="1"
          >
            <button class="px-4 py-2 border border-slate-300 rounded hover:border-[#4A90E2] hover:text-[#4A90E2] transition-colors text-slate-600 text-sm flex items-center space-x-2">
              <span>选择文件</span>
            </button>
          </Upload>
          <div class="mt-2 text-xs text-slate-400">仅支持 xlsx、xls、csv 格式文件</div>
        </div>
      </div>

      <!-- 智能体 导入内容 -->
      <div v-else-if="activeTab === 'agent'" class="space-y-6">
        <!-- 提示信息 -->
        <div class="flex items-center bg-blue-50 border border-blue-100 rounded-lg p-4">
          <i class="ri-information-fill text-[#4A90E2] text-lg mr-2"></i>
          <span class="text-sm text-slate-700">通过智能体连接飞书获取名单数据</span>
        </div>
        <!-- 选择智能体 -->
        <div class="space-y-2">
          <div class="text-sm text-slate-600">选择智能体</div>
          <Select
            v-model:value="selectedAgent"
            :options="agentList"
            placeholder="请选择智能体"
            show-search
            style="width: 100%;"
          />
        </div>
      </div>

      <!-- API 导入占位 -->
      <div v-else class="py-12 text-center text-slate-400">
        功能开发中...
      </div>

      <!-- 底部按钮 -->
      <div class="flex items-center justify-end space-x-3 mt-8 pt-4 border-t border-slate-100">
        <button
          @click="handleCancel"
          class="px-6 py-2 border border-slate-300 text-slate-600 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors"
        >
          取消
        </button>
        <button
          @click="handleUpload"
          :disabled="uploading || !canSubmit"
          class="px-6 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
        >
          <i v-if="uploading" class="ri-loader-4-line animate-spin"></i>
          <span>立即上传</span>
        </button>
      </div>
    </div>
  </Modal>
</template>
