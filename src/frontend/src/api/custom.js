export const syncFriend = async (wxNumber) => {
  if (!wxNumber) {
    throw new Error('请提供微信号');
  }
  const url = `/api/custom/sync_friend?wx_number=${wxNumber}`;
  const response = await fetch(url);
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('同步好友失败');
  }
};

export const syncGroup = async (wxNumber) => {
  if (!wxNumber) {
    throw new Error('请提供微信号');
  }
  const url = `/api/custom/sync_group?wx_number=${wxNumber}`;
  const response = await fetch(url);
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('同步群聊失败');
  }
};

export const getFriends = async (wxNumber) => {
  console.log('currentUser.wxNumber', wxNumber);
  if (!wxNumber) {
    throw new Error('请提供微信号');
  }
  const url = `/api/custom/friends?wx_number=${wxNumber}`;
  const response = await fetch(url);
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取好友列表失败');
  }
};

export const getGroups = async (wxNumber) => {
  if (!wxNumber) {
    throw new Error('请提供微信号');
  }
  const url = `/api/custom/groups?wx_number=${wxNumber}`;
  const response = await fetch(url);
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取群聊列表失败');
  }
};

export const getFriendTags = async (wxNumber) => {
  if (!wxNumber) {
    throw new Error('请提供微信号');
  }
  const url = `/api/custom/friend_tags?wx_number=${wxNumber}`;
  const response = await fetch(url);
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取好友标签失败');
  }
};

export const getGroupTags = async (wxNumber) => {
  if (!wxNumber) {
    throw new Error('请提供微信号');
  }
  const url = `/api/custom/group_tags?wx_number=${wxNumber}`;
  const response = await fetch(url);
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取群聊标签失败');
  }
};

export const setGroupTags = async (wxNumber, groups, tag) => {
  if (!wxNumber) {
    throw new Error('请提供微信号');
  }
  const url = `/api/custom/set_group_tags?wx_number=${wxNumber}&tag=${encodeURIComponent(tag)}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(groups)
  });
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('设置群聊标签失败');
  }
};

export const getCurrentUser = async () => {
  const response = await fetch('/api/custom/current_user');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取当前用户失败');
  }
};