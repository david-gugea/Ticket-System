const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: [
    'vue', // Add 'vue' to the list of dependencies to transpile
    '@vue/cli-service', // Add other dependencies if needed
    // ... other dependencies
  ],
})
