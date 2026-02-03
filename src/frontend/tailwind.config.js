export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 定义语义化颜色变量，方便后续统一调整主题
        primary: {
          50: '#eff6ff', // blue-50
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6', // blue-500 (Standard Blue)
          600: '#2563eb', // blue-600 (Action Blue)
          700: '#1d4ed8', // blue-700 (Deep Blue)
          800: '#1e40af', // blue-800 (Deeper Blue)
          900: '#1e3a8a', // blue-900 (Navy/Deep Sea)
        },
        gray: {
          // 使用 Slate (蓝灰色) 作为中性色，比纯灰更显高级和现代
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        }
      },
      fontFamily: {
        // 优化字体栈：英文字体优先 (Segoe UI 适配 Win11)，中文字体紧随其后
        sans: [
          '"Segoe UI"', 
          '"Microsoft YaHei"', 
          '"PingFang SC"', 
          'system-ui', 
          'sans-serif'
        ],
        // 等宽字体用于代码、ID、日志显示
        mono: [
          '"Consolas"', 
          '"Monaco"', 
          '"Courier New"', 
          'monospace'
        ],
      }
    },
  },
  plugins: [],
}
