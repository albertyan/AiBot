export const getGreetingConfig = async () => {
  const response = await fetch('/api/setting/greeting_config');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取话术配置失败');
  }
};

export const saveGreetingConfig = async (config) => {
  const response = await fetch('/api/setting/greeting_config', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(config)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存话术配置失败');
  }
};
