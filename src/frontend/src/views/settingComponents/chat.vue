<template>
    <div class="chat-setting">
        <p>聊天记录保存本地data文件夹</p>
        <div>
            <span>自动保存聊天记录</span>
            <a-switch v-model:checked="state.checked1" checked-children="开启" un-checked-children="关闭" />
        </div>
        <div>
            <span>AI回复携带上下文(单聊)</span>
            <a-switch v-model:checked="state.checked2" checked-children="开启" un-checked-children="关闭" />
        </div>
    </div>
</template>
<script setup>
import { reactive } from 'vue';
const state = reactive({
  checked1: false,
  checked2: false
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
</style>