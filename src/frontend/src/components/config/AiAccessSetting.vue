<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { getDifySettings, saveDifySettings, getCozeSettings, setCozeSettings } from '../../api/setting';
import { isValidUrl } from '../../utils/validators';

const cozeToken = ref('');
const difyUrl = ref('');
const cozeTokenDays = ref(0);
const loading = ref(false);
const showCozeToken = ref(false);

const loadSettings = async () => {
  try {
    const [difyRes, cozeRes] = await Promise.all([
      getDifySettings(),
      getCozeSettings()
    ]);
    
    if (difyRes.code === 200 && difyRes.data) {
      difyUrl.value = difyRes.data.baseUrl || '';
    }
    
    if (cozeRes.code === 200 && cozeRes.data) {
      cozeToken.value = cozeRes.data.token || '';
      cozeTokenDays.value = cozeRes.data.last_update_time || 0;
    }
  } catch (error) {
    console.error('Failed to load settings:', error);
    message.error('获取配置失败');
  }
};

const handleSaveCoze = async () => {
  if (!cozeToken.value.trim()) {
    message.warning('请输入 Coze Token');
    return;
  }
  
  loading.value = true;
  try {
    const res = await setCozeSettings(cozeToken.value);
    if (res.code === 200) {
      message.success('Coze 配置保存成功');
      // 重新加载以更新天数
      const cozeRes = await getCozeSettings();
      if (cozeRes.code === 200 && cozeRes.data) {
        cozeTokenDays.value = cozeRes.data.last_update_time || 0;
      }
    } else {
      message.error(res.msg || '保存失败');
    }
  } catch (error) {
    message.error('保存失败');
  } finally {
    loading.value = false;
  }
};

const handleSaveDify = async () => {
  if (!difyUrl.value.trim()) {
    message.warning('请输入 Dify 服务器地址');
    return;
  }
  
  // URL 校验：确保以 http:// 或 https:// 开头
  if (!isValidUrl(difyUrl.value)) {
    message.warning('请输入有效的服务器地址 (需以 http:// 或 https:// 开头)');
    return;
  }
  
  loading.value = true;
  try {
    const res = await saveDifySettings(difyUrl.value);
    if (res.code === 200) {
      message.success('Dify 配置保存成功');
    } else {
      message.error(res.msg || '保存失败');
    }
  } catch (error) {
    message.error('保存失败');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadSettings();
});
</script>

<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-slate-800">AI接入配置</h1>

    <!-- Coze平台 -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
            <i class="ri-robot-line text-white text-lg"></i>
          </div>
          <h2 class="text-lg font-semibold text-slate-800">Coze平台</h2>
        </div>
        <button 
          @click="handleSaveCoze"
          :disabled="loading"
          class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
        >
          {{ loading ? '保存中...' : '保存配置' }}
        </button>
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">Coze Token</label>
          <div class="relative">
            <input
              :type="showCozeToken ? 'text' : 'password'"
              v-model="cozeToken"
              placeholder="请输入Coze Token"
              class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            />
            <button 
              @click="showCozeToken = !showCozeToken"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
            >
              <i :class="showCozeToken ? 'ri-eye-off-line' : 'ri-eye-line'"></i>
            </button>
          </div>
          <p v-if="cozeToken" class="text-xs text-orange-500 mt-2">token已使用 {{ cozeTokenDays }} 天，如果永久期限，记得到期及时更换</p>
        </div>
      </div>
    </div>

    <!-- Dify平台 -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
            <i class="ri-robot-2-line text-white text-lg"></i>
          </div>
          <h2 class="text-lg font-semibold text-slate-800">Dify平台</h2>
        </div>
        <button 
          @click="handleSaveDify"
          :disabled="loading"
          class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
        >
          {{ loading ? '保存中...' : '保存配置' }}
        </button>
      </div>

      <div>
        <label class="block text-sm font-medium text-slate-700 mb-2">服务器地址</label>
        <input
          type="text"
          v-model="difyUrl"
          placeholder="如果是本地则默认可输入：http://localhost/v1"
          class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
        />
      </div>
    </div>
  </div>
</template>
