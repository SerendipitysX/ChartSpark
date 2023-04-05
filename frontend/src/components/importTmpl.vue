<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-07 00:17:35
 * @Description: 导入模板
-->

<template>
  <div style="display:inline-block">
    <el-divider content-position="left">{{ t('title_template') }}</el-divider>
    <el-tooltip :content="item.label" v-for="(item, i) in  list" :key="i + '-bai1-button'" placement="top">
      <img class="tmpl-img" :alt="item.label" :src="item.src" @click="getTempData(item.tempUrl)" />
    </el-tooltip>
  </div>
</template>

<script setup>
import { downFontByJSON } from '@/utils/utils'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const canvas = inject("canvas")
const { proxy } = getCurrentInstance();
let jsonFile = ref(null)
let list = reactive([
  {
    label: '笔记模板',
    tempUrl: '../../template/073606d4-22de-491b-8b51-b90d72101d89.json',
    src: '../../template/073606d4-22de-491b-8b51-b90d72101d89.png',
  },
  {
    label: '醒目封面',
    tempUrl: '../../template/dcebee41-59b5-408b-a65a-c51bc390be3d.json',
    src: '../../template/dcebee41-59b5-408b-a65a-c51bc390be3d.png',
  },
  {
    label: '教师节',
    tempUrl: '../../template/3a7471f2-b8cf-4939-ad1a-a7d586768640.json',
    src: '../../template/3a7471f2-b8cf-4939-ad1a-a7d586768640.png',
  },
  {
    label: '升职锦囊',
    tempUrl: '../../template/ef5eb884-28e0-4d79-9e98-a73d759541f8.json',
    src: '../../template/ef5eb884-28e0-4d79-9e98-a73d759541f8.png',
  },
  {
    label: '古风模板',
    tempUrl: '../../template/ecc3fca2-f66e-465e-b2c7-80b7522fdb3b.json',
    src: '../../template/ecc3fca2-f66e-465e-b2c7-80b7522fdb3b.png',
  },
])
// 插入文件
const insertSvgFile = () => {
  // $Spin.show({
  //   render: (h) => {
  //     return h('div', '正在加载字体，您耐心等候...')
  //   }
  // });
  downFontByJSON(jsonFile.value).then(() => {
    // $Spin.hide();
    canvas.c.loadFromJSON(jsonFile.value, canvas.c.renderAll.bind(canvas.c));
  }).catch((e) => {
    // $Spin.hide();
    ElMessage(t('alert.loading_fonts_failed'))
  })
}
// 获取模板数据
const getTempData = (tmplUrl) => {
  // $Spin.show({
  //   render: (h) => {
  //     return h('div', '加载数据中...')
  //   }
  // });
  const getTemp = proxy.$http.get(tmplUrl)
  getTemp.then(res => {
    jsonFile.value = JSON.stringify(res.data)
    insertSvgFile()
  })
}
</script>

<style scoped lang="less">
.tmpl-img {
  width: 77px;
  cursor: pointer;
  margin-right: 5px;
}
</style>
