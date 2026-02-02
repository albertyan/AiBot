export const syncFriend = async () => {
  const response = await fetch('/api/custom/sync_friend');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('同步好友失败');
  }
};

export const syncGroup = async () => {
  const response = await fetch('/api/custom/sync_group');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('同步群聊失败');
  }
};

export const getFriends = async () => {
  const response = await fetch('/api/custom/friends');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取好友列表失败');
  }
};

export const getGroups = async () => {
  const response = await fetch('/api/custom/groups');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取群聊列表失败');
  }
};

export const getFriendTags = async () => {
  const response = await fetch('/api/custom/friend_tags');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取好友标签失败');
  }
};

export const getGroupTags = async () => {
  const response = await fetch('/api/custom/group_tags');
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('获取群聊标签失败');
  }
};

export const setGroupTags = async (groups, tag) => {
  const response = await fetch('/api/custom/set_group_tags?tag=' + encodeURIComponent(tag), {
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
