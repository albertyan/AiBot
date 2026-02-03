/**
 * 校验 URL 格式
 * 要求以 http:// 或 https:// 开头
 * @param {string} url 
 * @returns {boolean}
 */
export const isValidUrl = (url) => {
  if (!url) return false;
  const urlPattern = /^https?:\/\/.+/i;
  return urlPattern.test(url.trim());
};

/**
 * 校验 Bot ID 格式
 * 简单校验非空且长度限制（根据实际需求调整）
 * @param {string} id 
 * @returns {boolean}
 */
export const isValidBotId = (id) => {
  return !!id && id.trim().length > 0;
};

/**
 * 校验 Token 格式
 * 简单校验非空
 * @param {string} token 
 * @returns {boolean}
 */
export const isValidToken = (token) => {
  return !!token && token.trim().length > 0;
};
