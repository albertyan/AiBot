<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useSystemStore } from '../stores/system';
import NavBar from '../components/NavBar.vue';
import { getFriendCount, getGroupCount } from '../api/launch.js';

// 这里使用路由查询参数而非全局状态，原因是首页展示的数据仅在启动阶段生成并短期使用，避免引入复杂状态管理
const route = useRoute();
const systemStore = useSystemStore();
const activeTab = ref('account');
// 将 Launch 通过 query 传递的参数转为响应式，原因是 Home 可能会在同一会话内被重新导航，需要实时反映路由变化
const wxNumber = computed(() => route.query.wxNumber || '');
const nickname = computed(() => route.query.nickname || '');
const status = computed(() => systemStore.statusText);

const friendCount = ref(0);
const groupCount = ref(0);
const loading = ref(true);

onMounted(async () => {
  try {
    const [fc, gc] = await Promise.all([getFriendCount(), getGroupCount()]);
    friendCount.value = fc?.data ?? 0;
    groupCount.value = gc?.data ?? 0;
  } catch (err) {
    console.error(err);
    friendCount.value = 0;
    groupCount.value = 0;
  } finally {
    loading.value = false;
  }
});


</script>

<template>
  <div v-if="!loading" class="min-h-screen bg-slate-50">
    <!-- 顶部导航 -->
    <NavBar />

    <!-- 主要内容区域 -->
    <div class="flex h-[calc(100vh-65px)]">
      <!-- 左侧边栏 -->
      <div class="w-20 bg-white/80 backdrop-blur-md border-r border-slate-200 flex flex-col items-center py-8 space-y-4">
        <button
          @click="activeTab = 'account'"
          :class="`w-12 h-12 rounded-xl flex flex-col items-center justify-center transition-all duration-200 ${
            activeTab === 'account'
              ? 'bg-gradient-to-br from-primary-50 to-primary-100 text-primary-600 border border-primary-100 shadow-sm'
              : 'text-slate-400 hover:text-primary-600 hover:bg-slate-50'
          }`"
        >
          <div :class="`w-6 h-6 rounded-md flex items-center justify-center text-[10px] font-bold mb-0.5 transition-colors ${
             activeTab === 'account' ? 'bg-gradient-to-br from-primary-500 to-primary-600 text-white' : 'bg-slate-200 text-slate-500'
          }`">
            {{ wxNumber.slice(0, 2) }}
          </div>
          <span class="text-[10px] whitespace-nowrap font-medium">账号</span>
        </button>
        
        <button
          @click="activeTab = 'settings'"
          :class="`w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-200 ${
            activeTab === 'settings'
              ? 'bg-gradient-to-br from-primary-50 to-primary-100 text-primary-600 border border-primary-100 shadow-sm'
              : 'text-slate-400 hover:text-primary-600 hover:bg-slate-50'
          }`"
        >
          <i class="ri-settings-3-line text-xl"></i>
        </button>
      </div>

      <!-- 主内容区 -->
      <div class="flex-1 overflow-y-auto bg-slate-50">
        <div class="max-w-6xl mx-auto px-8 py-10">
          <!-- 标题区域 -->
          <div class="mb-10 flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-slate-800 mb-2 tracking-tight">
                Anlunai <span class="text-slate-400 text-lg font-normal ml-2">v1.5.5</span>
              </h1>
              <p class="text-base text-slate-500">
                欢迎回来，<span class="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-primary-500 font-bold">{{ nickname }}</span>
              </p>
            </div>
            <!-- 可选：添加快捷操作按钮或时间显示 -->
          </div>

          <!-- 统计卡片 -->
          <div class="grid grid-cols-3 gap-6 mb-8">
            <div class="bg-gradient-to-br from-white to-primary-50/30 border border-slate-200/60 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow group">
              <div class="flex items-center justify-between mb-4">
                <div class="text-slate-500 text-sm font-medium">好友数量</div>
                <div class="w-8 h-8 rounded-lg bg-primary-50 flex items-center justify-center text-primary-600">
                  <i class="ri-user-line"></i>
                </div>
              </div>
              <div class="text-4xl font-bold text-slate-800 group-hover:text-primary-600 transition-colors">{{ friendCount }}</div>
            </div>
            
            <div class="bg-gradient-to-br from-white to-emerald-50/30 border border-slate-200/60 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow group">
              <div class="flex items-center justify-between mb-4">
                <div class="text-slate-500 text-sm font-medium">群聊数量</div>
                <div class="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center text-emerald-600">
                  <i class="ri-group-line"></i>
                </div>
              </div>
              <div class="text-4xl font-bold text-slate-800 group-hover:text-emerald-600 transition-colors">{{ groupCount }}</div>
            </div>
            
            <div :class="`bg-gradient-to-br ${systemStore.isConnected ? 'from-primary-500 to-primary-600' : 'from-slate-500 to-slate-600'} rounded-xl p-6 shadow-lg shadow-primary-500/20 text-white relative overflow-hidden group`">
              <div class="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-8 -mt-8 pointer-events-none transition-transform group-hover:scale-150 duration-500"></div>
              <div class="flex items-center justify-between mb-4 relative z-10">
                <div class="text-primary-100 text-sm font-medium">系统状态</div>
                <div class="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center text-white">
                  <i class="ri-wifi-line"></i>
                </div>
              </div>
              <div class="text-2xl font-bold mb-1 relative z-10">{{ status }}</div>
              <div class="text-primary-100 text-sm relative z-10">{{ systemStore.isConnected ? '正常连接' : '连接断开' }}</div>
            </div>
          </div>

          <!-- 功能卡片 -->
          <div class="grid grid-cols-2 gap-6 mb-8">
            <div class="bg-white border border-slate-200/60 rounded-xl p-6 shadow-sm hover:border-primary-300 hover:shadow-md hover:bg-primary-50/30 transition-all cursor-default group">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center shrink-0 group-hover:bg-primary-600 transition-colors duration-300">
                  <i class="ri-shield-check-line text-primary-600 text-xl group-hover:text-white transition-colors duration-300"></i>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-slate-800 mb-1 group-hover:text-primary-600 transition-colors">安全保障</h3>
                  <p class="text-slate-500 text-sm leading-relaxed">基于 RPA 技术模拟真人操作，确保账号安全稳定，降低封号风险。</p>
                </div>
              </div>
            </div>

            <div class="bg-white border border-slate-200/60 rounded-xl p-6 shadow-sm hover:border-emerald-300 hover:shadow-md hover:bg-emerald-50/30 transition-all cursor-default group">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-emerald-50 rounded-lg flex items-center justify-center shrink-0 group-hover:bg-emerald-600 transition-colors duration-300">
                  <i class="ri-customer-service-2-line text-emerald-600 text-xl group-hover:text-white transition-colors duration-300"></i>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-slate-800 mb-1 group-hover:text-emerald-600 transition-colors">AI智能客服</h3>
                  <p class="text-slate-500 text-sm leading-relaxed">接入先进大模型，提供 7*24 小时智能问答服务，精准响应客户需求。</p>
                </div>
              </div>
            </div>

            <div class="bg-white border border-slate-200/60 rounded-xl p-6 shadow-sm hover:border-cyan-300 hover:shadow-md hover:bg-cyan-50/30 transition-all cursor-default group">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-cyan-50 rounded-lg flex items-center justify-center shrink-0 group-hover:bg-cyan-600 transition-colors duration-300">
                  <i class="ri-group-line text-cyan-600 text-xl group-hover:text-white transition-colors duration-300"></i>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-slate-800 mb-1 group-hover:text-cyan-600 transition-colors">多账号管理</h3>
                  <p class="text-slate-500 text-sm leading-relaxed">集中管理多个微信账号，统一消息聚合与回复，大幅提升运营效率。</p>
                </div>
              </div>
            </div>
            
            <div class="bg-white border border-slate-200/60 rounded-xl p-6 shadow-sm hover:border-primary-300 hover:shadow-md hover:bg-primary-50/30 transition-all cursor-default group">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center shrink-0 group-hover:bg-primary-600 transition-colors duration-300">
                  <i class="ri-wechat-line text-primary-600 text-xl group-hover:text-white transition-colors duration-300"></i>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-slate-800 mb-1 group-hover:text-primary-600 transition-colors">朋友圈营销</h3>
                  <p class="text-slate-500 text-sm leading-relaxed">自动化朋友圈内容发布与互动，打造活跃人设，增强客户粘性。</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 底部按钮 -->
          <div class="flex items-center justify-center space-x-4 mt-8">
            <button class="px-6 py-2.5 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-lg font-medium shadow-md shadow-primary-500/20 hover:from-primary-600 hover:to-primary-700 hover:shadow-lg transition-all whitespace-nowrap flex items-center space-x-2 text-sm">
              <i class="ri-service-line text-base"></i>
              <span>专属客服</span>
            </button>
            
            <button class="px-6 py-2.5 bg-white text-slate-700 rounded-lg font-medium shadow-sm hover:shadow-md hover:text-primary-600 hover:border-primary-200 transition-all border border-slate-200 whitespace-nowrap flex items-center space-x-2 text-sm">
              <i class="ri-link text-base"></i>
              <span>解绑账号</span>
            </button>
            
            <button class="px-6 py-2.5 bg-white text-slate-700 rounded-lg font-medium shadow-sm hover:shadow-md hover:text-primary-600 hover:border-primary-200 transition-all border border-slate-200 whitespace-nowrap flex items-center space-x-2 text-sm">
              <i class="ri-refresh-line text-base"></i>
              <span>版本更新</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
