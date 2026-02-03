import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSystemStore = defineStore('system', () => {
  const isConnected = ref(true);
  const statusText = ref('在线');
  const timer = ref(null);

  const checkHeartbeat = async () => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000); // 3s timeout
      
      const response = await fetch('/api/c_hello', { 
        signal: controller.signal 
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        isConnected.value = true;
        statusText.value = '在线';
      } else {
        isConnected.value = false;
        statusText.value = '离线';
      }
    } catch (error) {
      isConnected.value = false;
      statusText.value = '离线';
      console.warn('Heartbeat failed:', error);
    }
  };

  const startHeartbeat = () => {
    // Check immediately
    checkHeartbeat();
    // Then every 5 seconds
    if (timer.value) clearInterval(timer.value);
    timer.value = setInterval(checkHeartbeat, 10000);
  };

  const stopHeartbeat = () => {
    if (timer.value) {
      clearInterval(timer.value);
      timer.value = null;
    }
  };

  return {
    isConnected,
    statusText,
    startHeartbeat,
    stopHeartbeat
  };
});
