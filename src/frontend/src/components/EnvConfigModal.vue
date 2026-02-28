<template>
  <a-modal
    :open="open"
    :footer="null"
    :closable="true"
    :maskClosable="false"
    width="500px"
    class="env-config-modal"
    @cancel="handleCancel"
  >
    <div class="content-wrapper" v-if="currentView === 'config'">
      <div class="header">
        <span class="warning-icon">!</span>
        <span class="title">设备环境异常~</span>
      </div>
      
      <p class="description">
        您使用的是4.1版本微信，需要进行设备环境配置。点击下方按钮，会自动执行以下配置：
      </p>
      
      <div class="steps-container">
        <div class="step-item" v-for="(step, index) in steps" :key="index">
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-text">{{ step }}</div>
        </div>
      </div>
      
      <div class="action-area">
        <a-button 
          type="primary" 
          shape="round" 
          size="large" 
          :loading="loading"
          block
          class="start-btn"
          @click="startConfig"
        >
          {{ loading ? '配置中...' : '开始自动配置' }}
        </a-button>
      </div>
    </div>

    <div class="content-wrapper success-wrapper" v-else>
      <div class="success-header">
        <h2 class="success-title">自动配置完成！</h2>
      </div>
      
      <div class="success-content">
        <p class="success-main-text">已完成配置（先不要关闭讲述人模式）</p>
        <p class="success-sub-text">请登录微信后，点击下方按钮启动应用</p>
      </div>
      
      <div class="action-area">
        <a-button 
          type="primary" 
          shape="round" 
          size="large" 
          block
          class="launch-btn"
          @click="handleSuccessLaunch"
        >
          启动应用
        </a-button>
      </div>
    </div>
  </a-modal>
</template>

<script setup>
import { ref, watch } from 'vue';
import { message } from 'ant-design-vue';
import { autoConfigureEnv } from '../api/launch';

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:open', 'success']);

const loading = ref(false);
const currentView = ref('config'); // 'config' or 'success'

// Reset view when modal is reopened
watch(() => props.open, (newVal) => {
  if (newVal) {
    currentView.value = 'config';
  }
});

const steps = [
  '退出当前微信程序',
  '配置电脑环境变量',
  '启动“讲述人”模式并运行 10 秒',
  '重新启动微信程序'
];

const handleCancel = () => {
  if (loading.value) return;
  emit('update:open', false);
};

const startConfig = async () => {
  loading.value = true;
  try {
    const res = await autoConfigureEnv();
    if (res.code === 200) {
      // Switch to success view instead of closing immediately
      currentView.value = 'success';
    } else {
      message.error(res.msg || '配置失败，请重试');
    }
  } catch (error) {
    message.error(error.message || '请求失败');
  } finally {
    loading.value = false;
  }
};

const handleSuccessLaunch = () => {
  emit('success');
  emit('update:open', false);
};
</script>

<style scoped>
.content-wrapper {
  padding: 20px 10px;
  text-align: center;
}

.success-wrapper {
  padding-top: 10px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.success-header {
  margin-bottom: 30px;
  text-align: left;
}

.success-title {
  font-size: 24px;
  font-weight: bold;
  color: #000;
  margin: 0;
}

.success-content {
  text-align: left;
  margin-bottom: 40px;
}

.success-main-text {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.success-sub-text {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.warning-icon {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  border-radius: 50%;
  background-color: #faad14;
  color: white;
  font-weight: bold;
  margin-right: 10px;
  font-size: 16px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  color: #faad14;
}

.description {
  color: #666;
  margin-bottom: 30px;
  text-align: left;
  line-height: 1.6;
}

.steps-container {
  background-color: #f5f8ff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
}

.step-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.step-item:last-child {
  margin-bottom: 0;
}

.step-number {
  width: 24px;
  height: 24px;
  line-height: 24px;
  border-radius: 50%;
  background-color: #1890ff;
  color: white;
  font-size: 14px;
  font-weight: bold;
  margin-right: 15px;
  flex-shrink: 0;
}

.step-text {
  color: #333;
  font-size: 15px;
  text-align: left;
}

.action-area {
  margin-top: 20px;
  padding: 0 20px;
}

.launch-btn {
  height: 45px;
  font-size: 16px;
  font-weight: bold;
  background-color: #1890ff;
  border-color: #1890ff;
  box-shadow: 0 4px 10px rgba(24, 144, 255, 0.3);
}

.start-btn {
  height: 45px;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 10px rgba(24, 144, 255, 0.3);
}
</style>