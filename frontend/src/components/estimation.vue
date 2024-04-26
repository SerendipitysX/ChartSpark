<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-06 23:20:40
 * @Description: 图层面板
-->

<template>
  <div class="estimationBox">
    <!-- <el-divider content-position="bottom" style="margin-top:10px"> Estimation </el-divider> -->
    <h3 class="background"><span>EVALUATION</span></h3>
    <!-- <el-progress :percentage="100" :format="format"></el-progress> -->

    <div class="content" style="display: flex; flex-direction: row; position: relative;">
      <!-- <div class="eval_info"> -->
        <div class="img_container" style="position: relative;">
          <img id="myImage" :src=imgSrc>
        </div>
        <button class="value" v-if="show" style="position: absolute; top: 0; right: 100;">{{ value_estimation }}</button>
      <!-- </div> -->

      <div class="fourtypes" style="display: flex; flex-direction: column;">

        <button class="btn_e" @click="clickButtonBar">
          <svg t="1677853487870" class="icon" style="width: 30px; height: 30px;" viewBox="0 0 1024 1024" version="1.1"
            xmlns="http://www.w3.org/2000/svg" p-id="5337" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path
              d="M145.066667 371.285333v348.714667h131.498666V371.285333H145.066667z m-11.861334-59.733333H288.426667c26.453333 0 47.829333 21.418667 47.829333 47.829333v372.48c0 26.453333-21.418667 47.872-47.829333 47.872H133.12C106.794667 779.733333 85.333333 758.314667 85.333333 731.861333v-372.48c0-26.453333 21.418667-47.829333 47.872-47.829333zM446.250667 148.053333v571.733334h131.498666V148.053333H446.293333zM434.346667 88.32h155.306666c26.453333 0 47.829333 21.418667 47.829334 47.872v595.456c0 26.453333-21.418667 47.872-47.829334 47.872H434.346667c-26.453333 0-47.829333-21.418667-47.829334-47.872V136.192C386.517333 109.738667 407.893333 88.32 434.346667 88.32zM747.434667 720H878.933333v-231.68h-131.498666v231.68z m143.36-291.413333c26.453333 0 47.872 21.418667 47.872 47.872v255.402666c0 26.453333-21.418667 47.872-47.872 47.872H735.573333c-26.453333 0-47.829333-21.418667-47.829333-47.872V476.458667c0-26.453333 21.418667-47.872 47.829333-47.872h155.306667z"
              fill="#617282" p-id="5338" class="selected"></path>
            <path
              d="M85.333333 880.512m34.133334 0l785.066666 0q34.133333 0 34.133334 34.133333l0 0q0 34.133333-34.133334 34.133334l-785.066666 0q-34.133333 0-34.133334-34.133334l0 0q0-34.133333 34.133334-34.133333Z"
              fill="#617282" p-id="5339" class="selected"></path>
          </svg>
        </button>

        <button class="btn_e" @click="clickButtonLine">
          <svg t="1677854436397" class="icon" style="width: 30px; height: 30px;" viewBox="0 0 1024 1024" version="1.1"
            xmlns="http://www.w3.org/2000/svg" p-id="11529" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path
              d="M123.690667 128c19.754667 0 36.266667 14.506667 38.186666 33.578667l0.170667 3.584v545.024c0 59.52 48.256 108.544 109.653333 111.36l5.418667 0.128h613.632c20.48 0 37.333333 15.573333 38.314667 35.413333a37.546667 37.546667 0 0 1-34.602667 38.741333l-3.712 0.170667H277.12c-103.509333 0-188.330667-79.573333-191.701333-179.797333L85.333333 710.229333V165.12c0-9.856 4.053333-19.285333 11.221334-26.282667A38.954667 38.954667 0 0 1 123.733333 128z m786.005333 136.021333l0.981333 3.456 26.581334 121.173334c6.997333 31.872-12.757333 63.573333-45.141334 72.448l-4.096 1.024-125.013333 25.728a38.4 38.4 0 0 1-45.226667-26.837334 36.992 36.992 0 0 1 25.642667-44.928l3.584-0.938666 54.954667-11.306667-94.549334-56.192-204.16 167.936a39.338667 39.338667 0 0 1-44.288 3.669333l-3.114666-2.005333-79.573334-56.234667-115.328 103.04a39.253333 39.253333 0 0 1-51.370666 0.554667l-2.816-2.645333a36.266667 36.266667 0 0 1-0.554667-49.792l2.730667-2.730667 138.538666-123.733333a39.296 39.296 0 0 1 45.354667-4.778667l3.242667 2.090667 80.554666 56.917333 202.368-166.357333a39.338667 39.338667 0 0 1 41.557334-5.12l3.328 1.792 125.269333 74.453333-13.525333-61.781333a37.034667 37.034667 0 0 1 25.984-43.178667l3.584-0.853333a38.485333 38.485333 0 0 1 44.501333 25.130666z"
              fill="#424242" p-id="11530" class="selected"></path>
          </svg>
        </button>

        <button class="btn_e" @click="clickButtonPie">
          <svg t="1677722625184" class="icon" style="width: 30px; height: 30px;" viewBox="0 0 1024 1024" version="1.1"
            xmlns="http://www.w3.org/2000/svg" p-id="8201" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path
              d="M503.338667 42.773333a8.533333 8.533333 0 0 1 8.469333 6.698667l0.192 1.856V418.133333a93.866667 93.866667 0 0 0 93.866667 93.866667h366.805333c4.714667 0 8.533333 3.84 8.533333 8.533333v0.149334c-0.106667 5.674667-0.213333 10.176-0.384 13.504C969.237333 783.104 763.776 981.333333 512 981.333333 252.8 981.333333 42.666667 771.2 42.666667 512 42.666667 260.373333 240.682667 54.997333 489.386667 43.2l12.096-0.384 1.856-0.042667zM441.6 119.253333l-6.144 1.130667C251.434667 156.117333 113.066667 318.250667 113.066667 512c0 220.330667 178.602667 398.933333 398.933333 398.933333 193.984 0 355.626667-138.453333 391.509333-321.92l1.216-6.613333H605.866667a164.266667 164.266667 0 0 1-164.181334-159.061333L441.6 418.133333V119.253333z m149.333333-69.76h0.725334l9.130666 1.621334c2.56 0.469333 4.821333 0.896 6.826667 1.301333l2.858667 0.597333c182.229333 38.912 325.269333 183.594667 361.792 366.698667l2.154666 11.925333a8.533333 8.533333 0 0 1-6.954666 9.834667l-1.450667 0.128H629.333333a46.933333 46.933333 0 0 1-46.805333-43.584l-0.128-3.370667V58.026667a8.533333 8.533333 0 0 1 8.533333-8.533334z m62.144 93.802667a4.266667 4.266667 0 0 0-0.298666 1.557333v222.058667c0 2.346667 1.92 4.266667 4.266666 4.266667h222.08a4.266667 4.266667 0 0 0 3.968-5.824A400.512 400.512 0 0 0 658.602667 140.885333a4.266667 4.266667 0 0 0-5.546667 2.410667z"
              fill="#515151" p-id="8202" data-spm-anchor-id="a313x.7781069.0.i8" class="selected"></path>
          </svg>
        </button>

        <button class="btn_e" :class="{ active: isEvaluateScatter }" @click="toggleButtonScatter">
          <svg t="1677724146373" class="icon" style="width: 30px; height: 30px;" viewBox="0 0 1024 1024" version="1.1"
            xmlns="http://www.w3.org/2000/svg" p-id="11292" data-spm-anchor-id="a313x.7781069.0.i13"
            xmlns:xlink="http://www.w3.org/1999/xlink">
            <path d="M896 128v832H64V128h832m64-64H0v960h960V64z" p-id="11293" data-spm-anchor-id="a313x.7781069.0.i15"
              class="selected" fill="#515151"></path>
            <path
              d="M288 384c19.2 0 32-12.8 32-32s-12.8-32-32-32-32 12.8-32 32 12.8 32 32 32z m0 64c-51.2 0-96-44.8-96-96s44.8-96 96-96 96 44.8 96 96-44.8 96-96 96zM480 576c19.2 0 32-12.8 32-32s-12.8-32-32-32-32 12.8-32 32 12.8 32 32 32z m0 64c-51.2 0-96-44.8-96-96s44.8-96 96-96 96 44.8 96 96-44.8 96-96 96zM736 512c19.2 0 32-12.8 32-32s-12.8-32-32-32-32 12.8-32 32 12.8 32 32 32z m0 64c-51.2 0-96-44.8-96-96s44.8-96 96-96 96 44.8 96 96-44.8 96-96 96zM352 832c19.2 0 32-12.8 32-32s-12.8-32-32-32-32 12.8-32 32 12.8 32 32 32z m0 64c-51.2 0-96-44.8-96-96s44.8-96 96-96 96 44.8 96 96-44.8 96-96 96zM768 704h-64v-64h-64v64h-64v64h64v64h64v-64h64zM256 512h-64v64h-64v64h64v64h64v-64h64v-64h-64zM576 384v-64h64v-64h-64v-64h-64v64h-64v64h64v64z"
              p-id="11294" data-spm-anchor-id="a313x.7781069.0.i14" class="selected"></path>
          </svg>
        </button>
      </div>
    </div>


  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useGenerateStore } from '../store/modules/generateStore';
import { startEvaluate } from '../service/dataService';
const { t } = useI18n()
let mSelectMode = inject('mSelectMode')
let mSelectId = inject('mSelectId')
let mSelectIds = inject('mSelectIds')
const canvas = inject("canvas")
let isEvaluateBar = ref(false);
let isEvaluateLine = ref(false);
let isEvaluatePie = ref(false);
let isEvaluateScatter = ref(false);
let imgSrc = ref('/src/assets/generation/estimation/default.png')
const value_estimation = ref(94.5);
let show = ref(false)
let count = ref(0)

const store = useGenerateStore()
const eventBus = inject("eventBus")

function clickButtonBar() {
  var activeObj = canvas.c.getActiveObject();
  localStorage.setItem('activeObj', JSON.stringify(activeObj));
  var dataURL = JSON.parse(localStorage.getItem('activeObj'));
  let param = { "type": "Bar", "mask_path": store.maskPath, "image_data": dataURL, "count": count.value };
  console.log(param)
  startEvaluate(param, function (data) {
    // data:json
    console.log("======estimation=======")
    console.log(data)
    show.value = true;
    value_estimation.value = data.score_eval;
    // imgSrc.value = '/src/assets/evaluation/evaluation.png';
    var imgElement = document.getElementById('myImage');
    imgElement.src = data.eval_img_path
    count.value = count.value + 1;
  });
}

function clickButtonLine() {
  var activeObj = canvas.c.getActiveObject();
  localStorage.setItem('activeObj', JSON.stringify(activeObj));
  var dataURL = JSON.parse(localStorage.getItem('activeObj'));
  let param = { "type": "Line", "mask_path": store.maskPath, "image_data": dataURL, "count": count.value };
  console.log(param)
  startEvaluate(param, function (data) {
    // data:json
    console.log("======estimation=======")
    console.log(data)
    show.value = true;
    value_estimation.value = data.score_eval;
    // imgSrc.value = '/src/assets/evaluation/evaluation.png';
    var imgElement = document.getElementById('myImage');
    imgElement.src = data.eval_img_path
    count.value = count.value + 1;
  });
}

function clickButtonPie() {
  var activeObj = canvas.c.getActiveObject();
  localStorage.setItem('activeObj', JSON.stringify(activeObj));
  var dataURL = JSON.parse(localStorage.getItem('activeObj'));
  let param = { "type": "Pie", "mask_path": store.maskPath, "image_data": dataURL, "count": count.value };
  console.log(param)
  startEvaluate(param, function (data) {
    // data:json
    console.log("======estimation=======")
    console.log(data)
    show.value = true;
    value_estimation.value = data.score_eval;
    // imgSrc.value = '/src/assets/evaluation/evaluation.png';
    var imgElement = document.getElementById('myImage');
    imgElement.src = data.eval_img_path
    count.value = count.value + 1;
  });
}

// function clickButtonLine() {
//   setTimeout(() => {
//     imgSrc.value = '/src/assets/estimation/estimation.png';
//     show.value = true;
//     console.log(123445)
//   }, 1000);
// }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
:deep(.ivu-tooltip-inner) {
  white-space: normal;
}

:deep(.ivu-tooltip) {
  display: block;
}

:deep(.ivu-tooltip-rel) {
  display: block;
}

.estimationBox {
  height: 224px;
  background-color: white;
  margin-top: -19px;
  width: 100%;
}

.layer-box {
  max-height: 170px;
  height: auto;
  overflow-y: auto;
  margin-bottom: 5px;

  .ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    cursor: pointer;
  }

  &>div {
    padding: 0px 5px;
    margin: 3px 0;
    background: #f7f7f7;
    color: #c8c8c8;
    border-radius: 3px;
    font-size: 12px;
    line-height: 28px;

    &.active {
      color: #2d8cf0;
      background: #f0faff;
      font-weight: bold;
    }
  }
}

svg {
  vertical-align: text-top;
}
</style>

<style lang="less">
span.active {
  svg.icon {
    fill: #2d8cf0;
  }
}


h3 {
  margin-top: 30px;
  text-align: center;
  text-transform: uppercase;
  background: c;

  font-family: "DM Sans", sans-serif;
  color: #2a2a2a;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
}

h3.background {
  position: relative;
  z-index: 1;

  &:before {
    border-top: 1.5px solid #2a2a2a;
    content: "";
    margin: 0 auto;
    /* this centers the line to the full width specified */
    position: absolute;
    /* positioning must be absolute here, and relative positioning must be applied to the parent */
    top: 50%;
    left: 0;
    right: 0;
    bottom: 0;
    width: 95%;
    z-index: -1;
  }

  span {
    /* to hide the lines from behind the text, you have to set the background color the same as the container */
    background: #fff;
    padding: 0 15px;
  }
}

.btn_e {
  background-color: #eaeaea;
  border: none;
  border-radius: 5px;
  color: white;
  padding: 4px 4px;
  font-size: 18px;
  cursor: pointer;
  margin-right: 8px;
  margin-bottom: 10px;
}

/* Darker background on mouse-over */
.btn_e.active {
  background-color: #EEF9FF;
  border: 15px;
  border-color: #a1a1a1;
}

.btn_e svg {
  // color: #465EEA;
  color: #a1a1a1;
}

// .btn:focus svg {
//   // color: #465EEA;
//   color: #465EEA;
// }
.btn_e.active>.icon path {
  fill: #304FFE;
}

.icon .selected {
  width: 10px;
  height: 10px;
  fill: #333;
}


.container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: stretch;
  height: 100%;
  flex-direction: row;
}

.eval_info {
  // width: 80%;
  // display: flex;
  align-items: center;
}

.img_container {
  width: 90%;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.img_container img {
  max-width: 85%;
  max-height: 85%;
}

// .progress_container {
//   display: flex;
//   justify-content: center;
//   align-items: center;
//   height: 100%;
// }

.value {
  margin-left: 190px;
  margin-top: 60px;
  background-color: rgba(255, 255, 255, 0.2);
  // background-color: rgba(218, 218, 218, 0.2);
  border: 3px solid #4f96f3;
  border-radius: 50%;
  color: rgb(58, 58, 58);
  padding: 4px 4px;
  font-size: 13px;
  cursor: pointer;
  margin-right: -20px;
  margin-bottom: 10px;
  height: 42px;
  width: 42px;
}
</style>
