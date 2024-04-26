<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-06 23:20:40
 * @Description: 图层面板
-->

<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <div class="settings">
    <!-- <el-divider content-position="bottom" style="margin-top:0px; display: flex; padding-top: 3px; 
                                                        justify-content: center">Settings </el-divider> -->
    <h3 class="background"><span>SETTING</span></h3>
    <!-- icon -->
    <div style="margin-bottom: 8px; padding-left: 10px;">
      Chart type:
      &nbsp;
      <span>
        <button class="btn" :class="{ active: isActiveBar }" @click="toggleButtonBar">
          <svg t="1677853487870" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
            p-id="5337" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path
              d="M145.066667 371.285333v348.714667h131.498666V371.285333H145.066667z m-11.861334-59.733333H288.426667c26.453333 0 47.829333 21.418667 47.829333 47.829333v372.48c0 26.453333-21.418667 47.872-47.829333 47.872H133.12C106.794667 779.733333 85.333333 758.314667 85.333333 731.861333v-372.48c0-26.453333 21.418667-47.829333 47.872-47.829333zM446.250667 148.053333v571.733334h131.498666V148.053333H446.293333zM434.346667 88.32h155.306666c26.453333 0 47.829333 21.418667 47.829334 47.872v595.456c0 26.453333-21.418667 47.872-47.829334 47.872H434.346667c-26.453333 0-47.829333-21.418667-47.829334-47.872V136.192C386.517333 109.738667 407.893333 88.32 434.346667 88.32zM747.434667 720H878.933333v-231.68h-131.498666v231.68z m143.36-291.413333c26.453333 0 47.872 21.418667 47.872 47.872v255.402666c0 26.453333-21.418667 47.872-47.872 47.872H735.573333c-26.453333 0-47.829333-21.418667-47.829333-47.872V476.458667c0-26.453333 21.418667-47.872 47.829333-47.872h155.306667z"
              fill="#617282" p-id="5338" class="selected"></path>
            <path
              d="M85.333333 880.512m34.133334 0l785.066666 0q34.133333 0 34.133334 34.133333l0 0q0 34.133333-34.133334 34.133334l-785.066666 0q-34.133333 0-34.133334-34.133334l0 0q0-34.133333 34.133334-34.133333Z"
              fill="#617282" p-id="5339" class="selected"></path>
          </svg>
        </button>
        <button class="btn" :class="{ active: isActiveLine }" @click="toggleButtonLine">
          <svg t="1677854436397" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
            p-id="11529" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path
              d="M123.690667 128c19.754667 0 36.266667 14.506667 38.186666 33.578667l0.170667 3.584v545.024c0 59.52 48.256 108.544 109.653333 111.36l5.418667 0.128h613.632c20.48 0 37.333333 15.573333 38.314667 35.413333a37.546667 37.546667 0 0 1-34.602667 38.741333l-3.712 0.170667H277.12c-103.509333 0-188.330667-79.573333-191.701333-179.797333L85.333333 710.229333V165.12c0-9.856 4.053333-19.285333 11.221334-26.282667A38.954667 38.954667 0 0 1 123.733333 128z m786.005333 136.021333l0.981333 3.456 26.581334 121.173334c6.997333 31.872-12.757333 63.573333-45.141334 72.448l-4.096 1.024-125.013333 25.728a38.4 38.4 0 0 1-45.226667-26.837334 36.992 36.992 0 0 1 25.642667-44.928l3.584-0.938666 54.954667-11.306667-94.549334-56.192-204.16 167.936a39.338667 39.338667 0 0 1-44.288 3.669333l-3.114666-2.005333-79.573334-56.234667-115.328 103.04a39.253333 39.253333 0 0 1-51.370666 0.554667l-2.816-2.645333a36.266667 36.266667 0 0 1-0.554667-49.792l2.730667-2.730667 138.538666-123.733333a39.296 39.296 0 0 1 45.354667-4.778667l3.242667 2.090667 80.554666 56.917333 202.368-166.357333a39.338667 39.338667 0 0 1 41.557334-5.12l3.328 1.792 125.269333 74.453333-13.525333-61.781333a37.034667 37.034667 0 0 1 25.984-43.178667l3.584-0.853333a38.485333 38.485333 0 0 1 44.501333 25.130666z"
              fill="#424242" p-id="11530" class="selected"></path>
          </svg>
        </button>
        <button class="btn" :class="{ active: isActivePie }" @click="toggleButtonPie">
          <svg t="1677722625184" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
            p-id="8201" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path
              d="M503.338667 42.773333a8.533333 8.533333 0 0 1 8.469333 6.698667l0.192 1.856V418.133333a93.866667 93.866667 0 0 0 93.866667 93.866667h366.805333c4.714667 0 8.533333 3.84 8.533333 8.533333v0.149334c-0.106667 5.674667-0.213333 10.176-0.384 13.504C969.237333 783.104 763.776 981.333333 512 981.333333 252.8 981.333333 42.666667 771.2 42.666667 512 42.666667 260.373333 240.682667 54.997333 489.386667 43.2l12.096-0.384 1.856-0.042667zM441.6 119.253333l-6.144 1.130667C251.434667 156.117333 113.066667 318.250667 113.066667 512c0 220.330667 178.602667 398.933333 398.933333 398.933333 193.984 0 355.626667-138.453333 391.509333-321.92l1.216-6.613333H605.866667a164.266667 164.266667 0 0 1-164.181334-159.061333L441.6 418.133333V119.253333z m149.333333-69.76h0.725334l9.130666 1.621334c2.56 0.469333 4.821333 0.896 6.826667 1.301333l2.858667 0.597333c182.229333 38.912 325.269333 183.594667 361.792 366.698667l2.154666 11.925333a8.533333 8.533333 0 0 1-6.954666 9.834667l-1.450667 0.128H629.333333a46.933333 46.933333 0 0 1-46.805333-43.584l-0.128-3.370667V58.026667a8.533333 8.533333 0 0 1 8.533333-8.533334z m62.144 93.802667a4.266667 4.266667 0 0 0-0.298666 1.557333v222.058667c0 2.346667 1.92 4.266667 4.266666 4.266667h222.08a4.266667 4.266667 0 0 0 3.968-5.824A400.512 400.512 0 0 0 658.602667 140.885333a4.266667 4.266667 0 0 0-5.546667 2.410667z"
              fill="#515151" p-id="8202" data-spm-anchor-id="a313x.7781069.0.i8" class="selected"></path>
          </svg>
        </button>
        <button class="btn" :class="{ active: isActiveScatter }" @click="toggleButtonScatter">
          <svg t="1677724146373" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
            p-id="11292" data-spm-anchor-id="a313x.7781069.0.i13" xmlns:xlink="http://www.w3.org/1999/xlink">
            <path d="M896 128v832H64V128h832m64-64H0v960h960V64z" p-id="11293" data-spm-anchor-id="a313x.7781069.0.i15"
              class="selected" fill="#515151"></path>
            <path
              d="M288 384c19.2 0 32-12.8 32-32s-12.8-32-32-32-32 12.8-32 32 12.8 32 32 32z m0 64c-51.2 0-96-44.8-96-96s44.8-96 96-96 96 44.8 96 96-44.8 96-96 96zM480 576c19.2 0 32-12.8 32-32s-12.8-32-32-32-32 12.8-32 32 12.8 32 32 32z m0 64c-51.2 0-96-44.8-96-96s44.8-96 96-96 96 44.8 96 96-44.8 96-96 96zM736 512c19.2 0 32-12.8 32-32s-12.8-32-32-32-32 12.8-32 32 12.8 32 32 32z m0 64c-51.2 0-96-44.8-96-96s44.8-96 96-96 96 44.8 96 96-44.8 96-96 96zM352 832c19.2 0 32-12.8 32-32s-12.8-32-32-32-32 12.8-32 32 12.8 32 32 32z m0 64c-51.2 0-96-44.8-96-96s44.8-96 96-96 96 44.8 96 96-44.8 96-96 96zM768 704h-64v-64h-64v64h-64v64h64v64h64v-64h64zM256 512h-64v64h-64v64h64v64h64v-64h64v-64h-64zM576 384v-64h64v-64h-64v-64h-64v64h-64v64h64v64z"
              p-id="11294" data-spm-anchor-id="a313x.7781069.0.i14" class="selected"></path>
          </svg>
        </button>
      </span>
    </div>

    <div class="aspect-ratio" style="margin-bottom: 8px; padding-left: 10px;">
      <form>
        <label for="aspect-ratio">Aspect ratio:</label> &nbsp;
        <select id="aspect-ratio" name="aspect-ratio">
          <!-- [(1,1), (3,2),     (4, 3), (5, 4)] -->
          <option value="1:1">1:1</option>
          <option value="3:2">3:2</option>
          <option value="4:3">4:3</option>
          <option value="5:4">5:4</option>
        </select>
      </form>
    </div>

  <div class="bar-width" v-if="showBar" style="margin-bottom: 8px; padding-left: 5px;">
    <el-form :label-width="80">
      <label for="bar-width">Bar width:</label> &nbsp; &nbsp; &nbsp;
      <el-input-number style="width: 40%" :max="1" :min="0" :step="0.1" v-model="barWidth" size="small">
      </el-input-number>
    </el-form>
  </div>
  <!-- 
    <div class="range" v-if="showNotPie" style="margin-bottom: 8px; padding-left: 5px; display: flex;">
      <label for="range">Range:</label> &nbsp; &nbsp;
      <el-form :label-width="150">
          <label style="color: #6F6E7E; font-size: 13px;">Y_min</label>&nbsp;
          <el-input-number style="width: 50%" :max="100000" :min="0" :step="1" v-model="y_min" size="small">
          </el-input-number>
          <label style=" color: #6F6E7E; font-size: 13px;">Y_max</label>&nbsp;
          <el-input-number style=" width: 49%" :max="100000" :min="0" :step="1" v-model="y_max" size="small">
          </el-input-number>
        </el-form>
      </div> -->

    <div :class="{ active: isActivePreview }" @click="toggleButtonPreview" class="button-8-container"
      style="display: flex; justify-content: center;  align-items: center;">
      <button class="button-8" role="button">Preview</button>
    </div>
  </div>

  <div class="rawData">

    <h3 class="background"><span>Raw Data</span></h3>
    <div style="margin:-2px">
      <img :src="imgSrc" alt="preview of raw data" style="max-width: 75%; height: auto;
        display: flex; justify-content: center; margin-left: 35px; margin-top: -12px; align-items: center;">
    </div>

  </div>

  <div class="theme">
    <h3 class="background"><span>Theme</span></h3>
    <div style="margin-top:-12px">
      <img :src='imgSrcTheme' alt="theme of data"
        style="max-width: 90%; height: auto; border-radius: 7px;margin-left: 10px;margin-top: 10px;">
    </div>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue';
import { useI18n } from 'vue-i18n'
import { IconButton } from "@chakra-ui/react"
import { SearchIcon } from "@chakra-ui/icons"
import { Delete, Edit, Search, Share, Upload } from '@element-plus/icons-vue'
import { cond } from 'lodash';
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios';
import { useSettingStore, useJsonStore } from '../store/modules/settingStore'
import { sendChart } from '../service/dataService';
const router = useRouter()
const route = useRoute()


let showBar = ref(false)
let showNotPie = ref(false)
let isActiveBar = ref(false);
let isActiveLine = ref(false);
let isActivePie = ref(false);
let isActiveScatter = ref(false);
let isActivePreview = ref(false)
let barWidth = ref(0.8)
let y_min = ref()
let y_max = ref()
const imgSrc = ref('/src/assets/preview/default.png');
const imgSrcTheme = ref('/src/assets/wordcloud/default.png');

const store = useSettingStore()
const storeJson = useJsonStore()

const canvas = inject("canvas")

// const jsonObject = JSON.parse(storeJson.jsonData);
//     const valuesArray = Object.values(jsonObject.y);
//     const minValue = Math.min(...valuesArray);
//     const maxValue = Math.max(...valuesArray);
//     let y_min = ref(minValue)
//     let y_max = maxValue

// console.log(storeJson.jsonData)

// onMounted(() => {
//   setMinMax();
// })
// const setMinMax = () => {
// }

//设置点击chart icon
function toggleButtonBar() {
  isActiveBar.value = !isActiveBar.value;
  if (isActiveBar.value === true) {
    showBar.value = true;
    showNotPie.value = true
    isActiveLine.value = isActivePie.value = isActiveScatter.value = false;
    //传递参数 错了，这个是传递给新的界面。。。
    // router.push({ path: '/rawdata/' + isActiveBar })
    // 用pinia在平级vue中传递参数
    store.isActiveBar = isActiveBar.value
    store.isActiveLine = store.isActivePie = store.isActiveScatter = false;
    // 万一能用后端传呢
    // const jsonObject = JSON.parse(storeJson.jsonData);
    // const valuesArray = Object.values(jsonObject.y);
    // const minValue = Math.min(...valuesArray);
    // const maxValue = Math.max(...valuesArray);
    // let y_min = minValue
    // let y_max = maxValue
    // console.log("min:")
    // console.log(y_min)
  }
  else {
    store.isActiveBar = isActiveBar.value
  }
}
function toggleButtonLine() {
  isActiveLine.value = !isActiveLine.value;
  if (isActiveLine.value === true) {
    showBar.value = false;
    showNotPie.value = true
    isActiveBar.value = isActivePie.value = isActiveScatter.value = false;
    store.isActiveLine = isActiveLine.value
    store.isActiveBar = store.isActivePie = store.isActiveScatter = false;
  }
  else {
    store.isActiveLine = isActiveLine.value
  }
}
function toggleButtonPie() {
  isActivePie.value = !isActivePie.value;
  if (isActivePie.value === true) {
    showBar.value = false;
    showNotPie.value = false
    isActiveLine.value = isActiveBar.value = isActiveScatter.value = false;
    store.isActivePie = isActivePie.value
    store.isActiveLine = store.isActiveBar = store.isActiveScatter = false;
  }
  else {
    store.isActivePie = isActivePie.value
  }
}
function toggleButtonScatter() {
  isActiveScatter.value = !isActiveScatter.value;
  if (isActiveScatter.value === true) {
    showBar.value = false;
    showNotPie.value = true
    isActiveLine.value = isActivePie.value = isActiveBar.value = false;
    store.isActiveScatter = isActiveScatter.value
    store.isActiveLine = store.isActivePie = store.isActiveBar = false;
  }
  else {
    store.isActiveScatter = isActiveScatter.value
  }
}

//设置点击preview按钮
function toggleButtonPreview() {
  isActivePreview.value = !isActivePreview.value;
  store.isActivePreview = isActivePreview.value
  if (isActivePreview.value == true && isActiveBar.value == true) {
    // aspect-ratio
    const selectElement = document.getElementById("aspect-ratio");
    const selectedIndex = selectElement.selectedIndex;
    const selectedOption = selectElement.options[selectedIndex];
    const selectedValue = selectedOption.value;
    console.log(selectedValue);
    // bar-width
    console.log(barWidth.value)
    console.log(y_min.value)
    let param = { "chart-type": "bar", "aspect-ratio": selectedValue, "y_min": y_min.value, "y_max": y_max.value, "bar_width": barWidth.value, "data": storeJson.jsonData }
    sendChart(param, function (data) {
      // 显示图表
      store.mask_path_foreground = data[2]
      store.mask_path_background = data[3]
      imgSrc.value = '/src/assets/preview/bar_preview.png'
      imgSrcTheme.value = '/src/assets/wordcloud/wc.png'
      fabric.loadSVGFromURL('/src/assets/preview/plot.svg', function (objects, options) {
        var svgObject = fabric.util.groupSVGElements(objects, options);
        svgObject.id = "data preview";
        canvas.c.add(svgObject);
      });
    });
  }
  if (isActivePreview.value == true && isActiveLine.value == true) {
    // aspect-ratio
    const selectElement = document.getElementById("aspect-ratio");
    const selectedIndex = selectElement.selectedIndex;
    const selectedOption = selectElement.options[selectedIndex];
    const selectedValue = selectedOption.value;
    console.log(selectedValue);
    let param = { "chart-type": "line", "aspect-ratio": selectedValue, "bar_width": [], "data": storeJson.jsonData }
    sendChart(param, function (data) {
      console.log(data)
      // 显示图表
      store.mask_path_foreground = data[2]
      store.mask_path_background = data[3]
      imgSrc.value = '/src/assets/preview/line_preview.png'
      imgSrcTheme.value = '/src/assets/wordcloud/wc.png'

      fabric.loadSVGFromURL('/src/assets/preview/plot.svg', function (objects, options) {
        var svgObject = fabric.util.groupSVGElements(objects, options);
        svgObject.id = "data preview";
        canvas.c.add(svgObject);
      });

    });
  }
  if (isActivePreview.value == true && isActivePie.value == true) {
    // aspect-ratio
    const selectElement = document.getElementById("aspect-ratio");
    const selectedIndex = selectElement.selectedIndex;
    const selectedOption = selectElement.options[selectedIndex];
    const selectedValue = selectedOption.value;
    console.log(selectedValue);
    let param = { "chart-type": "pie", "aspect-ratio": selectedValue, "bar_width": [], "data": storeJson.jsonData }
    sendChart(param, function (data) {
      store.mask_path_foreground = data[2]
      store.mask_path_background = data[3]
      // 显示图表
      imgSrc.value = '/src/assets/preview/pie_preview.png'
      imgSrcTheme.value = '/src/assets/wordcloud/wc.png'
      fabric.loadSVGFromURL('/src/assets/preview/plot.svg', function (objects, options) {
        var svgObject = fabric.util.groupSVGElements(objects, options);
        svgObject.id = "data preview";
        canvas.c.add(svgObject);
      });
    });
  }
  if (isActivePreview.value == true && isActiveScatter.value == true) {
    // aspect-ratio
    const selectElement = document.getElementById("aspect-ratio");
    const selectedIndex = selectElement.selectedIndex;
    const selectedOption = selectElement.options[selectedIndex];
    const selectedValue = selectedOption.value;
    let param = { "chart-type": "scatter", "aspect-ratio": selectedValue, "bar_width": [], "data": storeJson.jsonData }
    sendChart(param, function (data) {
      // 显示图表
      store.mask_path_foreground = data[2]
      store.mask_path_background = data[3]
      imgSrc.value = '/src/assets/preview/scatter_preview.png'
      imgSrcTheme.value = '/src/assets/wordcloud/wc.png'
      fabric.loadSVGFromURL('/src/assets/preview/plot.svg', function (objects, options) {
        var svgObject = fabric.util.groupSVGElements(objects, options);
        svgObject.id = "data preview";
        canvas.c.add(svgObject);
      });
    });
  }
}

//响应button
// const buttonOption = [['Bar width', ''], ['Aspect ratio']]

// function clickIcon(cnt) {
//   buttonSelect.value = cnt;
//   if (buttonSelect.value === 0) {
//     showBar.value = true;
//     showNotPie.value = true
//   }
//   if (buttonSelect.value === 1) {
//     showBar.value = false;
//     showNotPie.value = true
//   }
//   if (buttonSelect.value === 2) {
//     showBar.value = false;
//     showNotPie.value = false
//   }
//   if (buttonSelect.value === 3) {
//     showBar.value = false;
//     showNotPie.value = true
//   }
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

.settings {
  width: 100%;
  height: 16%;
  margin-top: -33px;
  background: #fff;
  position: relative;
  z-index: 1;
}

.rawData {
  width: 100%;
  height: 23%;
  margin-top: -20px;
  background: #fff;
}


.theme {
  width: 100%;
  height: 16.5%;
  margin-top: -20px;
  background: #fff;
}

h3 {
  margin-top: 30px;
  text-align: center;
  text-transform: uppercase;
  background: #fff;

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

.btn {
  background-color: #eaeaea;
  border: none;
  border-radius: 5px;
  color: white;
  padding: 4px 4px;
  font-size: 18px;
  cursor: pointer;
  margin-right: 8px;
}

/* Darker background on mouse-over */
.btn.active {
  background-color: #EEF9FF;
  border: 15px;
  border-color: #a1a1a1;
}

.btn svg {
  // color: #465EEA;
  color: #a1a1a1;
}

// .btn:focus svg {
//   // color: #465EEA;
//   color: #465EEA;
// }
.btn.active>.icon path {
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


input[type="text"],
select {
  // display: block;
  width: 40%;
  color: #6F6E7E;
  height: 24px;
  padding: 3px;
  padding-left: 12%;
  font-size: 13px;
  border-radius: 5px;
  border: 1.5px solid #E1E4EB;
  margin-bottom: 0px;
  box-sizing: border-box;
}

.button-8 {
  width: 80%;
  height: 23px;
  background-color: #d6eaf4; //e1ecf4
  border-radius: 3px;
  border: 0px solid #EEF9FF; //#7aa7c7
  // box-shadow: rgba(255, 255, 255, .7) 0 1px 0 0 inset;
  box-sizing: border-box;
  color: #39739d;
  cursor: pointer;
  display: flex;
  align-items: center;
  /* 垂直居中 */
  justify-content: center;
  /* 水平居中 */
  font-family: -apple-system, system-ui, "Segoe UI", "Liberation Sans", sans-serif;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.15385;
  margin: 0;
  outline: none;
  // padding: 8px 8px;
  // position: relative;
  // text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: baseline;
  white-space: nowrap;
}

.button-8:hover {
  background-color: #b3d3ea;
  color: #2c5777;
}

.button-8:active {
  background-color: #a0c7e4;
  box-shadow: none;
  // color: #2c5777;
}


button {
  background-color: #ccc;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button.active {
  background-color: green;
  color: white;
}
</style>
