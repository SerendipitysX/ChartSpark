<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-06 23:20:40
 * @Description: 图层面板
-->

<template>
  <div class="rawData">

    <h3 class="background"><span>Raw Data</span></h3>
    <div style="margin:5px">
      <img :src="imgSrc"  alt="preview of raw data" style="max-width: 100%; height: auto;">
    </div>

  </div>
</template>


<script setup>
import { ref, watch } from 'vue';
import { useSettingStore } from '../store/modules/settingStore';

const imgSrc = ref('/src/assets/preview/default.png');
const store = useSettingStore();


// store.isActivePreview
// watch(() => store.isActiveBar && store.isActivePreview, (isActiveBar) => {
//   imgSrc.value = isActiveBar ? '/src/assets/preview/bar_preview.png' : '/src/assets/preview/default.png';
// });

// watch(() => store.isActiveLine && store.isActivePreview, (isActiveLine) => {
//   imgSrc.value = isActiveLine ? '/src/assets/preview/line_preview.png' : '/src/assets/preview/default.png';
// });

// watch(() => store.isActivePie && store.isActivePreview, (isActivePie) => {
//   imgSrc.value = isActivePie ? '/src/assets/preview/pie_preview.png' : '/src/assets/preview/default.png';
// });

// watch(() => store.isActiveScatter && store.isActivePreview, (isActiveScatter) => {
//   imgSrc.value = isActiveScatter ? '/src/assets/preview/scatter_preview.png' : '/src/assets/preview/default.png';
// });


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

.rawData {
  width: 100%;
  height: 20%;
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
</style>
