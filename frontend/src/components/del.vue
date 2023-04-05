<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-03 22:35:59
 * @Description: 删除元素按钮
-->

<template>
  <el-button  @click="del" :icon="Delete" size="small"></el-button>
</template>


<script setup>
import { Delete } from '@element-plus/icons-vue'
let mSelectMode = inject('mSelectMode')
const canvas = inject("canvas")
const del = () => {
  const activeObject = canvas.c.getActiveObjects();
  activeObject && activeObject.map(item => canvas.c.remove(item))
  canvas.c.requestRenderAll()
  canvas.c.discardActiveObject()
}
</script>

<style scoped lang="less">

</style>
