<template>
    <div class="chat-setting">
        <p>出现异常会向指定邮箱发送预警消息</p>
        <a-form
            ref="formRef"
            name="custom-validation"
            :model="formState"
            v-bind="layout"
        >
                <a-form-item has-feedback label="邮箱地址" name="email">
                    <a-input v-model:value="formState.email" placeholder="请输入邮箱地址" />
                </a-form-item>
        </a-form>
        
    </div>
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
  email: ''
});
</script>
<style scoped>
.chat-setting > p{
    color: #999;
}
.chat-setting > div{
    display: flex;
    align-items: center;
    padding: 10px 0;
    justify-content: space-between;
}
.chat-setting > div > span {
    width: 100px;
    display: block;
    text-align: right;
    margin-right: 5px;
}
</style>