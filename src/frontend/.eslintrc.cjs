/* eslint-env node */
module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    // Vue 3 supports multiple v-models and v-model arguments
    'vue/no-v-model-argument': 'off',
    'vue/multi-word-component-names': 'off',
    'no-unused-vars': 'warn'
  }
}
