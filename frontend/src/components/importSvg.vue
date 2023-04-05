<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-05 22:36:02
 * @Description: 插入SVG元素
-->

<template>
  <div style="display:inline-block">
    <el-button @click="insert" size="small">{{ t('insert_svg') }}</el-button>
    <el-dialog v-model="showModal" :title="t('please_choose')" @on-ok="insertSvg" @on-cancel="showModal = false">
      <el-radio-group v-model="insertType" style="padding-bottom:  10px">
        <el-radio-button label="string">{{ t('string') }}</el-radio-button>
        <el-radio-button label="file">{{ t('file') }}</el-radio-button>
      </el-radio-group>
      <!-- 字符串 -->
      <el-input v-if="insertType === 'string'" v-model="svgStr" type="textarea" placeholder="请输入SVG字符" />
      <!-- 文件 -->
      <el-upload v-if="insertType === 'file'" :before-upload="handleUpload">
        <el-button :icon="UploadFilled">{{ t('select_svg') }}</el-button>
      </el-upload>

      <template #footer>
        <el-button @click="showModal = false" size="small">{{ t('alert.cancel') }}</el-button>
        <el-button @click="insertSvg" size="small">{{ t('alert.confirm') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { UploadFilled } from '@element-plus/icons-vue'
import { getImgStr } from "@/utils/utils";
import { v4 as uuid } from 'uuid';
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const fabric = inject("fabric")
const canvas = inject("canvas")
let insertType = ref('string')
let showModal = ref(false)
let svgStr = ref('')
let svgFile = ref(null)
const insert = () => {
  svgStr.value = ''
  svgFile.value = null
  showModal.value = true
}
const insertSvg = () => {
  if (insertType.value === 'string') {
    insertSvgStr()
  } else {
    insertSvgFile()
  }
  showModal.value = false
}
// 插入字符串元素
const insertSvgStr = () => {
  fabric.loadSVGFromString(svgStr.value, function (objects, options) {
    const item = fabric.util.groupSVGElements(objects, { ...options, name: 'defaultSVG', id: uuid() });
    canvas.c.add(item).centerObject(item).renderAll();
  });
}
// 插入文件元素
const insertSvgFile = () => {
  fabric.loadSVGFromURL(svgFile.value, function (objects, options) {
    const item = fabric.util.groupSVGElements(objects, { ...options, name: 'defaultSVG', id: uuid() });
    canvas.c.add(item).centerObject(item).renderAll();
  });
}
const handleUpload = (file) => {
  getImgStr(file).then(res => {
    svgFile.value = res
  })
}
</script>

<style scoped lang="less">

</style>
