<script setup>
import { ref } from 'vue';
import { Modal, Checkbox, TimePicker, InputNumber, Select } from 'ant-design-vue';
import dayjs from 'dayjs';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const syncSettings = ref({
  account: ['albertyanm','yanming'],
  syncItems: ['groups'],
  syncFrequency: 7,
  startTime: dayjs('02:00', 'HH:mm'),
  endTime: dayjs('04:00', 'HH:mm'),
  isEnabled: false
});

const accountOptions = ref([
  {
    label: 'albertyanm',
    value: 'albertyanm'
  },
  {
    label: 'yanming',
    value: 'yanming'
  }
]);

const handleCancel = () => {
  emit('update:modelValue', false);
};
</script>

<template>
  <Modal
    :open="modelValue"
    title="同步通讯录"
    :footer="null"
    :width="500"
    centered
    @cancel="handleCancel"
  >
    <div class="space-y-6 pt-4">
      <!-- 提示信息 -->
      <div class="space-y-3">
        <div class="bg-slate-50 text-slate-500 px-4 py-3 rounded-lg flex items-start space-x-3">
          <i class="ri-information-fill text-lg mt-0.5"></i>
          <span class="text-sm">所有微信通讯录数据均保存本地，绝不会上传服务器</span>
        </div>
        <div class="bg-orange-50 text-orange-600 px-4 py-3 rounded-lg flex items-start space-x-3">
          <i class="ri-error-warning-fill text-lg mt-0.5"></i>
          <span class="text-sm">建议开启夜间同步，3-7天同步一次好友列表</span>
        </div>
      </div>

      <!-- 手动同步 -->
      <div class="border border-slate-200 rounded-xl overflow-hidden">
        <div class="bg-slate-50 px-4 py-2 border-b border-slate-200 font-medium text-slate-700">手动同步</div>
        <div class="p-6 space-y-4">
          <div class="flex items-center">
            <span class="w-16 text-slate-600">账号：</span>
            <div class="flex-1">
              <Select
                v-model="syncSettings.account"
                :options="accountOptions"
                class="w-full"
                placeholder="请选择账号"
              />
            </div>
          </div>
          <div class="flex justify-center space-x-4 pt-2">
            <button class="px-6 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg transition-colors shadow-sm text-sm">
              同步好友
            </button>
            <button class="px-6 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg transition-colors shadow-sm text-sm">
              同步群聊
            </button>
          </div>
        </div>
      </div>

      <!-- 自动同步 -->
      <div class="border border-slate-200 rounded-xl overflow-hidden">
        <div class="bg-slate-50 px-4 py-2 border-b border-slate-200 font-medium text-slate-700">自动同步</div>
        <div class="p-6 space-y-5">
          <div class="flex items-center">
            <span class="w-20 text-slate-600">同步项：</span>
            <Checkbox.Group v-model="syncSettings.syncItems">
              <Checkbox value="friends">好友</Checkbox>
              <Checkbox value="groups">群聊</Checkbox>
            </Checkbox.Group>
          </div>
          
          <div class="flex items-center">
            <span class="w-20 text-slate-600">同步频率：</span>
            <span class="mr-2 text-slate-600">每隔</span>
            <InputNumber v-model="syncSettings.syncFrequency" :min="1" :max="30" class="w-20" />
            <span class="ml-2 text-slate-600">天</span>
          </div>

          <div class="flex items-center">
            <span class="w-20 text-slate-600">时间段：</span>
            <div class="flex items-center space-x-2">
              <TimePicker v-model="syncSettings.startTime" format="HH:mm" :allowClear="false" />
              <span class="text-slate-400">至</span>
              <TimePicker v-model="syncSettings.endTime" format="HH:mm" :allowClear="false" />
            </div>
          </div>

          <div class="pt-2 flex items-center justify-center border-t border-slate-100 mt-4">
            <div class="flex items-center space-x-3 mt-4">
              <span :class="!syncSettings.isEnabled ? 'text-[#4A90E2] font-medium' : 'text-slate-400'">已关闭</span>
              <div 
                @click="syncSettings.isEnabled = !syncSettings.isEnabled"
                :class="`w-12 h-6 rounded-full p-1 cursor-pointer transition-colors duration-300 ease-in-out ${syncSettings.isEnabled ? 'bg-[#4A90E2]' : 'bg-slate-200'}`"
              >
                <div :class="`w-4 h-4 bg-white rounded-full shadow-sm transform transition-transform duration-300 ${syncSettings.isEnabled ? 'translate-x-6' : 'translate-x-0'}`"></div>
              </div>
              <span :class="syncSettings.isEnabled ? 'text-[#4A90E2] font-medium' : 'text-slate-400'">已启用</span>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-center pt-2">
        <button 
          @click="handleCancel"
          class="px-8 py-2 border border-slate-300 rounded-lg text-slate-600 hover:bg-slate-50 transition-colors"
        >
          关闭
        </button>
      </div>
    </div>
  </Modal>
</template>
