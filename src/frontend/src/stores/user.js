import { defineStore } from 'pinia';
import { ref } from 'vue';
import router from '../router';

export const useUserStore = defineStore('user', () => {
  const userInfo = ref(null);

  const setUserInfo = (data) => {
    userInfo.value = data;
    // Persist to localStorage for persistence across reloads if needed
    localStorage.setItem('user_info', JSON.stringify(data));
  };

  const clearUserInfo = () => {
    userInfo.value = null;
    localStorage.removeItem('user_info');
  };

  // Initialize from localStorage if available
  const init = () => {
    const stored = localStorage.getItem('user_info');
    if (stored) {
      try {
        userInfo.value = JSON.parse(stored);
      } catch (e) {
        console.error('Failed to parse user info from localStorage', e);
        localStorage.removeItem('user_info');
      }
    }
  };

  init();

  return {
    userInfo,
    setUserInfo,
    clearUserInfo
  };
});

// Global method to get current user
export const get_current_user = () => {
  const store = useUserStore();
  if (!store.userInfo) {
    message.error('用户信息已失效，请重新登录！');
    router.push('/');
    return null;
  }
  return store.userInfo;
};
