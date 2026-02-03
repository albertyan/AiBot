<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import AddAgentModal from './AddAgentModal.vue';
import { getAgents, addAgent, deleteAgent, setDefaultAgent } from '../../api/setting';

/**
 * 智能体管理
 * 为什么将“添加”与“列表”放在同一组件：
 * - 保持操作的局部性与可见性，避免在不同页面来回切换造成认知负荷
 * - 列表与新增共享同一数据源，减少跨组件状态同步问题
 */
const agents = ref([]);

const isAddModalVisible = ref(false);

const loadAgents = async () => {
  try {
    const res = await getAgents();
    if (res.code === 200) {
      agents.value = res.data.agents;
    }
  } catch (error) {
    console.error(error);
    message.error('加载智能体列表失败');
  }
};

onMounted(() => {
  loadAgents();
});

/**
 * 处理添加智能体
 */
const handleAddAgent = async (payload) => {
  try {
    const res = await addAgent(payload);
    if (res.code === 200) {
      message.success('添加成功');
      loadAgents();
    } else {
      message.error(res.msg || '添加失败');
    }
  } catch (error) {
    console.error(error);
    message.error('添加智能体出错');
  }
};

// 暂不支持单独设置默认，目前仅在添加时设置生效
// 如果需要支持单独设置默认，需要后端增加更新接口
const setDefault = async (id) => {
  try {
    const res = await setDefaultAgent(id);
    if (res.code === 200) {
      message.success('设置默认成功');
      loadAgents();
    } else {
      message.error(res.msg || '设置失败');
    }
  } catch (error) {
    console.error(error);
    message.error('设置默认出错');
  }
};

const removeAgent = async (id) => {
  try {
    const res = await deleteAgent(id);
    if (res.code === 200) {
      message.success('删除成功');
      loadAgents();
    } else {
      message.error(res.msg || '删除失败');
    }
  } catch (error) {
    console.error(error);
    message.error('删除出错');
  }
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-slate-800">智能体管理</h1>
      <button
        @click="isAddModalVisible = true"
        class="px-4 py-2 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors"
      >
        添加智能体
      </button>
    </div>

    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="space-y-4">
        <div
          v-for="agent in agents"
          :key="agent.id"
          class="flex items-center justify-between p-4 border border-slate-200 rounded-lg"
        >
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-[#4A90E2] rounded-lg flex items-center justify-center">
              <i class="ri-robot-line text-white text-lg"></i>
            </div>
            <div>
              <div class="text-sm font-semibold text-slate-800">{{ agent.name }}</div>
              <div class="text-xs text-slate-500">Bot ID: {{ agent.botId }}</div>
              <div class="text-xs text-slate-400 mt-0.5">平台：{{ agent.platform }}</div>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button
              @click="setDefault(agent.id)"
              :class="agent.isDefault ? 'bg-green-500 text-white hover:bg-green-600' : 'bg-green-50 text-green-600 hover:bg-green-100'"
              class="px-3 py-1.5 rounded text-xs font-medium transition-colors"
            >
              {{ agent.isDefault ? '默认' : '设为默认' }}
            </button>
            <button
              @click="removeAgent(agent.id)"
              class="w-8 h-8 flex items-center justify-center text-red-500 hover:bg-red-50 rounded-lg transition-colors"
            >
              <i class="ri-delete-bin-line"></i>
            </button>
          </div>
        </div>
      </div>

      <button
        @click="isAddModalVisible = true"
        class="w-full mt-4 px-4 py-2.5 bg-[#4A90E2] hover:bg-[#357ABD] text-white rounded-lg text-sm font-medium transition-colors"
      >
        添加智能体
      </button>
    </div>
    
    <AddAgentModal
      v-model="isAddModalVisible"
      @confirm="handleAddAgent"
    />
  </div>
</template>
