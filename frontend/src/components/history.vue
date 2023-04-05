<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-03 22:57:06
 * @Description: 回退重做
-->

<template>
  <el-button-group v-if=false size="small" style="margin-top: 11px; margin-bottom: -10px;">
    <!-- 后退 -->
    <el-button @click="undo" :disabled="!list.length">
      <el-icon class="el-icon--right">
        <ArrowLeft />
      </el-icon>{{ list.length }}
    </el-button>
    <!-- 重做 -->
    <el-button @click="redo" :disabled="!redoList.length">
      <el-icon class="el-icon--right">
        <ArrowRight />
      </el-icon>{{ redoList.length }}
    </el-button>
  </el-button-group>
</template>

<script setup>
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import onHotKeys from '@/core/hotkeys'
import keyNames from '@/core/hotkeys/constantKey'
const canvas = inject("canvas")

const maxStep = 10

let redoList = ref([])
let list = ref([])

onMounted(() => {
  // 有更新时记录进度
  canvas.c.on({
    'object:modified': save,
    'selection:updated': save,
  });
  onHotKeys(keyNames.ctrlz, undo)

  // EventBus.on('historyUndo', undo)
  // $once('hook:beforeDestroy', () => {
  //   EventBus.off('historyUndo', undo)
  // })
})


// 保存记录
const save = () => {
  const data = canvas.c.toJSON(['id'])
  if (list.value.length > maxStep) {
    list.value.shift()
  }
  list.value.push(data)
}
// 后退
const undo = () => {
  if (list.value.length) {
    const item = list.value.pop()
    redoList.value.push(item)
    renderCanvas(item)
  }
}
// 重做
const redo = () => {
  if (redoList.value.length) {
    const item = redoList.value.pop()
    list.value.push(item)
    renderCanvas(item)
  }
}
// 根据数据渲染
const renderCanvas = (data) => {
  canvas.c.clear();
  canvas.c.loadFromJSON(data, canvas.c.renderAll.bind(canvas.c));
  canvas.c.requestRenderAll();
}
</script>

<style scoped lang="less">
span.active {
  svg.icon {
    fill: #2d8cf0;
  }
}
</style>