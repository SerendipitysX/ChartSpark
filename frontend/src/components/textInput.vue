<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-06 23:20:40
 * @Description: 图层面板
-->

<template>
  <div class="textInput">
    <!-- <el-divider content-position="bottom" style="margin-top:0px"> Text Input </el-divider> -->
    <h3 class="background"><span>Generate</span></h3>

    <div class="object" style="display: inline-block; padding-left: 10px; margin-bottom: 5px;">
      <!-- style="display: flexs; justify-content: center; align-items: center;width: 100%; padding-left: 5px; margin-bottom: 5px;"> -->
      <form>
        <label for="object">Object</label> <br>
        <textarea placeholder="Input what you want to generate" rows="20" name="object" id="object" cols="40"
          class="object-input" autocomplete="off" role="textbox" aria-autocomplete="list" aria-haspopup="true"></textarea>
      </form>
    </div>

    <div class="description" style="padding-left: 10px; margin-bottom: 5px;">
      <form>
        <label for="description">Description</label><br>
        <textarea placeholder="Add some description for this object" rows="20" name="description" id="description"
          cols="40" class="description-input" autocomplete="off" role="textbox" aria-autocomplete="list"
          aria-haspopup="true"></textarea>
      </form>
    </div>

    <div style="display: flex; justify-content: center; align-items: center;">
      <div>
        <button class="btn_uncon" :class="{ active: isActiveUNCon }" @click="toggleButtonUNCon">
          <strong>UNC</strong>onditional
        </button>
      </div>
      <div>
        <button class="btn_con" :class="{ active: isActiveCon }" @click="toggleButtonCon">
          <strong>C</strong>onditional
        </button>
      </div>
    </div>

    <div style="margin-left: 0px; margin-bottom: 5px; display: flex;  ">
      <button class="embed-fore-ex-rect" :class="{ active: isActiveF }" @click="toggleButtonF">
        <strong>F</strong>oreground&nbsp;
        <!-- <strong>E</strong>xternal -->
      </button>
    </div>

    <div style="margin-left: 0px; margin-bottom: 5px; display: flex; ">
      <button class="embed-bg-rect" :class="{ active: isActiveB }" @click="toggleButtonBG">
      <strong>B</strong>ackground
      <!-- <strong>g</strong>round -->
    </button>
  </div>

  <div style="margin-left: 0px; margin-bottom: 5px; display: flex; ">
    <div class="mask-container">
        <!-- <input type="checkbox" class="button-mask" id="mask1">
              <label for="mask1"><img src="src\assets\mask\pie\foreground\mask_0.png"></label>

              <input type="checkbox" class="button-mask" id="mask2">
              <label for="mask2"><img src="src\assets\mask\pie\foreground\mask_1.png"></label>

              <input type="checkbox" class="button-mask" id="mask3">
              <label for="mask3"><img src="src\assets\mask\pie\foreground\mask_2.png"></label> -->
      </div>
    </div>


    <div @click="clickButtonGenerate" class="generateButton"
      style="display: flex; justify-content: center;  align-items: center;">
      <button class="button-8" role="button">Generate ✨</button>
    </div>


  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { ref } from 'vue';
import mitt from 'mitt';
// import { EventBus } from '/src/core/eventBus/index.js';
import { useGenerateStore } from '../store/modules/generateStore'; 
import { useSettingStore } from '../store/modules/settingStore';
import { startGenerate } from '../service/dataService';
import { px } from 'framer-motion';
// import { fs } from 'fs'
// import { path } from 'path'
// const fs = require('fs');
// const path = require('path');

// Get references to the textareas
let isActiveF = ref(false);
let isActiveB = ref(false);
let isActiveCon = ref(false);
let isActiveUNCon = ref(false);
let isActiveGenerate = ref(false)
let has_show_mask_foreground = ref(false)
let has_show_mask_background = ref(false)

const store = useGenerateStore()
const storeSetting = useSettingStore()
const eventBus = inject("eventBus")


function toggleButtonF() {
  isActiveF.value = !isActiveF.value;
  if (isActiveF.value === true) {
    isActiveB.value = false;
  }
  checkBothButtonsClicked()
}

function toggleButtonBG() {
  isActiveB.value = !isActiveB.value;
  if (isActiveB.value === true) {
    isActiveF.value = false;
  }
}

function toggleButtonCon() {
  isActiveCon.value = !isActiveCon.value;
  if (isActiveCon.value === true) {
    isActiveUNCon.value = false;
  }
  checkBothButtonsClicked()
}

function toggleButtonUNCon() {
  isActiveUNCon.value = !isActiveUNCon.value;
  if (isActiveUNCon.value === true) {
    isActiveCon.value = false;
  }
}

const generationStateList = []

function clickButtonGenerate() {
  let objectTextarea = document.getElementById("object").value;
  let descriptionTextarea = document.getElementById("description").value;
  const chart_type = [storeSetting.isActiveBar, storeSetting.isActiveLine, storeSetting.isActivePie, storeSetting.isActiveScatter]
  // get mask
  const checkboxes = document.querySelectorAll('.button-mask');
  for (let i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      const imgSrc = checkboxes[i].nextElementSibling.firstElementChild.getAttribute('src'); // get image source
      store.maskPath = imgSrc;
      // console.log("mask是!!")
      console.log(store.maskPath)
    }
  }

  // const container = document.querySelector(".mask-container");
  // console.log(container)
  // Foreground
  if (isActiveF.value === true) {
    // Foreground + Con
    if (isActiveCon.value === true) {
      console.log("F+C")
      let str3 = objectTextarea + descriptionTextarea + "F" + "C";
      // New text
      if (!generationStateList.includes(str3)) {
        generationStateList.push(str3);
        let param = {
          "num_to_generate": 4, "method_to_generate": "F", "location": "C", "mask": store.maskPath,
          "object": objectTextarea, "description": descriptionTextarea, "chart_type": chart_type
        };
        startGenerate(param, function (data) {
          eventBus.emit("isGenerate", {
            "object": objectTextarea,
            "description": descriptionTextarea,
            "generateMethod": "F",
            "location": "C",
            "addRow": true,
            "imgList": data
          })
        });
      }
      // Old text
      else {
        let param = {
          "num_to_generate": store.generateNum, "method_to_generate": "F", "location": "C", "mask": store.maskPath,
          "object": objectTextarea, "description": descriptionTextarea, "chart_type": chart_type
        };
        startGenerate(param, function (data) {
          eventBus.emit("isGenerate", {
            "object": objectTextarea,
            "description": descriptionTextarea,
            "generateMethod": "F",
            "location": "C",
            "addRow": false,
            "imgList": data
          })
        });
      }
    }
    // Foreground + UNCon
    if (isActiveUNCon.value === true) {
      console.log("F+UNC")
      let str3 = objectTextarea + descriptionTextarea + "F" + "UNC";
      if (!generationStateList.includes(str3)) {
        generationStateList.push(str3);
        let param = {
          "num_to_generate": 4, "method_to_generate": "F", "location": "UNC", 
          "object": objectTextarea, "description": descriptionTextarea, "chart_type": chart_type
        };
        startGenerate(param, function (data) {
          eventBus.emit("isGenerate", {
            "object": objectTextarea,
            "description": descriptionTextarea,
            "generateMethod": "F",
            "location": "UNC",
            "addRow": true,
            "imgList": data
          })
        });
      }
      else {
        let param = {
          "num_to_generate": store.generateNum, "method_to_generate": "F", "location": "UNC", 
          "object": objectTextarea, "description": descriptionTextarea, "chart_type": chart_type
        };
        startGenerate(param, function (data) {
          eventBus.emit("isGenerate", {
            "object": objectTextarea,
            "description": descriptionTextarea,
            "generateMethod": "F",
            "location": "UNC",
            "addRow": false,
            "imgList": data
          })
        });
      }
    }
  };

  // Background
  if (isActiveB.value === true) {
    if (isActiveCon.value === true) {
      let str3 = objectTextarea + descriptionTextarea + "B" + "C";
      if (!generationStateList.includes(str3)) {
        generationStateList.push(str3);
        console.log("-----------------------------B+c")
        let param = {
          "num_to_generate": 4, "method_to_generate": "B", "location": "C", "mask": store.maskPath,
          "object": objectTextarea, "description": descriptionTextarea, "chart_type": chart_type
        };
        console.log(param);
        startGenerate(param, function (data) {
          eventBus.emit("isGenerate", {
            "object": objectTextarea,
            "description": descriptionTextarea,
            "generateMethod": "B",
            "location": "C",
            "addRow": true,
            "imgList": data
          })
        });
        // startGenerate(param, function (data) {
        //   eventBus.emit("isGenerate", {
        //     "object": objectTextarea,
        //     "description": descriptionTextarea,
        //     "generateMethod": "F",
        //     "location": "C",
        //     "addRow": true,
        //     "imgList": data
        //   })
        // });
      }
      else {
        let param = {
          "num_to_generate": store.generateNum, "method_to_generate": "B", "location": "C", "mask": store.maskPath,
          "object": objectTextarea, "description": descriptionTextarea, "chart_type": chart_type
        };
        console.log(param);
        startGenerate(param, function (data) {
          eventBus.emit("isGenerate", {
            "object": objectTextarea,
            "description": descriptionTextarea,
            "generateMethod": "B",
            "location": "C",
            "addRow": false,
            "imgList": data
          })
        });
      }
    }
    if (isActiveUNCon.value === true) {
      let str3 = objectTextarea + descriptionTextarea + "B" + "UNC";
      if (!generationStateList.includes(str3)) {
        generationStateList.push(str3);
        let param = {
          "num_to_generate": 4, "method_to_generate": "B", "location": "UNC", 
          "object": objectTextarea, "description": descriptionTextarea, "chart_type": chart_type
        };
        console.log(param);
        startGenerate(param, function (data) {
          eventBus.emit("isGenerate", {
            "object": objectTextarea,
            "description": descriptionTextarea,
            "generateMethod": "B",
            "location": "UNC",
            "addRow": true,
            "imgList": data
          })
        });
      }
      else {
        let param = {
          "num_to_generate": store.generateNum, "method_to_generate": "B", "location": "UNC", 
          "object": objectTextarea, "description": descriptionTextarea, "chart_type": chart_type
        };
        console.log(param);
        startGenerate(param, function (data) {
          eventBus.emit("isGenerate", {
            "object": objectTextarea,
            "description": descriptionTextarea,
            "generateMethod": "B",
            "location": "UNC",
            "addRow": false,
            "imgList": data
          })
        });
      }
    }

  };


  // 全部都要变成false
  isActiveF.value = isActiveB.value = false;
  isActiveCon.value = isActiveUNCon.value = false;
}

function checkBothButtonsClicked() {
  if (isActiveCon.value && isActiveF.value) {
    readDataFromFolder()
  }
  if (isActiveCon.value && isActiveB.value) {
    readDataFromFolder()
  }
}

function readDataFromFolder() {
  const container = document.querySelector(".mask-container");
  if (isActiveCon.value === true && isActiveF.value === true && has_show_mask_foreground.value === false) {
    container.innerHTML = ""; // clear previous mask
    storeSetting.mask_path_foreground.forEach((image, index) => {
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.classList.add("button-mask");
      checkbox.id = `mask${index + 1}`;

      const label = document.createElement("label");
      label.htmlFor = `mask${index + 1}`;

      const img = document.createElement("img");
      img.src = image;

      label.appendChild(img);
      container.appendChild(checkbox);
      container.appendChild(label);
    });
    // Add CSS styles for the checkboxes and labels
    const style = document.createElement("style");
    style.innerHTML = `
      input[type="checkbox"] { 
        -webkit-appearance: none; 
        -moz-appearance: none; 
        appearance: none; 
        display: none; 
        visibility: hidden; 
        cursor: pointer; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
      } 

      .button-mask+label img { 
        width: 26px; 
        height: 26px; 
        border-radius: 10%; 
        margin: 2px 2px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
      } 

      .button-mask:checked+label { 
        border: 2px solid #304FFE; 
        border-radius: 10%; 
      }`;
    document.head.appendChild(style);
    has_show_mask_foreground.value = true
    has_show_mask_background.value = false
  }
  console.log(isActiveCon.value, isActiveB.value, has_show_mask_background.value)
  if (isActiveCon.value === true && isActiveB.value === true && has_show_mask_background.value === false) {
    container.innerHTML = ""; // clear previous mask
    storeSetting.mask_path_background.forEach((image, index) => {
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.classList.add("button-mask");
      checkbox.id = `mask${index + 1}`;

      const label = document.createElement("label");
      label.htmlFor = `mask${index + 1}`;

      const img = document.createElement("img");
      img.src = image;

      label.appendChild(img);
      container.appendChild(checkbox);
      container.appendChild(label);
    });
    // Add CSS styles for the checkboxes and labels
    const style = document.createElement("style");
    style.innerHTML = `
      input[type="checkbox"] { 
        -webkit-appearance: none; 
        -moz-appearance: none; 
        appearance: none; 
        display: none; 
        visibility: hidden; 
        cursor: pointer; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
      } 

      .button-mask+label img { 
        width: 26px; 
        height: 26px; 
        border-radius: 10%; 
        margin: 2px 2px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
      } 

      .button-mask:checked+label { 
        border: 2px solid #304FFE; 
        border-radius: 10%; 
      }`;
    document.head.appendChild(style);
    has_show_mask_background.value = true
    has_show_mask_foreground.value = false
  }
}

onMounted(() => {
  // backTracking
  eventBus.on("backTracking", (data) => {
    console.log('-----')
    console.log(store.objectText, store.descriptionText, store.generateMethod, store.location)
    const objectInput = document.querySelector('.object-input');
    objectInput.value = store.objectText;
    const descriptionInput = document.querySelector('.description-input');
    descriptionInput.value = store.descriptionText;
    const buttonFE = document.querySelector(".embed-fore-ex-rect");
    if (store.generateMethod === "F") {
      // console.log("没写出来, 需要label亮起来")
      isActiveF.value = true;
      buttonFE.click();
    }
    const buttonBG = document.querySelector(".embed-bg-rect");
    if (store.generateMethod === "B") {
      // console.log("没写出来, 需要label亮起来")
      isActiveB.value = true;
      buttonBG.click();
    }
    const buttonCon = document.querySelector(".btn_con");
    if (store.location === "UNC") {
      // console.log("没写出来, 需要label亮起来")
      isActiveUNCon.value = true;
      buttonCon.click();
    }
    const buttonUNCon = document.querySelector(".btn_uncon");
    if (store.location === "C") {
      // console.log("没写出来, 需要label亮起来")
      isActiveCon.value = true;
      buttonUNCon.click();
    }
  });
})

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.textInput {
  width: 100%;
  height: 38.5%;
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


textarea {
  margin-top: 10px;
  margin-left: 2px;
  width: 89%;
  height: 40px;
  -moz-border-bottom-colors: none;
  -moz-border-left-colors: none;
  -moz-border-right-colors: none;
  -moz-border-top-colors: none;
  background: none repeat scroll 0 0 #F5F5F5;
  border-color: -moz-use-text-color #FFFFFF #FFFFFF -moz-use-text-color;
  border-image: none;
  border-radius: 6px 6px 6px 6px;
  // border-style: none solid solid none;
  border-style: none;
  // border-width: medium 1px 1px medium;
  // box-shadow: 0 1px 2px rgba(99, 99, 99, 0.12) inset;
  color: #4f4f4f;
  font-family: "DM Sans", sans-serif;
  font-size: 13px;
  line-height: 1.4em;
  padding: 5px 8px;
  transition: background-color 0.2s ease 0s;
}


textarea:focus {
  background: none repeat scroll 0 0 #f9f9f9;
  outline-width: 0;
}

.button-8 {
  width: 88%;
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
  margin-top: 0px;
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

// Foreground External
.embed-fore-ex-rect {
  // margin-left: -2px;
  background-color: #ffffff;
  width: 89%;
  height: 23px;
  border: 1.5px solid #5B97BD;
  border-radius: 10px;
  align-items: center;
  font-size: 14px;
  font-weight: 540;
  // padding-left: 27px;
  color: #2F75A1;
  margin-left: 15px;
}

.embed-fore-ex-rect.active {
  background-color: #CDE7F8;
  border: 0px solid #5B97BD;
}

// Background
.embed-bg-rect {
  width: 89%;
  height: 23px;
  border: 1.5px solid #C84444;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 540;
  color: #C84444;
  margin-left: 15px;
  background-color: #ffffff;
}


.embed-bg-rect.active {
  background-color: #F5CAC2;
  // border: 1.5px solid #F5CAC2;
  border: 0px solid #C84444;
}

// conditional
.btn_con {
  background-color: #ffffff;
  border: none;
  border-radius: 10px;
  color: rgb(17, 17, 17);
  padding: 4px 4px;
  padding-left: 18px;
  padding-right: 20px;
  font-size: 14px;
  border: 1.5px solid #a2a2a2;
  cursor: pointer;
  // margin-right: px;
  font-weight: 540;
  margin-top: 1px;
  margin-bottom: 5px;
  height: 23px;
}

/* Darker background on mouse-over */
.btn_con.active {
  background-color: #c8c8c8;
  border: 15px;
  border-color: #a1a1a1;
  // border: 1.5px solid #a2a2a2;
}

.btn_uncon {
  background-color: #ffffff;
  border: none;
  border-radius: 10px;
  color: rgb(17, 17, 17);
  padding: 4px 4px;
  padding-left: 18px;
  padding-right: 20px;
  font-size: 14px;
  border: 1.5px solid #a2a2a2;
  cursor: pointer;
  // margin-right: px;
  font-weight: 540;
  margin-top: 1px;
  margin-bottom: 5px;
  height: 23px;
  margin-right: 10px;
  // margin-left: 5px;
}

/* Darker background on mouse-over */
.btn_uncon.active {
  background-color: #c8c8c8;
  border: 15px;
  border-color: #a1a1a1;
  // border: 1.5px solid #a2a2a2;
}

// mask
.mask-container {
  width: 90%;
  // height: 30px;
  background-color: #ffffff; //e1ecf4
  border-radius: 5px;
  border: 0px solid #EEF9FF; //#7aa7c7
  box-sizing: border-box;
  color: #ffffff;
  display: flex;
  align-items: center;
  /* 垂直居中 */
  justify-content: center;
  /* 水平居中 */
  font-family: -apple-system, system-ui, "Segoe UI", "Liberation Sans", sans-serif;
  margin: 2px;
  outline: none;
  margin-left: 15px;
}

// .button-mask {
//   background-color: transparent;
//   background-color: #ffffff; //e1ecf4
//   border: none;
//   cursor: pointer;
//   padding: 5px;
//   margin: 0 5px;
//   display: flex;
//   align-items: center;
//   justify-content: center;
// }


// .button-mask img {
//   width: 26px;
//   height: 26px;
//   object-fit: cover;
//   border-radius: 10%;
// }

// mask 没用，得写在script里面
input[type="checkbox"] {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  display: none;
  visibility: hidden;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}


.button-mask+label img {
  width: 26px;
  height: 26px;
  border-radius: 10%;
  margin: 2px 2px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.button-mask:checked+label {
  border: 2px solid #304FFE;
  border-radius: 10%;
}

// .btn svg {
//   // color: #465EEA;
//   color: #a1a1a1;
// }

// .btn:focus svg {
//   // color: #465EEA;
//   color: #465EEA;
// }
// .btn.active>.icon path {
//   fill: #304FFE;
// }

// .icon .selected {
//   width: 10px;
//   height: 10px;
//   fill: #333;
// }

// .icon {
//   width: 20px;
//   height: 20px
// }
</style>
