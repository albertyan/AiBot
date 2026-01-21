<template>
    <a-card title="主动推送群发任务" style="width: 100%">
         <template #extra>
            <a-button type="primary" size="small" @click="showModal">新建任务</a-button>
        </template>
        <!-- 任务列表 -->
         
        <!-- 添加弹框 -->
         <a-modal v-model:open="open" title="新建推送任务" @ok="handleOk" @cancel="resetForm">
            <a-form
                ref="formRef"
                :model="formState"
                :rules="rules"
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
                style="margin-top: 30px;"
            >
                <a-form-item ref="time" label="发送时间" name="time">
                    <a-radio-group v-model:value="formState.time">
                        <a-radio value="1">立即发送</a-radio>
                        <a-radio value="2">定时发送</a-radio>
                    </a-radio-group>
                </a-form-item>
                <a-form-item ref="tags" label="好友标签" name="tags">
                    <a-checkbox-group v-model:value="formState.tags">
                        <a-checkbox value="1" name="tags">未分组</a-checkbox>
                        <a-checkbox value="2" name="tags">同学</a-checkbox>
                        <a-checkbox value="3" name="tags">同事</a-checkbox>
                    </a-checkbox-group>
                </a-form-item>
                <a-form-item ref="hs" label="请选择话术组" name="hs">
                    <a-select
                    ref="select"
                    v-model:value="formState.hs"
                    style="width: 100%"
                    :options="hsList"
                    allow-clear 
                    placeholder="请选择话术组"
                    ></a-select>
                </a-form-item>
            </a-form>
        </a-modal>      
    </a-card>
</template>
<script setup>
import { onMounted, reactive, ref, toRaw, nextTick } from 'vue';
// 新增弹框
const open = ref(false);
const formRef = ref();
const labelCol = {
  span: 5,
};
const wrapperCol = {
  span: 18,
};
const formState = reactive({
  name: '',
  id: '',
  isDefault: false
});
const rules = {
  name: [
    {
      required: true,
      message: '请输入智能体名称',
      trigger: 'change',
    }
  ],
  id: [
    {
      required: true,
      message: '请输入BOT ID',
      trigger: 'change',
    },
  ]
};
// 话术组列表
const hsList = ref([
  {
    value: '0',
    label: '营销话语',
  },
  {
    value: '1',
    label: '客服回复',
  }
]);
const showModal = () => {
  open.value = true;
};
const resetForm = () => {
  formRef.value.resetFields();
};
// 提交
const handleOk = e => {
  console.log(e);
  formRef.value
    .validate()
    .then(() => {
        console.log('values', formState, toRaw(formState));
        open.value = false;
    })
    .catch(error => {
        console.log('error', error);
    });
};
</script>