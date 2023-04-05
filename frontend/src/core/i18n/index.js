import { createI18n } from 'vue-i18n'
import { getLocal, setLocal } from '@/core/storage/local'
import { LANG } from '@/config/constants/app'

function getDefaultLang() {
    const localLang = getLocal(LANG)
    const defaultLang = localLang || import.meta.env.VITE_DEFAULT_LANG
    setLocal(LANG, defaultLang)
    return defaultLang
}


function loadLocaleMessages() {
    const locales = import.meta.globEager('./locales/*.json')
    const messages = {}
    const keysArr = Object.keys(locales)
    keysArr && keysArr.forEach(key => {
        const matched = key.match(/([A-Za-z0-9-_]+)\./i)
        if (matched && matched.length > 1) {
        const locale = matched[1]
        messages[locale] = locales[key]
        }
    })
    return messages
}

const lang = getDefaultLang()
export default createI18n({
    locale: lang,
    fallbackLocale: lang,
    messages: loadLocaleMessages(),
    enableInSFC: false,
    legacy: false
})
