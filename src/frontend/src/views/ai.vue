<template>
    <div class="ai-body">
        <div class="ai-head">
            <a-space>
                自动回复：<a-switch></a-switch>
                <a-button type="link"><ProfileOutlined />日志</a-button>
            </a-space>
            <a-button type="primary" danger ghost @click="showModal">策略配置</a-button>
        </div>
        <a-flex gap="small" class="ai-list">
            <div class="ai-left">
                <a-card :bodyStyle="{padding:0,flexGrow:1}" :headStyle="{padding:'10px',minHeight:'35px'}" class="c-card">
                    <template #title>
                        最近会话: <span>3</span> 个用户
                    </template>
                    <template #extra>
                        <a-button type="link" size="small"><ReloadOutlined />刷新</a-button>
                    </template>
                    <div class="user-list">
                        <div class="user-items">
                            <a-list item-layout="horizontal" :data-source="data">
                                <template #renderItem="{ item }">
                                    <a-list-item>
                                        <a-list-item-meta style="align-items: center;">
                                            <template #title>
                                                <div class="a-items">
                                                    <div style="flex-grow: 1;">
                                                        <span class="a-title">{{ item.title }}</span>
                                                        <a-tag>群聊</a-tag>
                                                    </div>
                                                    <span class="a-time">17:34</span>
                                                </div>
                                            </template>
                                            <template #description>
                                                {{ item.description }}
                                            </template>
                                            <template #avatar>
                                                <a-avatar size="large" src="https://joeschmoe.io/api/v1/random" />
                                            </template>
                                        </a-list-item-meta>
                                    </a-list-item>
                                </template>
                            </a-list>
                        </div>
                    </div>
                </a-card>
            </div>
            <div class="ai-right">
                <a-card :bodyStyle="{padding:0,flexGrow:1}" :headStyle="{padding:'10px',minHeight:'35px'}" class="c-card">
                    <div class="user-list">
                        <div class="user-task"></div>
                        <div class="user-input">
                            <div class="user-input-head">
                                <a-button type="default" size="small">智能体生成话术</a-button>
                            </div>
                            <div class="user-input-box">
                                <div style="flex-grow: 1;">
                                    <a-textarea :rows="4" :maxlength="500" placeholder="请输入消息" allowClear></a-textarea>
                                </div>
                                <div>
                                    <a-button type="primary">发送</a-button>
                                </div>
                            </div>
                        </div>
                    </div>
                </a-card>
            </div>
        </a-flex>
        <!-- 配置弹框 -->
         <a-modal v-model:open="open" :bodyStyle="{height:'60vh',overflow:'auto',padding:'10px'}" title="自动回复策略配置" okText="保存设置" @ok="handleOk" @cancel="resetForm">
            <a-alert style="margin: 10px 0;"  message='修改策略后，需要重新开启自动回复生效' type="info" show-icon></a-alert>
            <aiSetting></aiSetting>
        </a-modal> 
    </div>
</template>
<script setup>
import {
    ProfileOutlined,
    ReloadOutlined
} from '@ant-design/icons-vue'
import aiSetting from '@/views/aiComponents/aiSetting.vue'
import  {ref} from 'vue'
const open = ref(false); 
const data = [
  {
    title: '王帅',
    description: '[2条]机器人查询:@人本s的算法的是否就啊手动阀'
  },
  {
    title: '&欣欣S向荣&',
    description: '[2条]机器人查询:@人本s的算法的是否就啊手动阀'
  },
  {
    title: '&-山鸡-&',
    description: '[2条]机器人查询:@人本s的算法的是否就啊手动阀'
  },
  {
    title: '撒旦发射点',
    description: '[2条]机器人查询:@人本s的算法的是否就啊手动阀'
  },
];
const showModal = () => {
  open.value = true;
};
 
// 提交
const handleOk = e => {
  console.log(e);
};
</script>
<style scoped>
.c-card{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.ai-body{
    height: 100%;
    padding: 10px 20px;
    background: #fff;
    display: flex;
    flex-direction: column;
}
.ai-head{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
}
.ai-list{
    flex-grow: 1;
}
.ai-left{
    width: 40%;
}
.ai-right{
    width: 60%;
}
.user-search{
    border-bottom: 1px solid #eee;
    padding: 10px;
}
.user-list{
    display: flex;
    flex-direction: column;
    height: 100%;
}
.user-items,.user-task{
    flex-grow: 1;
    padding: 0;
}
.a-items{
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.a-title{
    font-weight: bold;
    margin-right: 10px;
    min-width: 100px;
}
.a-time{
    color: #999;
}
.user-input{
    border-top: 1px solid #eee;
}
.user-input-head{
    padding: 10px;
    border-bottom: 1px solid #eee;
}
.user-input-box{
    display: flex;
    align-items: center;
}
.user-input-box > div{
    padding: 10px;
}
</style>