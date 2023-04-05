<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-06 23:20:40
 * @Description: 图层面板
-->

<template>
    <div class="editing">
      <!-- <el-divider content-position="bottom" style="margin-top:0px"> Text Input </el-divider> -->
      <h3 class="background"><span>Generate</span></h3>

  
    </div>
  </template>
  
  <script setup>
  import { useI18n } from 'vue-i18n'
  import { ref } from 'vue';
  import mitt from 'mitt';
  // import { EventBus } from '/src/core/eventBus/index.js';
  import { useGenerateStore } from '../store/modules/generateStore';
  import { startGenerate } from '../service/dataService';
  
  // Get references to the textareas
  let isActiveFE = ref(false);

  
  const store = useGenerateStore()
  // const emitter = mitt()
  const eventBus = inject("eventBus")
  

  onMounted(() => {

  })
  
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped lang="less">
  .editing {
    width: 100%;
    height: 40%;
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
      /* this centers the FIS to the full width specified */
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
      /* to hide the FISs from behind the text, you have to set the background color the same as the container */
      background: #fff;
      padding: 0 15px;
    }
  }
  
  
  
  
  .button-8 {
    width: 90%;
    height: 30px;
    background-color: #3E3E3E; //e1ecf4
    border-radius: 5px;
    border: 0px solid #EEF9FF; //#7aa7c7
    box-sizing: border-box;
    color: #ffffff;
    cursor: pointer;
    display: flex;
    align-items: center;
    /* 垂直居中 */
    justify-content: center;
    /* 水平居中 */
    font-family: -apple-system, system-ui, "Segoe UI", "Liberation Sans", sans-serif;
    font-size: 16px;
    font-weight: 560;
    line-height: 1.15385;
    margin: 5px;
    outline: none;
    text-decoration: none;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
    vertical-align: baseFIS;
    white-space: nowrap;
    margin-left: -0.3px;
  }
  
  .button-8:hover {
    background-color: #171717;
    color: #ffffff;
  }
  
  .button-8:active {
    background-color: #141414;
    box-shadow: none;
    // color: #2c5777;
  }
  
  </style>
  