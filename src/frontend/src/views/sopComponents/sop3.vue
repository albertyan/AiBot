<template>
    <a-card title="自动通过好友配置" style="width: 100%">
      <a-alert style="margin-bottom: 10px;"  message='开启后7点-24点执行，其他时间不执行' type="info" show-icon />
       <a-form
            ref="formRef"
            name="custom-validation"
            :model="formState"
            :rules="rules"
            v-bind="layout"
        >
            <a-form-item has-feedback label="每日通过上限" name="a1">
            <a-input-number v-model:value="formState.a1" :min="1" :max="100000" placeholder="请输入每日通过上限" style="width: 100%"/>
            </a-form-item>
            <a-form-item has-feedback label="检查间隔(分钟)" name="a2">
            <a-input-number v-model:value="formState.a2" :min="1" :max="100000" placeholder="请输入检查间隔(分钟)" style="width: 100%"/>
            </a-form-item>
            <a-form-item has-feedback label="单次最大处理" name="a3">
            <a-input-number v-model:value="formState.a3" :min="1" :max="100000" placeholder="请输入单次最大处理" style="width: 100%"/>
            </a-form-item>
            <a-form-item has-feedback label="到达上次位置" name="prevWz">
                <a-select
                ref="select"
                v-model:value="formState.prevWz"
                style="width: 100%"
                :options="prevWzList"
                allow-clear 
                placeholder="请选择到达上次位置"
                ></a-select>
            </a-form-item>
            <a-form-item has-feedback label="打招呼话术" name="modes">
                <a-select
                ref="select"
                v-model:value="formState.modes"
                style="width: 100%"
                :options="modesList"
                allow-clear 
                placeholder="请选择打招呼话术"
                ></a-select>
            </a-form-item>
            <a-form-item has-feedback label="好友标签" name="ai">
                <a-input v-model:value="formState.token" type="text" placeholder="请输入好友标签"/> 
            </a-form-item>
            
            <a-form-item :wrapper-col="{ span: 24, offset: '100px' }" style="text-align: right;">
                <a-switch checked-children="关闭任务" un-checked-children="开启任务" /> 
            </a-form-item>
        </a-form>          
    </a-card>
</template>
<script setup>
import { reactive, ref, toRaw } from 'vue';
const layout = {
  labelCol: {
    style: {
        width: '120px',
    }
  },
  wrapperCol: {
    span: 16
  },
};

const formRef = ref();
const formState = reactive({
  a1: '',
  a2: '',
  modes: undefined,
  ai: undefined,
  md: ''
});
// 互动模式列表
const modesList = ref([
  {
    value: '0',
    label: '点赞&&评论',
  },
  {
    value: '1',
    label: '分享',
  }
]);
// 智能体列表
const aiList = ref([]);
// 规则校验 
const rules = {
  a1: [
    {
      required: true,
      trigger: 'change',
      message: '请输入总评论条数限制'
    },
  ],
  a2: [
    {
      required: true,
      trigger: 'change',
      message: '请输入单好友评论次数'
    },
  ],
  modes: [
    {
      required: true,
      trigger: 'change',
      message: '请选择互动模式'
    },
  ],
  ai: [
    {
      required: true,
      trigger: 'change',
      message: '请选择智能体'
    },
  ]
};

// 提交数据
const onSubmit = () => {
  formRef.value
    .validate()
    .then(() => {
        console.log('values', formState, toRaw(formState));
    })
    .catch(error => {
        console.log('error', error);
    });
};
</script>