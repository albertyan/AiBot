<script setup>
import { MessageTwoTone,MailTwoTone,CalendarTwoTone } from '@ant-design/icons-vue';
import { useRouter } from 'vue-router'
const router = useRouter()
 
</script>

<template>
  <div class="homeBg">
    <a-card :bordered="false" class="wel-card">
      <template #title>
        <div class="title-box">
          <span class="title">webChatBot</span>
          <span class="version">v1.0.0</span>
        </div>
      </template >
      <h2>欢迎回来，lie234234</h2>
       <a-flex gap="middle" horizontal>
          <div class="grid-box">
            <div class="nums">0</div>
            <div class="txt-1">好友数量</div>
          </div>
          <div class="grid-box">
            <div class="nums">0</div>
            <div class="txt-1">群聊数量</div>
          </div>
          <div class="grid-box">
            <div class="nums">在线</div>
            <div class="txt-2">状态正常</div>
          </div>
       </a-flex>
       <p class="ptitle">功能介绍</p>
       <a-flex gap="middle" horizontal>
          <div class="grid-box">
            <div class="icon"><MessageTwoTone :style="{fontSize: '28px'}"/></div>
            <div class="txt-3">AI销售</div>
            <div class="txt-4">自动化回复消息</div>
          </div>
          <div class="grid-box">
            <div class="icon"><MailTwoTone :style="{fontSize: '28px'}" /></div>
            <div class="txt-3">无线群发</div>
            <div class="txt-4">高效率群发消息</div>
          </div>
          <div class="grid-box">
            <div class="icon"><CalendarTwoTone :style="{fontSize: '28px'}" /></div>
            <div class="txt-3">定时任务</div>
            <div class="txt-4">自动化SOP</div>
          </div>
       </a-flex>
       <div class="wel-footer">
        联系客服：13546545646 <a>解绑</a>
       </div>
    </a-card>
  </div>
</template>

<style scoped>
 .homeBg{
  background: radial-gradient(circle, #183149, #041b35);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
 }
 .wel-card{
  width: 500px;
 }
 .wel-card h2{
  text-align: center;
  color: #444444;
  margin: 0 0 25px 0;
 }
 .wel-card .version{
  font-size: 12px;
  color: #999;
  margin-left: 10px;
 }
 .wel-card .title-box{
  text-align: center;
 }
 .wel-card .title-box .title{
  font-size: 24px;
  font-weight: bold;
 }
 .wel-card .ptitle{
  font-size: 18px;
  font-weight: bold;
  margin: 35px 0 15px;
 }
 .wel-card .grid-box{
  width: 30%;
  background: #e8f0f8;
  border-radius: 10px;
  padding: 10px;
  text-align: center;
 }
 .wel-card .grid-box:hover{
  background: #cadbec;
  cursor: pointer;
 }
 .wel-card .grid-box .nums{
  font-size: 24px;
  font-weight: bold;
  color: #039bf3;
  margin: 10px 0;
 }
 .wel-card .grid-box .txt-1{
  font-size: 16px;
  color: #666;
 }
 .wel-card .grid-box .txt-2{
  font-size: 12px;
  color: #fcfcfc;
  background: #cccccc;
  border-radius: 30px;
  display: inline-block;
  padding: 3px 10px;
 }
 .wel-card .grid-box .icon{
  margin: 10px 0;
 }
 .wel-card .grid-box .txt-3{
  font-size: 16px;
  color: #193457;
  font-weight: bold;
  margin-bottom: 5px;
 }
 .wel-card .grid-box .txt-4{
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
 }
 .wel-footer{
  padding: 50px 20px 10px;
  text-align: center;
 }
</style>