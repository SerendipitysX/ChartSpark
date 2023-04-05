import { defineStore } from 'pinia'

export const useGenerateStore = defineStore('generateStoreId', {
  // 为了完整类型推理，推荐使用箭头函数
  state: () => {
    return {
      // 所有这些属性都将自动推断出它们的类型
      objectText: String,
      descriptionText: String,
      generateMethod: String,
      guide:String,
      generationStateList: [],
      generateNum: 4,
      isClickRow: false
    }
  },
})


