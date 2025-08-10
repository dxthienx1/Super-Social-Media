// 1. Ẩn navigator.webdriver
Object.defineProperty(navigator, 'webdriver', {
  get: () => undefined
});

// 2. Giả lập window.chrome
Object.defineProperty(window, 'chrome', {
  get: () => ({ runtime: {} })
});

// 3. Giả navigator.languages
Object.defineProperty(navigator, 'languages', {
  get: () => ['en-US', 'en']
});

// 4. Giả navigator.plugins
Object.defineProperty(navigator, 'plugins', {
  get: () => [1, 2, 3, 4, 5],
});

// 5. Giả navigator.permissions (đặc biệt với 'notifications')
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) =>
  parameters.name === 'notifications'
    ? Promise.resolve({ state: Notification.permission })
    : originalQuery(parameters);

// 6. Fake WebGL Vendor và Renderer (không phải lúc nào cũng cần)
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function (parameter) {
  if (parameter === 37445) return 'Intel Inc.';
  if (parameter === 37446) return 'Intel Iris OpenGL Engine';
  return getParameter.call(this, parameter);
};
