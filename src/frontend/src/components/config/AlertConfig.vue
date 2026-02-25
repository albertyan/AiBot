<script setup>
import { ref, onMounted, watch } from 'vue';
import { message } from 'ant-design-vue';
import { sendTestAlertEmail, getAlertSettings, saveAlertSettings } from '../../api/setting';

const alertEmail = ref('');
const enableEmailAlert = ref(true);
const alertFrequency = ref('immediate');
const sending = ref(false);
const saving = ref(false);
const loading = ref(false);
const isInitializing = ref(true);

const fetchSettings = async () => {
  loading.value = true;
  try {
    const res = await getAlertSettings();
    if (res.code === 200 && res.data && res.data.alert_settings) {
      const settings = res.data.alert_settings;
      alertEmail.value = settings.email || '';
      alertFrequency.value = settings.frequency || 'immediate';
      // 如果后端没有返回 enabled 字段，默认为 true
      enableEmailAlert.value = settings.enabled !== undefined ? settings.enabled : true;
    }
  } catch (error) {
    console.error('获取预警配置失败:', error);
    message.error('获取预警配置失败');
  } finally {
    loading.value = false;
    setTimeout(() => {
      isInitializing.value = false;
    }, 100);
  }
};

const saveSettings = async () => {
  if (isInitializing.value) return;

  if (enableEmailAlert.value && !alertEmail.value) {
    // 自动保存时，如果为空可能不提示更友好，或者仅在启用且为空时提示
    // message.warning('启用预警时，邮箱不能为空');
    return;
  }

  if (enableEmailAlert.value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(alertEmail.value)) {
      // message.warning('请输入有效的邮箱地址');
      return;
    }
  }

  saving.value = true;
  try {
    const config = {
      alert_settings: {
        email: alertEmail.value,
        frequency: alertFrequency.value,
        enabled: enableEmailAlert.value
      }
    };
    const res = await saveAlertSettings(config);
    if (res.code === 200) {
      message.success('配置已保存');
    } else {
      message.error(res.msg || '保存配置失败');
    }
  } catch (error) {
    console.error('保存预警配置失败:', error);
    message.error('保存配置失败');
  } finally {
    saving.value = false;
  }
};

watch(
  [alertEmail, enableEmailAlert, alertFrequency],
  () => {
    saveSettings();
  }
);

onMounted(() => {
  fetchSettings();
});

const handleSendTestEmail = async () => {
  if (!alertEmail.value) {
    message.warning('请先输入预警邮箱');
    return;
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(alertEmail.value)) {
    message.warning('请输入有效的邮箱地址');
    return;
  }

  sending.value = true;
  try {
    await sendTestAlertEmail(alertEmail.value);
    message.success('测试邮件发送成功');
  } catch (error) {
    console.error(error);
    message.error(error.message || '发送测试邮件失败');
  } finally {
    sending.value = false;
  }
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-slate-800">预警配置</h1>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <!-- 提示信息 -->
      <div class="flex items-start space-x-3 bg-orange-50 border border-orange-200 rounded-lg p-4 mb-6">
        <i class="ri-alarm-warning-fill text-orange-500 text-xl mt-0.5"></i>
        <div class="text-sm text-orange-700">
          当自动回复挂掉时会发送邮件提醒，请确保邮箱地址正确
        </div>
      </div>

      <div class="space-y-6">
        <!-- 启用邮件预警 -->
        <div>
          <div class="flex items-center justify-between mb-4">
            <label class="text-sm font-medium text-slate-700">启用邮件预警</label>
            <div class="flex items-center space-x-2">
              <span class="text-sm text-slate-600">{{ enableEmailAlert ? '已启用' : '已禁用' }}</span>
              <button
                @click="enableEmailAlert = !enableEmailAlert"
                class="relative w-12 h-6 rounded-full transition-colors"
                :class="enableEmailAlert ? 'bg-[#4A90E2]' : 'bg-slate-300'"
              >
                <span
                  class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform"
                  :class="enableEmailAlert ? 'translate-x-6' : ''"
                ></span>
              </button>
            </div>
          </div>
        </div>

        <!-- 预警邮箱 -->
        <div>
          <label class="block text-sm font-medium text-slate-700 mb-2">预警邮箱</label>
          <input
            type="email"
            v-model="alertEmail"
            placeholder="请输入接收预警通知的邮箱地址"
            class="w-full px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent"
            :disabled="!enableEmailAlert"
          />
          <p class="text-xs text-slate-500 mt-2">系统异常时将向此邮箱发送预警通知</p>
        </div>

        <!-- 预警频率 -->
        <!-- <div>
          <label class="block text-sm font-medium text-slate-700 mb-3">预警频率</label>
          <div class="relative">
            <select
              v-model="alertFrequency"
              class="w-full px-4 py-2.5 bg-white border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90E2] focus:border-transparent appearance-none cursor-pointer"
              :disabled="!enableEmailAlert"
            >
              <option value="immediate">立即通知</option>
              <option value="5min">每5分钟</option>
              <option value="15min">每15分钟</option>
              <option value="30min">每30分钟</option>
              <option value="1hour">每小时</option>
            </select>
            <i class="ri-arrow-down-s-line absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none"></i>
          </div>
          <p class="text-xs text-slate-500 mt-2">设置预警通知的发送频率</p>
        </div> -->

        <!-- 预警条件 -->
        <!-- <div class="pt-4 border-t border-slate-200">
          <h3 class="text-base font-semibold text-slate-800 mb-4">预警条件</h3>
          <div class="space-y-3">
            <label class="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
              <input
                type="checkbox"
                checked
                class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                :disabled="!enableEmailAlert"
              />
              <div class="flex-1">
                <div class="text-sm font-medium text-slate-700">AI回复服务停止</div>
                <div class="text-xs text-slate-500">当AI自动回复服务停止运行时发送预警</div>
              </div>
            </label>
            <label class="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
              <input
                type="checkbox"
                checked
                class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                :disabled="!enableEmailAlert"
              />
              <div class="flex-1">
                <div class="text-sm font-medium text-slate-700">API连接失败</div>
                <div class="text-xs text-slate-500">当外部API连接失败时发送预警</div>
              </div>
            </label>
            <label class="flex items-center space-x-3 p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-slate-100 transition-colors">
              <input
                type="checkbox"
                class="w-4 h-4 text-[#4A90E2] border-slate-300 rounded focus:ring-[#4A90E2]"
                :disabled="!enableEmailAlert"
              />
              <div class="flex-1">
                <div class="text-sm font-medium text-slate-700">系统资源异常</div>
                <div class="text-xs text-slate-500">当系统资源占用过高时发送预警</div>
              </div>
            </label>
          </div>
        </div> -->

        <!-- 测试预警 -->
        <div class="flex items-center space-x-3 pt-4">
          <button 
            @click="handleSendTestEmail"
            class="px-6 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg font-medium transition-colors whitespace-nowrap"
            :disabled="!enableEmailAlert || sending"
          >
            {{ sending ? '发送中...' : '发送测试邮件' }}
          </button>
          <span class="text-sm text-slate-500">测试预警邮件是否能正常发送</span>
        </div>
      </div>
    </div>
  </div>
</template>
