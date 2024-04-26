<template>
  <el-container>
    <el-header v-if="show" style="background-color: #3E3E3E;">
      <!-- 171717 -->
      <!-- 导入 -->
      <import-json></import-json>
      &nbsp;
      <!-- <import-svg></import-svg> -->
      &nbsp;
      <import-img></import-img>
      &nbsp;
      <!-- <group></group> -->
      <!-- <lock></lock> -->
      <!-- 对齐方式 -->
      <align></align>
      &nbsp;
      <flip></flip>
      &nbsp;
      <center-align></center-align>
      &nbsp;
      <group></group>
      <!-- &nbsp; -->
      <!-- <zoom></zoom> -->
      &nbsp;
      <!-- <lock></lock> -->
      <!-- &nbsp; -->
      <!-- <dele></dele>
      <clone></clone> -->
      <!-- <flip></flip> -->
      <div style=" float:right;">
        <!-- <zoom></zoom>&nbsp; &nbsp; -->
        <lang />
        <save></save>
      </div>
    </el-header>
    <el-main style="display: flex; height: calc(100vh - 64px);background-color: #F1F1F1;">
      <div class="left-panel" v-if="show" style="width: 500px; height: 99%;margin-top:12px;">
        <settings v-if="show"></settings>
        <!-- <rawData v-if="show"></rawData> -->
        <!-- <theme v-if="show"></theme> -->
        <textInput v-if="show"></textInput>
      </div>

      <!-- 画布区域 -->
      <div style="width: 100%; height: 98%;  margin-left: 3px;margin-top: 2px; overflow: hidden; background:#F1F1F1;">
        <div class="canvas-box">
          <canvas id="canvas"></canvas>
        </div>
        <div class="candidate-box0">
          <toolGallery ></toolGallery>
        </div>
        <div class="candidate-box">
          <gallery ></gallery>
        </div>
      </div>
      <!-- 属性区域 -->
      <div style="width: 500px; height: 100%; padding-left:10px; overflow-y: auto; background:#F1F1F1">
        <history v-if="show"></history>
        <estimation v-if="show"></estimation>
        <edit v-if="show"></edit>
        <layer v-if="show"></layer>
        <!-- <attribute v-if="show"></attribute> -->
      </div>
    </el-main>
  </el-container>
</template>

<script setup>
import { Promotion, EditPen, Operation } from '@element-plus/icons-vue'
// 导入元素
import importJson from '@/components/importJSON.vue'
import importSvg from '@/components/importSvg.vue'
import importImg from '@/components/importImg.vue'

// 顶部组件
import align from '@/components/align.vue'
import centerAlign from '@/components/centerAlign.vue'
import flip from '@/components/flip.vue'
import save from '@/components/save.vue'
import clone from '@/components/clone.vue'
import group from '@/components/group.vue'
import zoom from '@/components/zoom.vue'
import lock from '@/components/lock.vue'
import dele from '@/components/del.vue'
import lang from '@/components/lang.vue'
// 左侧组件
import settings from '@/components/settings.vue'
import textInput from '@/components/textInput.vue'
import gallery from '@/components/gallery.vue'
import toolGallery from '@/components/toolGallery.vue'
import tools from '@/components/tools.vue'
import setSize from '@/components/setSize.vue'

// 右侧组件
import history from '@/components/history.vue'
import layer from '@/components/layer.vue'
import edit from '@/components/edit.vue'
import estimation from '@/components/estimation.vue'

// 功能组件
import EventHandle from '@/utils/eventHandler'
import { fabric } from 'fabric';

// 对齐辅助线
import initAligningGuidelines from '@/core/initAligningGuidelines';
import initControlsRotate from '@/core/initControlsRotate';
import initHotkeys from '@/core/initHotKeys';
import initControls from '@/core/initControls';

//国际化
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

let mSelectMode = ref('') // one | multiple
let mSelectOneType = ref('') // i-text | group...
let mSelectId = ref('')// 选择id
let mSelectIds = ref([])// 选择id

let event = new EventHandle()
let canvas = {}


event.setMaxListeners(50)
provide("canvas", canvas)
provide("fabric", fabric)
provide("event", event)
provide("mSelectMode", mSelectMode)
provide("mSelectOneType", mSelectOneType)
provide("mSelectId", mSelectId)
provide("mSelectIds", mSelectIds)
let menuActive = ref('1')
let show = ref(false)

onMounted(() => {
  event.on('selectOne', (e) => {
    mSelectMode.value = 'one'
    mSelectId.value = e[0].id
    mSelectOneType.value = e[0].type
    mSelectIds.value = e.map(item => item.id)
  })

  event.on('selectMultiple', (e) => {
    mSelectMode.value = 'multiple'
    mSelectId.value = ''
    mSelectIds.value = e.map(item => item.id)
  })

  event.on('selectCancel', () => {
    mSelectId.value = ''
    mSelectIds.value = []
    mSelectMode.value = ''
    mSelectOneType.value = ''
  })


  canvas.c = new fabric.Canvas('canvas');
  canvas = canvas.c
  canvas.set('backgroundColor', '#fff')
  canvas.setWidth(2000);
  canvas.setHeight(2000);
  // let dotGrid = [];
  // for (let row = 0; row < 40; row++) {
  //   for (let col = 0; col < 40; col++) {
  //     let dot = new fabric.Circle({
  //       radius: 1.5,
  //       fill: '#CCCCCC',
  //       selectable: false,
  //       evented: false,
  //       left: col * 20,
  //       top: row * 20
  //     });
  //     dotGrid.push(dot);
  //   }
  // }
  // let dotGroup = fabric.util.groupSVGElements(dotGrid, {
  //   originX: 'left',
  //   originY: 'top'
  // });

  // dotGroup.selectable = false

  // canvas.add(dotGroup);
  canvas.renderAll()

  show.value = true

  windowsLoadEvt(canvas)

  event.init(canvas)
  initAligningGuidelines(canvas)
  initHotkeys(canvas)
  initControls(canvas)
  initControlsRotate(canvas)
})

//获取鼠标坐标
function getMouse(e) {
  var pointer = canvas.getPointer(e.e);
  var posX = Math.floor(pointer.x);
  var posY = Math.floor(pointer.y);
  console.log(posX + " " + posY);
}

const windowsLoadEvt = (canvas) => {
  canvas.on('mouse:down', (e) => {
    getMouse(e);
  });

  canvas.on('mouse:down', opt => { // 鼠标按下时触发
    let evt = opt.e
    if (evt.altKey === true) { // 是否按住alt
      canvas.selection = false;
      canvas.isDragging = true // isDragging 是自定义的
      canvas.lastPosX = evt.clientX // lastPosX 是自定义的
      canvas.lastPosY = evt.clientY // lastPosY 是自定义的
    }
  })

  canvas.on('mouse:move', opt => { // 鼠标移动时触发
    if (canvas.isDragging) {
      let evt = opt.e
      let vpt = canvas.viewportTransform // 聚焦视图的转换
      vpt[4] += evt.clientX - canvas.lastPosX
      vpt[5] += evt.clientY - canvas.lastPosY
      canvas.requestRenderAll()
      canvas.lastPosX = evt.clientX
      canvas.lastPosY = evt.clientY
    }
  })

  canvas.on('mouse:up', opt => { // 鼠标松开时触发
    canvas.setViewportTransform(canvas.viewportTransform) // 设置此画布实例的视口转换  
    canvas.isDragging = false
  })

  // canvas.on('mouse:wheel', opt => {
  //   let delta = opt.e.deltaY // 滚轮，向上滚一下是 -100，向下滚一下是 100
  //   let zoom = canvas.getZoom() // 获取画布当前缩放值
  //   zoom *= 0.999 ** delta
  //   if (zoom > 5) zoom = 5
  //   if (zoom < 0.5) zoom = 0.5
  //   canvas.zoomToPoint({ // 关键点
  //     x: opt.e.offsetX,
  //     y: opt.e.offsetY
  //   },
  //     zoom
  //   )
  //   opt.e.preventDefault()
  //   opt.e.stopPropagation()
  // })
}

//添加鼠标事件
// const windowsLoadEvt = (canvas) => {
//   canvas.on('mouse:down', (e) => {
//     getMouse(e);
//   });

//   canvas.on('mouse:down', opt => { // 鼠标按下时触发 
//     let evt = opt.e 
//     // console.log((canvas.getObjects().indexOf(opt.target) == 0))
//     // if (canvas.getObjects().indexOf(opt.target) == 0) {
//     //     // 阻止拖拽
//     //     evt.preventDefault();
//     //     canvas.selection = false; }
//     if (evt.altKey === true) { // 是否按住alt 
//       // console.log((canvas.getObjects().indexOf(opt.target) != 0))
//       if (canvas.getObjects().indexOf(opt.target) !== 0) {
//         // 阻止拖拽
//         evt.preventDefault();
//         canvas.selection = false; 
//         canvas.isDragging = true // isDragging 是自定义的 
//         canvas.lastPosX = evt.clientX // lastPosX 是自定义的 
//         canvas.lastPosY = evt.clientY // lastPosY 是自定义的 
//       }
//     } 
//   });

//   canvas.on('mouse:move', opt => { // 鼠标移动时触发
//     if (canvas.isDragging) {
//       if (canvas.getObjects().indexOf(opt.target) !== 0){
//       let evt = opt.e
//       let vpt = canvas.viewportTransform // 聚焦视图的转换
//       vpt[4] += evt.clientX - canvas.lastPosX
//       vpt[5] += evt.clientY - canvas.lastPosY
//       canvas.requestRenderAll()
//       canvas.lastPosX = evt.clientX
//       canvas.lastPosY = evt.clientY
//     }
//     }
//   })

//   canvas.on('mouse:up', opt => { // 鼠标松开时触发
//     canvas.setViewportTransform(canvas.viewportTransform) // 设置此画布实例的视口转换  
//     canvas.isDragging = false
//   })

//   canvas.on('mouse:wheel', opt => {
//     let delta = opt.e.deltaY // 滚轮，向上滚一下是 -100，向下滚一下是 100
//     let zoom = canvas.getZoom() // 获取画布当前缩放值
//     zoom *= 0.999 ** delta
//     if (zoom > 5) zoom = 5
//     if (zoom < 0.5) zoom = 0.5
//     canvas.zoomToPoint({ // 关键点
//       x: opt.e.offsetX,
//       y: opt.e.offsetY
//     },
//       zoom
//     )
//     opt.e.preventDefault()
//     opt.e.stopPropagation()
//   })
// }

</script>
<style lang="less" scoped>
:deep(.el-header) {
  padding: 0 10px;
  background: #515a6e;
  height: 64px;
  line-height: 64px;
}

.el-main {
  --el-main-padding: 0px;
}

.home,
.el-container {
  height: 96vh;
}

.icon {
  display: block;
}

.canvas-box {
  overflow: hidden;
  width: 99%;
  // width: 68%;
  margin: 1%;
  // height: 98%;
  height: 57%;
  background-color: white;
}


.candidate-box0 {
  overflow: hidden;
  width: 99%;
  // width: 68%;
  margin: 1%;
  margin-top: -10px;
  // padding-right: -30px;
  // height: 98%;
  height: 6%;
  background-color: white;
}

.candidate-box {
  overflow: hidden;
  width: 99%;
  // width: 68%;
  margin: 1%;
  // height: 98%;
  height: 32%;
  background-color: white;
}

#canvas {
  margin: 0 auto;
}

.content {
  flex: 1;
  width: 200px;
  padding: 10px;
  padding-top: 0;
  height: 95%;
  overflow-y: auto;
}

// .refs {
//   border: 1.5px #565656 dashed;
//   border-radius: 7px;
//   // background-color: orange;
//   // color: orange;
// }
</style>
