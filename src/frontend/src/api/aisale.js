
export const getAiConfig = async () => {
  const response = await fetch('/api/aisale/get_ai_config');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取AI助理配置失败');
  }
};

export const saveAiAgent = async (agent) => {
  const response = await fetch('/api/aisale/save_agent', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(agent)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存AI助理失败');
  }
};

export const deleteAiAgent = async (agentId) => {
  const response = await fetch(`/api/aisale/delete_agent?agent_id=${encodeURIComponent(agentId)}`, {
    method: 'POST'
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('删除AI助理失败');
  }
};

export const updateEnableStatus = async (agentId, enabled) => {
  const response = await fetch(`/api/aisale/update_enable_status?agent_id=${encodeURIComponent(agentId)}&enabled=${enabled}`, {
    method: 'POST'
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('更新状态失败');
  }
};

export const saveCommonConfig = async (config) => {
  const response = await fetch('/api/aisale/save_common_config', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(config)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('保存通用配置失败');
  }
};