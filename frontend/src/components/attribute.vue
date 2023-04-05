<template>
  <div class="box" >
    <!-- 字体属性 -->
    <div >
      <el-divider content-position="left">{{ t('attributes.font') }}</el-divider>
      <el-form label-position="left" :label-width="40">
        <el-form-item :label="t('size')">
          <el-input-number v-model="fontAttr.fontSize" @change="(value) => changeCommon('fontSize', value)"
            size="small">
          </el-input-number>
        </el-form-item>
        <el-form-item :label="t('attributes.font')">
          <el-select v-model="fontAttr.fontFamily" @change="changeFontFamily" size="small">
            <el-option v-for="item in fontFamilyList" :value="item" :key="'font-' + item">{{ item }}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item :label="t('background')">
          <el-color-picker v-model="fontAttr.textBackgroundColor"
            @change="(value) => changeCommon('textBackgroundColor', value)" show-alpha size="small" />
        </el-form-item>
        <el-form-item :label="t('attributes.align')">
          <el-radio-group v-model="fontAttr.textAlign" @change="(value) => changeCommon('textAlign', value)"
            size="small" type="button">
            <el-radio v-for="(item, i) in textAlignList" :label="item" :key="item">
              <span v-html="textAlignListSvg[i]"></span>
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <div style="padding: 5px 0">
          {{ t('attributes.bold') }}<el-switch v-model="fontAttr.fontWeight" active-value="bold" inactive-value="normal" size="small"
            @change="(value) => changeCommon('fontWeight', value)" />
            {{ t('attributes.italic') }} <el-switch v-model="fontAttr.fontStyle" active-value="italic" inactive-value="normal" size="small"
            @on-change="(value) => changeCommon('fontStyle', value)" />
          <br />
          {{ t('attributes.underline') }} <el-switch v-model="fontAttr.underline" size="small"
            @change="(value) => changeCommon('underline', value)" />
          {{ t('attributes.stroke') }}<el-switch v-model="fontAttr.linethrough" size="small"
            @change="(value) => changeCommon('linethrough', value)" />
          <br />
          {{ t('attributes.swipe_up') }} <el-switch v-model="fontAttr.overline" size="small"
            @change="(value) => changeCommon('overline', value)" />
        </div>

        <el-form-item :label="t('attributes.line_height')">
          <el-input-number v-model="fontAttr.lineHeight" @change="(value) => changeCommon('lineHeight', value)"
            size="small" :step="0.1"></el-input-number>
        </el-form-item>

        <el-form-item :label="t('attributes.char_spacing')">
          <el-input-number v-model="fontAttr.charSpacing" @change="(value) => changeCommon('charSpacing', value)"
            size="small"></el-input-number>
        </el-form-item>
      </el-form>
    </div>
    <!-- 通用属性 -->
    <div >
      <el-divider content-position="left">{{ t('attributes.exterior') }}</el-divider>
      <el-form label-position="left" :label-width="40">
        <el-form-item :label="t('color')">
          <el-color-picker v-model="baseAttr.fill" @change="(value) => changeCommon('fill', value)" show-alpha
            size="small" />
        </el-form-item>
        <el-form-item :label="t('attributes.angle')">
          <el-input-number v-model="baseAttr.angle" :max="360" @change="(value) => changeCommon('angle', value)"
            size="small">
          </el-input-number>
        </el-form-item>
        <el-form-item :label="t('attributes.left')">
          <el-input-number v-model="baseAttr.left" :max="360" @change="(value) => changeCommon('left', value)"
            size="small"></el-input-number>
        </el-form-item>
        <el-form-item :label="t('attributes.top')">
          <el-input-number v-model="baseAttr.top" :max="360" @change="(value) => changeCommon('top', value)"
            size="small"></el-input-number>
        </el-form-item>
        <el-form-item :label="t('attributes.opacity')">
          <el-slider v-model="baseAttr.opacity" @change="(value) => changeCommon('opacity', value)" size="small">
          </el-slider>
        </el-form-item>
      </el-form>
      <el-divider content-position="left">{{ t('attributes.stroke') }}</el-divider>
      <el-form label-position="left" :label-width="40">
        <el-form-item :label="t('width')">
          <el-input-number v-model="baseAttr.strokeWidth" :max="360"
            @change="(value) => changeCommon('strokeWidth', value)" show-input size="small"></el-input-number>
        </el-form-item>
        <el-form-item :label="t('color')">
          <el-color-picker v-model="baseAttr.stroke" @change="(value) => changeCommon('stroke', value)" show-alpha
            size="small" />
        </el-form-item>
      </el-form>

      <el-divider content-position="left">{{ t('attributes.shadow') }}</el-divider>
      <el-form label-position="left" :label-width="40">
        <el-form-item :label="t('color')">
          <el-color-picker size="small" v-model="baseAttr.shadow.color"
            @change="(value) => changeShadow('color', value)" show-alpha />
        </el-form-item>
        <el-form-item :label="t('attributes.blur')">
          <el-input-number v-model="baseAttr.shadow.blur" :max="360" @change="(value) => changeShadow('blur', value)"
            size="small"></el-input-number>
        </el-form-item>
        <el-form-item :label="t('attributes.offset_x')">
          <el-input-number v-model="baseAttr.shadow.offsetX" :max="360"
            @change="(value) => changeShadow('offsetX', value)" size="small"></el-input-number>
        </el-form-item>
        <el-form-item :label="t('attributes.offset_y')">
          <el-input-number v-model="baseAttr.shadow.offsetY" :max="360"
            @change="(value) => changeShadow('offsetY', value)" size="small"></el-input-number>
        </el-form-item>
      </el-form>
    </div>

    <!-- 图片属性 -->
    <!-- <div>
      <el-divider content-position="left">{{ t('attributes.picture_filter') }}</el-divider>
      {{ t('attributes.blur') }}: <el-slider v-model="imgAttr.blur" :max="1" :min="0" :step="0.1" @change="imgBlur" show-input
        size="small"></el-slider>
    </div> -->
  </div>
</template>


<script setup>
import FontFaceObserver from 'fontfaceobserver'
import fontList from "@/assets/fonts/font";
import { ElMessage } from 'element-plus';
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
let event = inject('event')
let canvas = inject('canvas')
let mSelectMode = inject('mSelectMode')
let mSelectOneType = inject('mSelectOneType')



// 通用元素
let baseType = ref(['text', 'i-text', 'textbox', 'rect', 'circle', 'triangle', 'image', 'group'])

// 文字元素
let textType = ref(['i-text', 'textbox', 'text'])
// 图片元素
let imgType = ref(['image'])
// 通用属性
let baseAttr = reactive({
  opacity: 0,
  angle: 0,
  fill: '#fff',
  left: 0,
  top: 0,
  strokeWidth: 0,
  stroke: '#fff',
  shadow: {
    color: '#fff',
    blur: 0,
    offsetX: 0,
    offsetY: 0,
  }
})
// 字体属性
let fontAttr = reactive({
  fontSize: 0,
  fontFamily: '',
  lineHeight: 0,
  charSpacing: 0,
  fontWeight: '',
  textBackgroundColor: '#fff',
  textAlign: '',
  fontStyle: '',
  underline: false,
  linethrough: false,
  overline: false
})
// 图片属性
let imgAttr = reactive({
  blur: 0,
})
// 字体下拉列表
let fontFamilyList = ref(fontList.map(item => item.fontFamily))
// 字体对齐方式
let textAlignList = ref(['left', 'center', 'right'])
// 对齐图标
let textAlignListSvg = ref(['<svg t="1650441458823" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3554" width="14" height="14"><path d="M198.4 198.4h341.333333c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533334 19.2v57.6c0 8.533333-2.133333 14.933333-8.533334 19.2-6.4 6.4-12.8 8.533333-19.2 8.533334h-341.333333c-8.533333 0-14.933333-2.133333-19.2-8.533334-6.4-6.4-8.533333-12.8-8.533333-19.2v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 4.266667-4.266667 12.8-8.533333 19.2-8.533333z m0 170.666667h569.6c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533333h-569.6c-8.533333 0-14.933333-2.133333-19.2-8.533333-6.4-6.4-8.533333-12.8-8.533333-19.2v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 4.266667-4.266667 12.8-8.533333 19.2-8.533333z m0 170.666666h454.4c8.533333 0 14.933333 2.133333 19.2 8.533334 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533333h-454.4c-8.533333 0-14.933333-2.133333-19.2-8.533333-6.4-6.4-8.533333-12.8-8.533333-19.2v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 4.266667-4.266667 12.8-8.533333 19.2-8.533334z m0 170.666667h625.066667c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533334h-625.066667c-8.533333 0-14.933333-2.133333-19.2-8.533334-6.4-6.4-8.533333-12.8-8.533333-19.2v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 4.266667-4.266667 12.8-8.533333 19.2-8.533333z" p-id="3555"></path></svg>', '<svg t="1650441512015" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3704" width="14" height="14"><path d="M313.6 198.4h398.933333c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533334 19.2v57.6c0 8.533333-2.133333 14.933333-8.533334 19.2-6.4 6.4-12.8 8.533333-19.2 8.533334h-398.933333c-8.533333 0-14.933333-2.133333-19.2-8.533334-6.4-6.4-8.533333-12.8-8.533333-19.2v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 4.266667-4.266667 10.666667-8.533333 19.2-8.533333z m-115.2 170.666667h625.066667c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533333h-625.066667c-8.533333 0-14.933333-2.133333-19.2-8.533333-6.4-6.4-8.533333-12.8-8.533333-19.2v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 4.266667-4.266667 12.8-8.533333 19.2-8.533333z m115.2 170.666666h398.933333c8.533333 0 14.933333 2.133333 19.2 8.533334 6.4 6.4 8.533333 12.8 8.533334 19.2v57.6c0 8.533333-2.133333 14.933333-8.533334 19.2-6.4 6.4-12.8 8.533333-19.2 8.533333h-398.933333c-8.533333 0-14.933333-2.133333-19.2-8.533333-6.4-6.4-8.533333-12.8-8.533333-19.2v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 4.266667-4.266667 10.666667-8.533333 19.2-8.533334z m-115.2 170.666667h625.066667c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533334h-625.066667c-8.533333 0-14.933333-2.133333-19.2-8.533334-6.4-6.4-8.533333-12.8-8.533333-19.2v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 4.266667-4.266667 12.8-8.533333 19.2-8.533333z" p-id="3705"></path></svg>', '<svg t="1650441519862" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3854" width="14" height="14"><path d="M454.4 283.733333v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 6.4-6.4 12.8-8.533333 19.2-8.533333h341.333334c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533334h-341.333334c-8.533333 0-14.933333-2.133333-19.2-8.533334-4.266667-4.266667-8.533333-10.666667-8.533333-19.2z m-226.133333 170.666667v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 6.4-6.4 12.8-8.533333 19.2-8.533333h569.6c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533333H256c-8.533333 0-14.933333-2.133333-19.2-8.533333-6.4-4.266667-8.533333-10.666667-8.533333-19.2z m113.066666 170.666667v-57.6c0-8.533333 2.133333-14.933333 8.533334-19.2 6.4-6.4 12.8-8.533333 19.2-8.533334h454.4c8.533333 0 14.933333 2.133333 19.2 8.533334 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533333h-454.4c-8.533333 0-14.933333-2.133333-19.2-8.533333-6.4-4.266667-8.533333-10.666667-8.533334-19.2z m-170.666666 170.666666v-57.6c0-8.533333 2.133333-14.933333 8.533333-19.2 6.4-6.4 12.8-8.533333 19.2-8.533333h625.066667c8.533333 0 14.933333 2.133333 19.2 8.533333 6.4 6.4 8.533333 12.8 8.533333 19.2v57.6c0 8.533333-2.133333 14.933333-8.533333 19.2-6.4 6.4-12.8 8.533333-19.2 8.533334h-625.066667c-8.533333 0-14.933333-2.133333-19.2-8.533334-6.4-4.266667-8.533333-10.666667-8.533333-19.2z" p-id="3855"></path></svg>'])

onMounted(() => {
  event.on('selectOne', (e) => {
    const activeObject = canvas.c.getActiveObjects()[0];
    if (activeObject) {
      // base
      baseAttr.opacity = activeObject.get('opacity') * 100
      baseAttr.fill = activeObject.get('fill')
      baseAttr.left = activeObject.get('left')
      baseAttr.top = activeObject.get('top')
      baseAttr.stroke = activeObject.get('stroke')
      baseAttr.strokeWidth = activeObject.get('strokeWidth')
      baseAttr.shadow = activeObject.get('shadow') || {}
      if (activeObject.type === 'i-text' || activeObject.type === 'text' || activeObject.type === 'textbox') {
        fontAttr.fontSize = activeObject.get('fontSize')
        fontAttr.fontFamily = activeObject.get('fontFamily')
        fontAttr.lineHeight = activeObject.get('lineHeight')
        fontAttr.textAlign = activeObject.get('textAlign')
        fontAttr.underline = activeObject.get('underline')
        fontAttr.linethrough = activeObject.get('linethrough')
        fontAttr.charSpacing = activeObject.get('charSpacing')
        fontAttr.overline = activeObject.get('overline')
        fontAttr.fontStyle = activeObject.get('fontStyle')
        fontAttr.textBackgroundColor = activeObject.get('textBackgroundColor')
        fontAttr.fontWeight = activeObject.get('fontWeight')
      }

      // 图片滤镜
      if (activeObject.type === 'image') {
        imgAttr.blur = activeObject.filters[0] ? activeObject.filters[0].blur : 0
      }
    }
  })
})

// 图片属性
const imgBlur = (blur) => {
  const activeObject = canvas.c.getActiveObjects()[0]
  if (activeObject) {
    const filter = new fabric.Image.filters.Blur({ blur });
    activeObject.filters = [filter]
    activeObject.applyFilters();
    canvas.c.renderAll()
  }
}
// 修改字体
const changeFontFamily = (fontName) => {
  if (!fontName) return

  // 跳过加载的属性
  const skipFonts = ['arial', 'Microsoft YaHei']
  if (skipFonts.includes(fontName)) {
    const activeObject = canvas.c.getActiveObjects()[0]
    activeObject && activeObject.set('fontFamily', fontName);
    canvas.c.renderAll()
    return
  }
  // 字体加载
  var font = new FontFaceObserver(fontName);
  font.load(null, 150000).then(() => {
    const activeObject = canvas.c.getActiveObjects()[0]
    activeObject && activeObject.set('fontFamily', fontName);
    canvas.c.renderAll()
  }).catch((err) => {
    ElMessage.error(err)
  })
}
// 通用属性改变
const changeCommon = (key, value) => {
  const activeObject = canvas.c.getActiveObjects()[0]
  // 透明度特殊转换
  if (key === 'opacity') {
    activeObject && activeObject.set(key, value / 100)
    canvas.c.renderAll()
    return
  }
  activeObject && activeObject.set(key, value)
  canvas.c.renderAll()
}
// 阴影设置
const changeShadow = () => {
  const activeObject = canvas.c.getActiveObjects()[0]
  activeObject && activeObject.set('shadow', new fabric.Shadow(baseAttr.shadow));
  canvas.c.renderAll()
}
</script>
<style scoped lang="less">
:deep(.ivu-form-item) {
  margin-bottom: 0;
}

:deep(.ivu-color-picker) {
  display: block;
}

:deep(.ivu-input-number) {
  display: block;
  width: 100%;
  top: 4px;
}

:deep(.ivu-divider-.ivu-divider-with-text-left) {
  margin: 10px 0;
  font-weight: bold;
}
</style>
