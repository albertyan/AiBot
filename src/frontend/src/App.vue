<script setup>
import { onMounted, onUnmounted } from 'vue';
import { useSystemStore } from './stores/system';

const systemStore = useSystemStore();

onMounted(() => {
  systemStore.startHeartbeat();
});

onUnmounted(() => {
  systemStore.stopHeartbeat();
});
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 font-sans">
    <router-view></router-view>
  </div>
</template>
