<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-04 00:21:58
 * @Description: 尺寸设置
-->

<template>
  <div>
    <el-divider content-position="left">{{ t('size') }}</el-divider>
    <el-form :label-width="40">
      <el-form-item :label="t('width')" prop="name">
        <el-input-number :max="2000" :min="1" v-model="width" @change="setSize" size="small"></el-input-number>
      </el-form-item>
      <el-form-item :label="t('height')" prop="name">
        <el-input-number :max="2000" :min="1" v-model="height" @change="setSize" size="small"></el-input-number>
      </el-form-item>
    </el-form>
    <el-divider content-position="left">{{ t('default_size') }}</el-divider>
    <el-button-group>
      <el-button v-for="(item, i) in presetSize" :key="i + 'presetSize'" size="small" style="text-align:left"
        @click="setSizeBy(item.width * item.scale, item.height * item.scale)">
        {{ item.label }}:{{ item.width }}x{{ item.height }}*{{ item.scale }}
      </el-button>
    </el-button-group>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
let width = ref(2000)
let height = ref(2000)
let presetSize = reactive([{
  label: '红书竖版',
  width: 900,
  height: 1200,
  scale: 0.5,
},
{
  label: '红书横版',
  width: 1200,
  height: 900,
  scale: 0.5,
},
{
  label: '手机壁纸',
  width: 1080,
  height: 1920,
  scale: 0.4,
},
])

const canvas = inject("canvas")
onMounted(() => {
  setSize()
})
const setSizeBy = (widthNum, heightNum) => {
  canvas.c.setWidth(widthNum);
  canvas.c.setHeight(heightNum);
  canvas.c.renderAll()
  width.value = widthNum
  height.value = heightNum
}
const setSize = () => {
  canvas.c.setWidth(width.value);
  canvas.c.setHeight(height.value);
  canvas.c.renderAll()
}
</script>

<style scoped lang="less">
.el-button-group {
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-start;
}

:deep(.ivu-form-item) {
  margin-bottom: 0;
}

:deep(.ivu-divider-plain.ivu-divider-with-text-left) {
  margin: 10px 0;
  font-weight: bold;
}
</style>
