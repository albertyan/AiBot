<template>
    <div class="contacts-body">
        <a-tabs v-model:activeKey="activeKey">
            <a-tab-pane key="1" tab="好友"></a-tab-pane>
            <a-tab-pane key="2" tab="群聊"></a-tab-pane>
            <template #rightExtra>
                <a-space>
                    <a-select style="width:100px" v-model:value="tb">
                        <a-select-option key="all" value="0">全部</a-select-option>
                    </a-select>
                    <a-button type="primary">同步{{ activeKey==='1'?'好友':'群聊' }}数据</a-button>
                </a-space>
            </template>
        </a-tabs>
        <a-flex gap="small" class="contacts-list">
            <div class="contacts-left">
                <a-card :bodyStyle="{padding:0,flexGrow:1}" :headStyle="{padding:'10px',minHeight:'35px'}" class="c-card" v-show="activeKey==='1'">
                    <template #title>
                        共 <span>1368</span> 个好友
                    </template>
                    <template #extra>
                        <a-button type="link" size="small">全选</a-button>
                    </template>
                    <div class="user-list">
                        <div class="user-search">
                            <a-input-search
                                placeholder="搜索好友"
                                style="width: 100%"
                                />
                        </div>
                        <div class="user-items">
                            <a-list item-layout="horizontal" :data-source="data">
                                <template #renderItem="{ item }">
                                    <a-list-item>
                                        <a-list-item-meta style="align-items: center;">
                                            <template #title>
                                                {{ item.title }}
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
                <a-card :bodyStyle="{padding:0,flexGrow:1}" :headStyle="{padding:'10px',minHeight:'35px'}" class="c-card" v-show="activeKey==='2'">
                    <template #title>
                        共 <span>54</span> 个群聊
                    </template>
                    <template #extra>
                        <a-button type="link" size="small">全选</a-button>
                    </template>
                    <div class="user-list">
                        <div class="user-search">
                            <a-input-search
                                placeholder="搜索群聊"
                                style="width: 100%"
                                />
                        </div>
                        <div class="user-items">
                            <a-list item-layout="horizontal" :data-source="data">
                                <template #renderItem="{ item }">
                                    <a-list-item>
                                        <a-list-item-meta style="align-items: center;">
                                            <template #title>
                                                {{ item.title }}
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
            <div class="contacts-right">
                <a-card :bodyStyle="{padding:0,flexGrow:1}" :headStyle="{padding:'10px',minHeight:'35px'}" title="通讯录群发" class="c-card">
                    <template #extra>
                        <a-button type="link" size="small">全选</a-button>
                    </template>
                    <template #actions>
                        <a-button type="primary">新建推送任务</a-button>
                    </template>
                    <div class="user-list">
                        <div class="user-search gray-bg">
                             已选择群聊: <a-button type="link">10月7日测试新区域问题处理</a-button>
                        </div>
                        <div class="user-task"></div>
                    </div>
                </a-card>
            </div>
        </a-flex>
    </div>
</template>
<script setup>
import  {ref} from 'vue'
const activeKey = ref('1')
const tb = ref('0')
const data = [
  {
    title: '王帅',
  },
  {
    title: '&欣欣S向荣&',
  },
  {
    title: '&-山鸡-&',
  },
  {
    title: '撒旦发射点',
  },
];
</script>
<style scoped>
.c-card{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.contacts-body{
    height: 100%;
    padding: 10px 20px;
    background: #fff;
    display: flex;
    flex-direction: column;
}
.contacts-list{
    flex-grow: 1;
}
.contacts-left{
    width: 40%;
}
.contacts-right{
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
.gray-bg{
    background-color: #f8f8f8;
}
</style>