<template>
  <div>
    <el-divider content-position="left">{{ t('color') }}</el-divider>
    <el-form :label-width="40">
      <el-form-item :label="t('color')" prop="name">
        <el-color-picker v-model="color" @change="setThisColor" size="small" />
      </el-form-item>
      <el-form-item :label="t('picture')" prop="name">
        <el-button @click="insert" :icon="UploadFilled" size="small">
          {{ t('upload_background') }}
        </el-button>
      </el-form-item>
    </el-form>
    <el-divider content-position="left">{{ t('color_macthing') }}</el-divider>
    <div class="color-list">
      <template v-for="(item, i) in colorList" :key="item.label + i">
        <div class="item">
          <em style="font-size:small">{{ item.label }}:</em>
          <span v-for="color in item.color" :key="color" :style="`background:${color}`" @click="setColor(color)"></span>
        </div>
      </template>
    </div>
    <el-divider content-position="left">{{ t('background_texture') }}</el-divider>
    <div>
      <img src="@/assets/1.png" @click="(e) => setBgImg(e.target)" class="img" />
      <img src="@/assets/2.png" @click="(e) => setBgImg(e.target)" class="img" alt="" />
      <img src="@/assets/3.png" @click="(e) => setBgImg(e.target)" class="img" alt="" />
      <img src="@/assets/4.png" @click="(e) => setBgImg(e.target)" class="img" alt="" />
      <img src="@/assets/5.png" @click="(e) => setBgImg(e.target)" class="img" alt="" />
    </div>
    <el-dialog v-model="showModal" :title="t('alert.select_image')">
      <el-upload :before-upload="handleUpload" action="#" :auto-upload="false">
        <el-button :icon="UploadFilled">{{ t('select_image') }}</el-button>
      </el-upload>
      <template #footer>
        <el-button @click="showModal = false" size="small">{{ t('alert.cancel') }}</el-button>
        <el-button @click="insertImgFile" size="small">{{ t('alert.confirm') }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { getImgStr } from "@/utils/utils";
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
let showModal = ref(false)
let color = ref('')
let imgFile = ref('')
let colorList = reactive([
  {
    label: t('scenary_x', { number: 1 }),
    color: ['#5F2B63', '#B23554', '#F27E56', '#FCE766']
  },
  {
    label: t('scenary_x', { number: 2 }),
    color: ['#86DCCD', '#E7FDCB', '#FFDC84', '#F57677']
  },
  {
    label: t('scenary_x', { number: 3 }),
    color: ['#5FC2C7', '#98DFE5', '#C2EFF3', '#DDFDFD']
  },
  {
    label: t('scenary_x', { number: 4 }),
    color: ['#9EE9D3', '#2FC6C8', '#2D7A9D', '#48466d']
  },
  {
    label: t('scenary_x', { number: 5 }),
    color: ['#61c0bf', '#bbded6', '#fae3d9', '#ffb6b9']
  },
  {
    label: t('scenary_x', { number: 6 }),
    color: ['#ffaaa5', '#ffd3b6', '#dcedc1', '#a8e6cf']
  }
])

const canvas = inject("canvas")
const fabric = inject("fabric")
// 设置背景图片
const setBgImg = (target) => {
  const imgEl = target.cloneNode(true);
  imgEl.onload = () => {
    // 可跨域设置
    const imgInstance = new fabric.Image(imgEl, { crossOrigin: 'anonymous' });
    // 渲染背景
    canvas.c.setBackgroundImage(imgInstance, canvas.c.renderAll.bind(canvas.c), {
      scaleX: canvas.c.width / imgInstance.width,
      scaleY: canvas.c.width / imgInstance.width,
    });
    canvas.c.renderAll()
    canvas.c.requestRenderAll();
  }
}
// 清空文件 展示文件框
const insert = () => {
  imgFile.value = ''
  showModal.value = true
}
// 确认插入图片
const insertImgFile = () => {
  if (imgFile.value === '') {
    return ElMessage.error(t('alert.select_file'))
  }
  const imgEl = document.createElement('img');
  imgEl.src = imgFile.value
  // 插入页面
  document.body.appendChild(imgEl);
  imgEl.onload = () => {
    setBgImg(imgEl)
    imgEl.remove()
  }
}
// 文件选择
const handleUpload = (file) => {
  getImgStr(file).then(res => {
    imgFile.value = res
  })
}
// 背景颜色设置
const setThisColor = () => {
  setColor(color.value)
}
// 背景颜色设置
const setColor = (color) => {
  canvas.c.setBackgroundColor(color, canvas.c.renderAll.bind(canvas.c))
  canvas.c.backgroundImage = ''
  canvas.c.renderAll()
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
:deep(.ivu-form-item) {
  margin-bottom: 0;
}

.img {
  width: 50px;
  padding: 5px;
  background: #f5f5f5;
  margin-left: 2px;
  height: 70px;
  cursor: pointer;
}

.color-list {
  padding: 10px 0;

  .item {
    padding-bottom: 5px;
  }

  span {
    display: inline-block;
    margin-left: 6px;
    background: #f5f5f5;
    height: 20px;
    width: 20px;
    font-size: 12px;
    line-height: 20px;
    vertical-align: middle;
    cursor: pointer;
  }
}

:deep(.ivu-divider-plain.ivu-divider-with-text-left) {
  margin: 10px 0;
  font-weight: bold;
}
</style>
