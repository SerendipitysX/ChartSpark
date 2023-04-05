import { getLocal, setLocal } from '@/core/storage/local'
import { LANG } from '@/config/constants/app'
import { defineStore } from 'pinia'

const useLang = defineStore({
    id: 'lang', // id必填，且需要唯一
    state: () => ({
        lang: getLocal(LANG) || 'zhCn'
    }),

    actions: {
        changeLang(lang) {
            this.lang = lang
            setLocal(LANG, lang)
        }
    }
})

export default useLang