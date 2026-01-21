<template>
  <a-layout id="components-layout-setting">
    <a-layout-sider
      theme="light"
      width="120px"
    >
      <div class="logo">
        配置导航
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="light" mode="vertical">
        <a-menu-item key="1">
          <a href="#ai1" class="nav-text">AI接入设置</a>
        </a-menu-item>
        <a-menu-item key="2">
          <a href="#ai2" class="nav-text">智能体管理</a>
        </a-menu-item>
        <a-menu-item key="3">
          <a href="#ai3" class="nav-text">朋友圈评论</a>
        </a-menu-item>
        <a-menu-item key="4">
          <a href="#ai4" class="nav-text">话术组配置</a>
        </a-menu-item>
        <a-menu-item key="5">
          <a href="#ai5" class="nav-text">聊天配置</a>
        </a-menu-item>
        <a-menu-item key="6">
          <a href="#ai6" class="nav-text">预警配置</a>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-content :style="{ margin: '10px 10px 0', overflow: 'auto' }">
        <div :style="{ padding: '10px 20px', background: '#fff', minHeight: '360px' }">
            <a name="ai1"></a>
            <a-card title="AI接入设置" style="width: 100%">
                <p>Coze设置</p>
                <coze></coze>
            </a-card>
            <a name="ai2"></a>
            <cozeList></cozeList>
            <a name="ai3"></a>
            <a-card title="朋友圈评论设置" style="width: 100%">
                <fpl></fpl>
            </a-card>
            <a name="ai4"></a>
            <a-card title="打招呼话术配置" style="width: 100%">
                 <hs></hs>
            </a-card>
            <a name="ai5"></a>
            <a-card title="聊天配置" style="width: 100%">
                 <chat></chat>
            </a-card>
            <a name="ai6"></a>
            <a-card title="预警邮箱配置" style="width: 100%">
                 <email></email>
            </a-card>
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script setup>
import { ref } from 'vue';
import coze from '@/views/settingComponents/coze.vue'
import cozeList from '@/views/settingComponents/cozeList.vue'
import fpl from '@/views/settingComponents/fpl.vue'
import hs from '@/views/settingComponents/hs.vue'
import chat from '@/views/settingComponents/chat.vue'
import email from '@/views/settingComponents/email.vue'
const selectedKeys = ref(['1']);
 
</script>
<style scoped>
#components-layout-setting{
    height: 100%;
}
#components-layout-setting .logo {
  height: 32px;
  margin: 16px 16px 0px;
  font-size: 16px;
  color: #2e2e2e;
  text-align: left;
  font-weight: bold;
}

.site-layout-sub-header-background {
  background: #fff;
}

.site-layout-background {
  background: #fff;
}

[data-theme='dark'] .site-layout-sub-header-background {
  background: #141414;
}
</style>