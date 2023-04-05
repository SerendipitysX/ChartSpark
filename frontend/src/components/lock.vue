<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-12-07 23:55:56
 * @Description: 锁定元素
-->

<template>
  <!-- <el-switch v-if="mSelectMode === 'one'" v-model="isLock" inline-prompt :active-icon="Check" :inactive-icon="Close"
    @change="doLock">
  </el-switch> -->
  <el-switch  v-model="isLock" inline-prompt :active-icon="Check" :inactive-icon="Close"
    @change="doLock">
  </el-switch>
</template>

<script setup>
import { Check, Close } from '@element-plus/icons-vue'
let mSelectMode = inject('mSelectMode')
let canvas = inject('canvas')
// let mSelectActive = inject('mSelectActive')
let mSelectActive = ref({})
let isLock = ref(false)
let event = inject('event')
const lockAttrs = ['lockMovementX', 'lockMovementY', 'lockRotation', 'lockScalingX', 'lockScalingY']

onMounted(() => {
  event.on('selectOne', (items) => {
    isLock.value = !items[0].hasControls
    mSelectActive.value = items[0]
  })
})
const doLock = (isLock) => {
  isLock ? lock() : unLock()
}
const lock = () => {
  // 修改自定义属性
  mSelectActive.value.hasControls = false
  // 修改默认属性
  lockAttrs.forEach(key => {
    mSelectActive.value[key] = true
  })

  mSelectActive.value.selectable = false

  isLock.value = true
  canvas.c.renderAll()
}
const unLock = () => {
  // 修改自定义属性
  mSelectActive.value.hasControls = true
  // 修改默认属性
  lockAttrs.forEach(key => {
    mSelectActive.value[key] = false
  })
  mSelectActive.value.selectable = true

  isLock.value = false
  canvas.c.renderAll()
}
</script>

<style scoped lang="less">
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
