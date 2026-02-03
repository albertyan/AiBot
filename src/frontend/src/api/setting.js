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

export const getDifySettings = async () => {
  const response = await fetch('/api/setting/dify_settings');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取 Dify 配置失败');
  }
};

export const saveDifySettings = async (baseUrl) => {
  const response = await fetch(`/api/setting/dify_settings?baseUrl=${encodeURIComponent(baseUrl)}`, {
    method: 'POST'
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存 Dify 配置失败');
  }
};

export const getCozeSettings = async () => {
  const response = await fetch('/api/setting/coze_settings');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取 Coze 配置失败');
  }
};

export const setCozeSettings = async (token) => {
  const response = await fetch('/api/setting/coze_settings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ token })
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存 Coze 配置失败');
  }
};

export const getAgents = async () => {
  const response = await fetch('/api/setting/agents');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取智能体列表失败');
  }
};

export const addAgent = async (agent) => {
  const response = await fetch('/api/setting/agents', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(agent)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('添加智能体失败');
  }
};

export const deleteAgent = async (id) => {
  const response = await fetch(`/api/setting/agents/${id}`, {
    method: 'DELETE'
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('删除智能体失败');
  }
};
