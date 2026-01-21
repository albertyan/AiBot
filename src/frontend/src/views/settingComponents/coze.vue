<template>
  <a-form
    ref="formRef"
    name="custom-validation"
    :model="formState"
    :rules="rules"
    v-bind="layout"
  >
    <a-form-item has-feedback label="Coze Token" name="token">
      <a-input v-model:value="formState.token" type="password" placeholder="请输入Token"/>
      <div style="color: red;padding: 10px 0;">token有效期最多30天，已绑定2天如到期及时更换</div>
    </a-form-item>
    <a-form-item :wrapper-col="{ span: 20, offset: 4 }" style="text-align: right;">
      <a-button type="primary" html-type="submit" @click="onSubmit">保存设置</a-button>
    </a-form-item>
  </a-form>
</template>
<script setup>
import { reactive, ref, toRaw } from 'vue';
const layout = {
  labelCol: {
    style:{
      width: '100px'
    }
  },
  wrapperCol: {
    span: 16,
  },
};

const formRef = ref();
const formState = reactive({
  token: ''
});

// 规则校验 
const rules = {
  token: [
    {
      required: true,
      trigger: 'change',
      message: '请输入token'
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