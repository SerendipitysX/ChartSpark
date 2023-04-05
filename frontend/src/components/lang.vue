<template>
    <el-button size="small">
        <el-dropdown teleported @command="saveWith">
            <span>
                {{ curLang }}
                <el-icon>
                    <ArrowDown />
                </el-icon>
            </span>
            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item command="zhCn">简体中文</el-dropdown-item>
                    <el-dropdown-item command="en">English</el-dropdown-item>
                    <el-dropdown-item command="pt">Portugal</el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
    </el-button>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { ArrowDown } from '@element-plus/icons-vue'
import useLang from '@/store/modules/lang'
const langStore = useLang()
const { locale } = useI18n()
const LANGMAP = {
    zhCn: '简体中文',
    en: 'English',
    pt: 'Portugal'
}

let curLang = ref(LANGMAP[langStore.lang])

const saveWith = type => {
    curLang.value = LANGMAP[type]
    locale.value = type
    langStore.changeLang(type)
}
</script>

<style lang="less" scoped>
.lang-wrap {
    display: inline-block;
}
</style>
