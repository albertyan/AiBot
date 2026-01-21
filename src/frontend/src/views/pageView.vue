
<template>
  <a-layout class="layout" id="components-layout-demo-top">
    <a-layout-header style="padding-inline: 10px;">
      <div class="logo">
        webChatBot
      </div>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
        @click="clickItem"
      >
        <a-menu-item key="welcome">欢迎</a-menu-item>
        <a-menu-item key="ai">AI销冠</a-menu-item>
        <a-menu-item key="contacts">通讯录</a-menu-item>
        <a-menu-item key="sop">自动化SOP</a-menu-item>
        <a-menu-item key="setting">配置</a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content>
       <RouterView />
    </a-layout-content>
  </a-layout>
</template>
<script setup>
import { onMounted } from 'vue';
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()
const selectedKeys = ref([]);
onMounted(()=>{
  selectedKeys.value = [route.name]
})
// 跳转页面
function clickItem({key}){
    router.push({name: key})
}
</script>
<style scoped>
.site-layout-content {
  min-height: 280px;
  padding: 24px;
  background: #fff;
}
#components-layout-demo-top .logo {
  float: left;
  width: 120px;
  height: 31px;
  line-height: 31px;
  margin: 16px 24px 16px 0;
  text-align: center;
  color: #fff;
  font-size: 24px;
}
.ant-row-rtl #components-layout-demo-top .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

[data-theme='dark'] .site-layout-content {
  background: #141414;
}
</style>