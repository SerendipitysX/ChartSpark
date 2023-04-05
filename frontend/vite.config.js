import { defineConfig } from 'vite'
import createVitePlugins from './vite/plugins'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: createVitePlugins(),
  // vite 相关配置
  server: {
    port: 80,
    host: true,
    open: true
  },
  resolve: {
    // https://cn.vitejs.dev/config/#resolve-alias
    alias: {
      // 设置路径
      '~': path.resolve(__dirname, './'),
      // 设置别名
      '@': path.resolve(__dirname, './src')
    },
    // https://cn.vitejs.dev/config/#resolve-extensions
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue']
  },
})
