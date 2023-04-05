<template>
  <el-config-provider :locale="elLocale">
    <router-view />
  </el-config-provider>
</template>

<script setup>
// element-plus语言包
import zhCn from 'element-plus/dist/locale/zh-cn'
import en from 'element-plus/dist/locale/en'
import pt from 'element-plus/dist/locale/pt'
import useLang from '@/store/modules/lang'
const langStore = useLang()

const ELEMENTLANGMAP = {
  zhCn,
  en,
  pt
}

const elLocale = computed(() => ELEMENTLANGMAP[langStore.lang] || zhCn) 

</script>

<style lang="less">
svg {
  vertical-align: text-top;
}
.el-button--small {
  padding: 5px 7px;
}
</style>
