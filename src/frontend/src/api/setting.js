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

export const setDefaultAgent = async (id) => {
  const response = await fetch(`/api/setting/agents/${id}/default`, {
    method: 'PUT'
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('设置默认智能体失败');
  }
};

export const getMomentSettings = async () => {
  const response = await fetch('/api/setting/moment_settings');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取朋友圈配置失败');
  }
};

export const saveMomentSettings = async (settings) => {
  const response = await fetch('/api/setting/moment_settings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(settings)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存朋友圈配置失败');
  }
};

export const getChatHistorySettings = async () => {
  const response = await fetch('/api/setting/chat_history_settings');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取 AI 回复配置失败');
  }
};

export const saveChatHistorySettings = async (settings) => {
  const response = await fetch('/api/setting/chat_history_settings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(settings)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存 AI 回复配置失败');
  }
};

export const sendTestAlertEmail = async (email) => {
  const response = await fetch(`/api/setting/test_alert_email?email=${encodeURIComponent(email)}`, {
    method: 'POST'
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('发送测试邮件失败');
  }
};

export const getAlertSettings = async () => {
  const response = await fetch('/api/setting/alert_settings');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取预警配置失败');
  }
};

export const saveAlertSettings = async (settings) => {
  const response = await fetch('/api/setting/alert_settings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(settings)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存预警配置失败');
  }
};

export const getRestTimeSettings = async () => {
  const response = await fetch('/api/setting/rest_time_settings');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取休息时间配置失败');
  }
};

export const saveRestTimeSettings = async (settings) => {
  const response = await fetch('/api/setting/rest_time_settings', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(settings)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存休息时间配置失败');
  }
};
