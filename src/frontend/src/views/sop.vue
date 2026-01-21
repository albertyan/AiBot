<template>
  <a-layout id="components-layout-sop">
    <a-layout-sider
      theme="light"
      v-model:collapsed="state.collapsed" 
      :trigger="null" 
      collapsible
    >
      <div class="logo">
        功能
      </div>
      <a-menu 
      v-model:selectedKeys="state.selectedKeys" 
      theme="light" 
      mode="inline"
      :items="items"
      >
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-content :style="{ margin: '10px 10px 0', overflow: 'auto' }">
        <a-flex gap="middle">
            <div :style="{ padding: '0', minHeight: '360px', width:'50%' }">
                <sop1 v-if="state.selectedKeys[0]==='1'"></sop1>
                <sop2 v-if="state.selectedKeys[0]==='2'"></sop2>
                <sop3 v-if="state.selectedKeys[0]==='3'"></sop3>
                <sop4 v-if="state.selectedKeys[0]==='4'"></sop4>
            </div>
            <a-card title="操作日志" style="width: 50%">
                        
            </a-card>
        </a-flex>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script setup>
import { reactive, h } from 'vue';
import sop1 from '@/views/sopComponents/sop1.vue'
import sop2 from '@/views/sopComponents/sop2.vue'
import sop3 from '@/views/sopComponents/sop3.vue'
import sop4 from '@/views/sopComponents/sop4.vue'
import {
  ChromeOutlined,
  BellOutlined,
  UserSwitchOutlined,
  UsergroupAddOutlined,
} from '@ant-design/icons-vue';

const state = reactive({
  collapsed: true,
  selectedKeys: ['1'],
});
const styleIcon = {fontSize:'24px',marginLeft:'-4px',marginTop:'8px',color:'#666'};
const items = reactive([
  {
    key: '1',
    icon: () => h(ChromeOutlined,{style: styleIcon}),
    label: '评论朋友圈',
    title: '自动评论朋友圈配置'
  },
  {
    key: '2',
    icon: () => h(BellOutlined,{style: styleIcon}),
    label: '群发任务',
    title: '主动推送群发任务',
  },
  {
    key: '3',
    icon: () => h(UserSwitchOutlined,{style: styleIcon}),
    label: '好友通过',
    title: '自动通过好友配置',
  },
  {
    key: '4',
    icon: () => h(UsergroupAddOutlined,{style: styleIcon}),
    label: '添加好友',
    title: '添加好友配置',
  },
]);
 
</script>
<style scoped>
#components-layout-sop{
    height: 100%;
}
#components-layout-sop .logo {
  height: 32px;
  margin: 16px 16px 0px;
  font-size: 16px;
  color: #2e2e2e;
  font-weight: bold;
  text-align: center;
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