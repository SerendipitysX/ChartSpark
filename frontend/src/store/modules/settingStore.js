import { defineStore } from 'pinia'

export const useJsonStore = defineStore('jsonStoreId', {
  // 为了完整类型推理，推荐使用箭头函数
  state: () => {
    return {
      // 所有这些属性都将自动推断出它们的类型
      jsonData: {"y":[1]},
    }
  },
})

export const useSettingStore = defineStore('settingStoreId', {
  // 为了完整类型推理，推荐使用箭头函数
  state: () => {
    return {
      // 所有这些属性都将自动推断出它们的类型
      isActiveBar: Boolean,
      isActiveLine: Boolean,
      isActivePie: Boolean,
      isActiveScatter: Boolean,
      isActivePreview: Boolean,
    }
  },
})


