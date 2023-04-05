<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-05 22:33:57
 * @Description: 插入图片
-->

<template>
  <div style="display: inline-block">
    <el-button @click="insert" size="small">{{ t('insert_picture') }}</el-button>
    <el-dialog v-model="showModal" :title="t('please_choose')">
      <el-upload :before-upload="handleUpload">
        <el-button icon="ios-cloud-upload-outline">{{ t('select_image') }}</el-button>
      </el-upload>
      <template #footer>
        <el-button @click="showModal = false, imgFile = null" size="small">{{ t('alert.cancel') }}</el-button>
        <el-button @click="insertImgFile" size="small">{{ t('alert.confirm') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>


<script setup>
import { getImgStr } from "@/utils/utils";
import { v4 as uuid } from 'uuid';
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const canvas = inject("canvas")
let showModal = ref(false)
let imgFile = ref(null)
const insert = () => {
  imgFile.value = ''
  showModal.value = true
}
const insertImgFile = () => {
  const imgEl = document.createElement('img');
  imgEl.src = imgFile.value
  // 插入页面
  document.body.appendChild(imgEl);
  imgEl.onload = () => {
    // 创建图片对象
    const imgInstance = new fabric.Image(imgEl, {
      id: uuid(),
      // name: '图片1',
      left: 100, top: 100,
    });
    // 设置缩放
    imgInstance.scale(0.2);
    canvas.c.add(imgInstance)
    canvas.c.setActiveObject(imgInstance);
    canvas.c.renderAll()
    // 删除页面中的图片元素
    imgEl.remove()
  }
  showModal.value = false
}
// 选择文件
const handleUpload = (file) => {
  getImgStr(file).then(res => {
    imgFile.value = res
  })
}
</script>

<style scoped lang="less">

</style>
