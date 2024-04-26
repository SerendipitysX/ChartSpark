<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-06 23:20:40
 * @Description: 图层面板
-->

<template>
    <div class="toolGallery">
    <div class="container">
            <button class="btn_g" @click="refine">
                <svg t="1679892220746" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    p-id="3115" width="200" height="200">
                    <path
                        d="M805.89 70.41l-644.68 768.3c-5.84 6.96-4.91 17.55 2.04 23.39l111.57 93.62c6.96 5.84 17.31 4.71 23.15-2.25l644.68-768.3c5.84-6.96 5.15-17.35-1.8-23.19L829.28 68.36c-6.96-5.84-17.55-4.91-23.39 2.05z m94.61 105.56l-189.05 225.3-78.22-65.64 189.05-225.31 78.22 65.65zM325.65 166.53l26.32 85.33 85.33 26.32-85.33 26.31-26.32 85.34-26.31-85.34-85.33-26.31 85.33-26.32zM551.99 110.33l12.05 39.1 39.1 12.06-39.1 12.06-12.05 39.1-12.06-39.1-39.1-12.06 39.1-12.06zM114.8 95.67l12.06 39.1 39.1 12.06-39.1 12.05-12.06 39.1-12.05-39.1-39.1-12.05 39.1-12.06zM909.2 360.91l12.05 39.1 39.1 12.06-39.1 12.06-12.05 39.1-12.06-39.1-39.1-12.06 39.1-12.06z"
                        fill="#6C6D6E" p-id="3116">
                    </path>
                </svg>
            </button>

            <div class="divider">
                <svg t="1679893232009" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    fill="#6C6D6E" p-id="6435" width="300" height="300">
                    <path d="M486.4 102.4l51.2 0 0 819.2-51.2 0 0-819.2Z" p-id="6436">
                    </path>
                </svg>
            </div>
            &nbsp;

            <button class="btn_g" @click="del">
                <svg t="1679892792610" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    p-id="5035" width="200" height="200">
                    <path
                        d="M972.657609 209.348408C987.158609 209.36839 998.930114 197.571202 998.949999 182.99865 998.969882 168.426097 987.230618 156.59651 972.729617 156.576528L32.457975 155.280806C17.956974 155.260823 6.18547 167.058012 6.165585 181.630564 6.1457 196.203116 17.884965 208.032703 32.385966 208.052686L972.657609 209.348408Z"
                        fill="#6C6D6E" p-id="5036"></path>
                    <path
                        d="M180.466902 992.356169 180.466902 1019.014859 206.993296 1018.74074 833.361858 1012.267947 859.348284 1011.999407 859.348284 985.883377 859.348284 289.397297C859.348284 274.824732 847.59289 263.011332 833.091874 263.011332 818.590859 263.011332 806.835465 274.824732 806.835465 289.397297L806.835465 985.883377 832.82189 959.498805 206.453329 965.971599 232.979723 992.356169 232.979723 282.67005C232.979723 268.097483 221.224329 256.284085 206.723313 256.284085 192.222298 256.284085 180.466902 268.097483 180.466902 282.67005L180.466902 992.356169Z"
                        fill="#6C6D6E" p-id="5037"></path>
                    <path
                        d="M656.410257 847.079027C656.410257 861.651593 668.165651 873.464992 682.666667 873.464992 697.167682 873.464992 708.923076 861.651593 708.923076 847.079027L708.923076 372.131659C708.923076 357.559091 697.167682 345.745694 682.666667 345.745694 668.165651 345.745694 656.410257 357.559091 656.410257 372.131659L656.410257 847.079027Z"
                        fill="#6C6D6E" p-id="5038"></path>
                    <path
                        d="M341.333333 847.079027C341.333333 861.651593 353.08873 873.464992 367.589743 873.464992 382.090758 873.464992 393.846155 861.651593 393.846155 847.079027L393.846155 372.131659C393.846155 357.559091 382.090758 345.745694 367.589743 345.745694 353.08873 345.745694 341.333333 357.559091 341.333333 372.131659L341.333333 847.079027Z"
                        fill="#6C6D6E" p-id="5039"></path>
                    <path
                        d="M498.871795 847.079027C498.871795 861.651593 510.627189 873.464992 525.128205 873.464992 539.62922 873.464992 551.384614 861.651593 551.384614 847.079027L551.384614 372.131659C551.384614 357.559091 539.62922 345.745694 525.128205 345.745694 510.627189 345.745694 498.871795 357.559091 498.871795 372.131659L498.871795 847.079027Z"
                        fill="#6C6D6E" p-id="5040"></path>
                    <path
                        d="M392.147755 116.721777C392.147755 102.063669 403.758665 90.363507 418.40134 90.363507L622.925796 90.363507C637.408947 90.363507 649.179381 102.1619 649.179381 116.549585L649.179381 171.644875 701.692203 171.644875 701.692203 116.549585C701.692203 72.986607 666.38105 37.591577 622.925796 37.591577L418.40134 37.591577C374.724427 37.591577 339.634933 72.950804 339.634933 116.721777L339.634933 165.310801 392.147755 165.310801 392.147755 116.721777Z"
                        fill="#6C6D6E" p-id="5041">
                    </path>
                </svg>
            </button>

            <button class="btn_g" @click="clone">
                <svg t="1679892948059" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    p-id="5717" width="200" height="200">
                    <path
                        d="M832 176V64c0-35.3-28.7-64-64-64H64C28.7 0 0 28.7 0 64v704c0 35.3 28.7 64 64 64h112c8.8 0 16 7.2 16 16v112c0 35.3 28.7 64 64 64h704c35.3 0 64-28.7 64-64V256c0-35.3-28.7-64-64-64H848c-8.8 0-16-7.2-16-16zM176 768H80c-8.8 0-16-7.2-16-16V80c0-8.8 7.2-16 16-16h672c8.8 0 16 7.2 16 16v96c0 8.8-7.2 16-16 16H256c-35.3 0-64 28.7-64 64v496c0 8.8-7.2 16-16 16z m768 192H272c-8.8 0-16-7.2-16-16V272c0-8.8 7.2-16 16-16h672c8.8 0 16 7.2 16 16v672c0 8.8-7.2 16-16 16z"
                        p-id="5718" fill="#707070">
                    </path>
                </svg>
            </button>

            <button class="btn_g" @click="big">
                <svg t="1679893767247" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    p-id="7431" width="200" height="200">
                    <path
                        d="M640 456h-118.4V320a32 32 0 0 0-64 0v136H320a32 32 0 0 0 0 64h137.6V640a32 32 0 1 0 64 0v-120H640a32 32 0 1 0 0-64z"
                        p-id="7432" fill="#515151"></path>
                    <path
                        d="M919.264 905.984l-138.912-138.912C851.808 692.32 896 591.328 896 480c0-229.376-186.624-416-416-416S64 250.624 64 480s186.624 416 416 416c95.008 0 182.432-32.384 252.544-86.208l141.44 141.44a31.904 31.904 0 0 0 45.248 0 32 32 0 0 0 0.032-45.248zM128 480C128 285.92 285.92 128 480 128s352 157.92 352 352-157.92 352-352 352S128 674.08 128 480z"
                        p-id="7433" fill="#515151">
                    </path>
                </svg>
            </button>

            <button class="btn_g" @click="small">
                <svg t="1679895171507" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                    p-id="8494" width="200" height="200">
                    <path
                        d="M919.264 905.984l-138.912-138.912C851.808 692.32 896 591.328 896 480c0-229.376-186.624-416-416-416S64 250.624 64 480s186.624 416 416 416c95.008 0 182.432-32.384 252.544-86.208l141.44 141.44a31.904 31.904 0 0 0 45.248 0 32 32 0 0 0 0.032-45.248zM128 480C128 285.92 285.92 128 480 128s352 157.92 352 352-157.92 352-352 352S128 674.08 128 480z"
                        p-id="8495" fill="#515151"></path>
                    <path d="M625.792 448H336a32 32 0 0 0 0 64h289.792a32 32 0 1 0 0-64z" p-id="8496" fill="#515151">
                    </path>
                </svg>
            </button>

        </div>
    </div>
</template>
  
<script setup>
import { ref } from 'vue'; // import ref from vue 
import { px } from 'framer-motion';
import mitt from 'mitt';
import { method } from 'lodash';
import { useGenerateStore } from '../store/modules/generateStore';
import { v4 as uuid } from 'uuid';
import { Delete, ZoomIn } from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'
import { startGenerate } from '../service/dataService';
// import tools
import align from '@/components/align.vue'
import centerAlign from '@/components/centerAlign.vue'
import flip from '@/components/flip.vue'
// import clone from '@/components/clone.vue'
import group from '@/components/group.vue'
// import zoom from '@/components/zoom.vue'
import lock from '@/components/lock.vue'
import dele from '@/components/del.vue'
import tools from '@/components/tools.vue'
import attribute from '@/components/attribute.vue'
import attributeText from '@/components/attributeText.vue'
import attributeEffect from '@/components/attributeEffect.vue'
// import { EventBus } from '/src/core/eventBus/index.js';
// const imgSrc = ref('/src/assets/generation/default.jpg'); 
const imgSrc = ref('/src/assets/generation/1.png');
const object = ref("object")
const description = ref("description")
const generateLabel = ref("xx")
const eventBus = inject("eventBus")
import { startRefine } from '../service/dataService';
const isAddRow = ref(false);
let mSelectMode = inject('mSelectMode')
let mSelectOneType = inject('mSelectOneType')
const canvas = inject("canvas")
let zoom = ref(0)

// const unShow = computed(() => {
//   return (mSelectMode.value === 'one' && mSelectOneType.value === 'group')
// })
// const createShow = computed(() => {
//   return (mSelectMode.value === 'multiple')
// })
// const rSet = () => {
//   canvas.c.zoomToPoint(
//     new fabric.Point(canvas.c.getWidth() / 2, canvas.c.getHeight() / 2),
//     1,
//   )
//   zoom.value = `${Math.round(100)}%`
// }


function refine() {
    var activeObj = canvas.c.getActiveObject();
    localStorage.setItem('activeObj', JSON.stringify(activeObj));
    // console.log(activeObj)
    var dataURL = JSON.parse(localStorage.getItem('activeObj'));
    console.log("===")
    // console.log(dataURL);
    var dataURL = canvas.c.toDataURL({
                    format: 'png',
                    left: activeObj.left,
                    top: activeObj.top,
                    width: activeObj.width,
                    height: activeObj.height
                    });
    // const data = dataURL.replace(/^data:image\/\w+;base64,/, '');
    let param = {
          "num_to_generate": 4, "object": "", "description": "", data: dataURL
        };
    startRefine(param, function (data) {
        eventBus.emit("isRefine", {
            "object": "",
            "description": "",
            "generateMethod": "",
            "location": "",
            "guide": "REFINE",
            "addRow": true,
            "imgList": data
          })
        });


    // eventBus.emit("isRefine", {
    //     "object": "",
    //     "description": "",
    //     "generateMethod": "",
    //     "guide": "REFINE",
    //     "addRow": true,
    //     "imgList": ["/src/assets/generation/refine/11.png", "/src/assets/generation/refine/22.png", "/src/assets/generation/refine/33.png",
    //         "/src/assets/generation/refine/44.png"]
    // });
}


const big = () => {
    let zoomRatio = canvas.c.getZoom();
    zoomRatio += 0.05;
    canvas.c.zoomToPoint(
        new fabric.Point(canvas.c.getWidth() / 2, canvas.c.getHeight() / 2),
        zoomRatio,
    )
    zoom.value = `${Math.round(zoomRatio * 100)}%`
}
const small = () => {
    let zoomRatio = canvas.c.getZoom();
    zoomRatio -= 0.05;
    canvas.c.zoomToPoint(
        new fabric.Point(canvas.c.getWidth() / 2, canvas.c.getHeight() / 2),
        zoomRatio,
    )
    zoom.value = `${Math.round(zoomRatio * 100)}%`
}



const del = () => {
    const activeObject = canvas.c.getActiveObjects();
    activeObject && activeObject.map(item => canvas.c.remove(item))
    canvas.c.requestRenderAll()
    canvas.c.discardActiveObject()
}

const clone = () => {
    const activeObject = canvas.c.getActiveObject();
    activeObject.clone(cloned => {
        canvas.c.discardActiveObject()
        // 间距设置
        const grid = 10
        cloned.set({
            left: cloned.left + grid,
            top: cloned.top + grid,
            id: uuid()
        })
        canvas.c.add(cloned)
        canvas.c.setActiveObject(cloned);
        canvas.c.requestRenderAll();
    })
}



</script>


  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">
:deep(.ivu-tooltip-inner) {
    white-space: normal;
}

:deep(.ivu-tooltip) {
    display: block;
}

:deep(.ivu-tooltip-rel) {
    display: block;
}

.toolGallery {
    /* add a scrollbar to the y-axis */
    width: 30%;
    margin: 1%;
    height: 70%;
    background-color: rgb(255, 255, 255);
    // margin-bottom: 3px;
    border-radius: 5px;
    float: right;
    justify-content: center;
    border: 2px solid #d5d5d5;
    align-items: center;
    // box-shadow: 2px 2px 5px rgba(110, 110, 110, 0.3);
}

.container {
    display: flex;
    justify-content: space-evenly;
    justify-content: center;
    align-items: center;
    padding-top: 4px;
    padding-left: 6px;
}

.gray-background {
    //   background-color: rgba(245,245,245,1);
    box-shadow: inset 0 0 3px #7e7e7e;
    border: 2px solid #0c0c0c;
}

.btn_g {
    background-color: #eaeaea;
    border: none;
    border-radius: 5px;
    color: white;
    // padding: 4px 4px 4px 4px;
    font-size: 18px;
    cursor: pointer;
    margin-right: 8px;
    width: 30px;
    height: 30px;
}

/* Darker background on mouse-over */
.btn_g.active {
    background-color: #EEF9FF;
    border: 15px;
    border-color: #a1a1a1;
}

.btn_g svg {
    // color: #465EEA;
    color: #a1a1a1;
}

// .btn:focus svg {
//   // color: #465EEA;
//   color: #465EEA;
// }
.btn_g.active>.icon path {
    fill: #304FFE;
}


.icon .selected {
    width: 10px;
    height: 10px;
    fill: #333;
}

.icon {
    width: 20px;
    height: 20px
}

.divider {
    width: 10px;
    height: 20px;
    margin-left: -10px;
    margin-top: 5px;
}
</style>
  