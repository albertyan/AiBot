export const getDashboardData = async () => {
  const response = await fetch('/api/home/dashboard');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('连接服务器失败，请检查后台服务是否启动');
  }
};

export const getFriendCount = async () => {
  const response = await fetch('/api/home/friendCount');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('连接服务器失败，请检查后台服务是否启动');
  }
};

export const getGroupCount = async () => {
  const response = await fetch('/api/home/groupCount');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('连接服务器失败，请检查后台服务是否启动');
  }
};


