<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
// 启动应用
function launchApp(){
  router.push('/index')
}
</script>

<template>
  <div class="homeBg">
    <a-card :bordered="false" class="home-card">
      <template #title>
        <div class="title-box">
          <span class="title">webChatBot</span>
          <span class="version">v1.0.0</span>
        </div>
      </template >
      <h2>启动向导</h2>
      <p>1、请确保已登录个人微信号</p>
      <p>2、适当缩小微信窗口，并保持和机器人并排放置</p>
      <a-alert message="重要! 确保微信窗口不要被遮挡" type="warning" show-icon />
      <p>3、以上完成后，点击下方按钮启动应用</p>
      <div class="home-button">
        <a-button size="large" shape="round" type="primary" @click="launchApp">启动应用</a-button>
      </div>
      <a-alert
      message="免责声明"
      type="info"
      >
      <template #description>
        <div>· 本软件仅供日常交流使用，严禁用于非法用途</div>
        <div>· 请遵守相关法律法规，违规使用造成的后果由使用者承担</div>
      </template>
      </a-alert>
    </a-card>
  </div>
</template>

<style scoped>
 .homeBg{
  background: radial-gradient(circle, #3a7bd5, #025497);
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
 }
 .home-card{
  width: 500px;
  margin:10% auto;
 }
 .home-card .title{
  font-size: 24px;
  font-weight: bold;
 }
 .home-card .version{
  font-size: 12px;
  color: #999;
  margin-left: 10px;
 }
 .home-card p{
  margin: 10px 0;
 }
 .home-card .title-box{
  text-align: center;
 }
 .home-button{
  padding: 20px 0;
  text-align: center;
 }
</style>