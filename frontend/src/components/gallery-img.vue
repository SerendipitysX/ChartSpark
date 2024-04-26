<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-06 23:20:40
 * @Description: 图层面板
-->

<template>
    <div class="gallery">

    </div>
</template>
  
<script setup>
import { ref } from 'vue'; // import ref from vue 
import { px } from 'framer-motion';
import { useI18n } from 'vue-i18n';
import mitt from 'mitt';
import { method } from 'lodash';
import { useGenerateStore } from '../store/modules/generateStore';

// import { EventBus } from '/src/core/eventBus/index.js';
// const imgSrc = ref('/src/assets/generation/default.jpg'); 
const imgSrc = ref('/src/assets/generation/1.png');
const object = ref("object")
const description = ref("description")
const generateLabel = ref("xx")
const eventBus = inject("eventBus")
const isAddRow = ref(false);

const store = useGenerateStore()
const canvas = inject("canvas")
// canvas.c.add(text)

function clickButton() {
    console.log(imgSrc)
    imgSrc.value = '/src/assets/generation/default.jpg'
};

function clickRow(event) {
    // console.log("------------------------")
    const gallery = document.querySelector('.gallery');
    const prevGrayRow = gallery.querySelector('.gray-background');
    if (prevGrayRow) {
        prevGrayRow.classList.remove('gray-background');
    }
    event.currentTarget.classList.add('gray-background');
    const objectInfo = event.currentTarget.querySelector('.object-info').textContent;
    store.objectText = objectInfo;;
    const descriptionInfo = event.currentTarget.querySelector('.description-info').textContent;
    store.descriptionText = descriptionInfo;
    // store.generateMethod = data.generateMethod;
    // console.log(store.objectText, store.descriptionText)
    const totalItems = event.currentTarget.querySelectorAll('.gallery-item').length;
    // Get the number of gallery-items without an img element
    const emptyItems = event.currentTarget.querySelectorAll('.gallery-item:not(:has(img))').length;
    // Return the number of empty gallery-items
    const numEmptyItems = totalItems - emptyItems;
    store.generateNum = emptyItems
    // console.log(numEmptyItems);
    eventBus.emit("backTracking", {
        message: "previous state of generation."
    });
    store.isClickRow = numEmptyItems
}

// function clickImg(event) {
//     const objectInfo = event.currentTarget.querySelector('.img').textContent;
//     console.log(objectInfo)
// }

onMounted(() => {
    eventBus.on("isGenerate", (data) => {
        // console.log(data)
        // console.log(store.generationStateList)
        store.objectText = data.object;
        store.descriptionText = data.description;
        store.generateMethod = data.generateMethod;
        // const c = JSON.stringify(data.addRow)
        if (data.addRow == true) {
            // console.log(data.addRow)
            console.log("yes, add a row")
            setTimeout(()=>{addRow(data)}, 2000);
        }
        else {
            // console.log(data.addRow)
            console.log("no, not a row")
            setTimeout(()=>{modifyRow(data)}, 1200);
        }
    });
    eventBus.on("isRefine", (data) => {
        console.log("refine!")
        setTimeout(()=>{addRefine(data)}, 1500);
    });
})

function modifyRow(data) {
    // 获取具有gray-background类的元素，也就是当前被点击的gallery-row
    const row = document.querySelector('.gray-background');

    // 获取当前row中所有的gallery-item
    const items = row.querySelectorAll('.gallery-item');

    // 遍历items数组，查找哪些item没有img
    let i = 0
    // items.forEach(item => {
    //     if (!item.querySelector('img')) {
    //         // item.innerHTML += `${data.imgList[i]}`;
    //         item.insertBefore(`${data.imgList[i]}`, item.querySelector('button'));
    //         i++;
    //     }
    // });
    items.forEach(item => {
        if (!item.querySelector('img')) {
            item.innerHTML = `<img src=${data.imgList[i]} alt="这是一张图片">` + item.innerHTML;
            i++;
        }
    });
    const imgButtons = row.querySelectorAll('.gallery-item-button');
    imgButtons.forEach(button => {
        const img = button.previousElementSibling;
        img.addEventListener('click', () => {
            fabric.Image.fromURL(img.src, function (imgInstance) {
                imgInstance.set({  // 设置图片属性
                    name: data.object // 添加名字
                });
                canvas.c.add(imgInstance);
            });
        });
        button.addEventListener('click', () => {
            img.remove();
            // button.remove(); 
        });
    });

}

const addRow = (data) => {
    // Get the gallery element
    const gallery = document.querySelector('.gallery');

    // Create a new gallery-row element 
    const newRow = document.createElement('div');
    newRow.classList.add('gallery-row');
    newRow.addEventListener('click', clickRow);

    // Add the info element to the new row
    const newInfo = document.createElement('div');
    newInfo.classList.add('info');
    // <img src=${data.imgList[0]}>  
    newInfo.innerHTML = `
  <div class="object-info">${data.object}</div>  
  <div class="description-info">${data.description}</div>  
  <div style="display: flex;">
  <button class="generate-method-${data.generateMethod}"><strong>${data.generateMethod}</strong></button>  
  <button class="guide-C"><strong>${data.guide}</strong></button>  
</div>
`;
    newRow.appendChild(newInfo);

    // Add the gallery-group element to the new row
    const newGalleryGroup = document.createElement('div');
    newGalleryGroup.classList.add('gallery-group');
    newGalleryGroup.innerHTML = `
  <div class="gallery-item">  
    <img src=${data.imgList[0]} alt="这是一张图片">
    <button class="gallery-item-button" role="button">X</button>  
  </div>  
  <div class="gallery-item">  
    <img src=${data.imgList[1]} alt="这是一张图片">
    <button class="gallery-item-button" role="button" @click="clickButton">X</button>  
  </div>  
  <div class="gallery-item">  
    <img src=${data.imgList[2]} alt="这是一张图片">
    <button class="gallery-item-button" role="button" @click="clickButton">X</button>  
  </div>  
  <div class="gallery-item">  
    <img src=${data.imgList[3]} alt="这是一张图片">
    <button class="gallery-item-button" role="button" @click="clickButton">X</button>  
  </div>  
`;
    newRow.appendChild(newGalleryGroup);

    // 给img加上监听事件
    const galleryRows = document.querySelectorAll('.gallery-row');
    for (let i = 0; i < galleryRows.length; i++) {
        console.log(i)
        const img = galleryRows[i].querySelector('img');
        img.addEventListener('click', () => {
            // const imgInstance = new fabric.Image(img, {
            //     id: uuid(),
            //     name: '图片1',
            //     left: 100, top: 100,
            // });
            // canvas.c.add(imgInstance)
            // canvas.c.setActiveObject(imgInstance);
            // canvas.c.renderAll()
            console.log("点击img")
        });
    }

    // Insert the new row before the first row 
    const firstRow = gallery.querySelector('.gallery-row');
    gallery.insertBefore(newRow, firstRow);

    function removeImg(button) {
        console.log("remove it?")
        console.log(button.parentNode)
        button.parentNode.remove();
    }

    const imgButtons = newRow.querySelectorAll('.gallery-item-button');
    // imgButtons.forEach(button => {
    //     button.addEventListener('click', () => {
    //         button.parentNode.remove();
    //     });
    // });
    imgButtons.forEach(button => {
        const img = button.previousElementSibling;
        img.addEventListener('click', () => {
            fabric.Image.fromURL(img.src, function (imgInstance) {
                imgInstance.set({  // 设置图片属性
                    id: data.object // 添加名字
                });
                canvas.c.add(imgInstance);
            });
        });
        button.addEventListener('click', () => {
            img.remove();
            // button.remove(); 
        });
    });
}

const addRefine = (data) => {
    // Get the gallery element
    const gallery = document.querySelector('.gallery');

    // Create a new gallery-row element 
    const newRow = document.createElement('div');
    newRow.classList.add('gallery-row');
    // newRow.addEventListener('click', clickRow);

    // Add the info element to the new row
    const newInfo = document.createElement('div');
    newInfo.classList.add('info');
    newInfo.innerHTML = `
  <button class="guide-C"><strong>REFINE</strong></button>  
`;
    newRow.appendChild(newInfo);

    // Add the gallery-group element to the new row
    const newGalleryGroup = document.createElement('div');
    newGalleryGroup.classList.add('gallery-group');
    newGalleryGroup.innerHTML = `
  <div class="gallery-item">  
    <img src=${data.imgList[0]} alt="这是一张图片">
    <button class="gallery-item-button" role="button">X</button>  
  </div>  
  <div class="gallery-item">  
    <img src=${data.imgList[1]} alt="这是一张图片">
    <button class="gallery-item-button" role="button" @click="clickButton">X</button>  
  </div>  
  <div class="gallery-item">  
    <img src=${data.imgList[2]} alt="这是一张图片">
    <button class="gallery-item-button" role="button" @click="clickButton">X</button>  
  </div>  
  <div class="gallery-item">  
    <img src=${data.imgList[3]} alt="这是一张图片">
    <button class="gallery-item-button" role="button" @click="clickButton">X</button>  
  </div>  
`;
    newRow.appendChild(newGalleryGroup);

    // 给img加上监听事件
    const galleryRows = document.querySelectorAll('.gallery-row');
    for (let i = 0; i < galleryRows.length; i++) {
        console.log(i)
        const img = galleryRows[i].querySelector('img');
        img.addEventListener('click', () => {
            // const imgInstance = new fabric.Image(img, {
            //     id: uuid(),
            //     name: '图片1',
            //     left: 100, top: 100,
            // });
            // canvas.c.add(imgInstance)
            // canvas.c.setActiveObject(imgInstance);
            // canvas.c.renderAll()
            console.log("点击img")
        });
    }

    // Insert the new row before the first row 
    const firstRow = gallery.querySelector('.gallery-row');
    gallery.insertBefore(newRow, firstRow);

    function removeImg(button) {
        console.log("remove it?")
        console.log(button.parentNode)
        button.parentNode.remove();
    }

    const imgButtons = newRow.querySelectorAll('.gallery-item-button');
    // imgButtons.forEach(button => {
    //     button.addEventListener('click', () => {
    //         button.parentNode.remove();
    //     });
    // });
    imgButtons.forEach(button => {
        const img = button.previousElementSibling;
        img.addEventListener('click', () => {
            fabric.Image.fromURL(img.src, function (imgInstance) {
                imgInstance.set({  // 设置图片属性
                    id: data.object // 添加名字
                });
                canvas.c.add(imgInstance);
            });
        });
        button.addEventListener('click', () => {
            img.remove();
            // button.remove(); 
        });
    });
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

.gallery {
    overflow-y: scroll;
    /* add a scrollbar to the y-axis */
    width: 98%;
    margin: 1%;
    margin-top: 10px;
    height: 98%;
    background-color: white;
}

.gray-background {
    //   background-color: rgba(245,245,245,1);
    box-shadow: inset 0 0 3px #7e7e7e;
    border: 2px solid #646464;
}

.gallery-row:focus {
    box-shadow: inset 0 0 3px #c4c4c4;
}

.gallery-row {
    display: flex;
    width: 96%;
    height: 110px;
    justify-content: center;
    align-items: center;
    border-radius: 7px;
    // border: 1px solid rgb(181, 181, 181);
    border: 1px solid #b5b5b5;
    padding: 8px;
    margin: 0px auto;
    margin-left: 0px;
    margin-bottom: 10px;
}

.gallery-group {
    display: flex;
    width: 75%;
    height: 100%;
    justify-content: space-evenly;
    margin-right: -10px;
}

.info {
    width: 25%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    /* horizontally center contents */
    align-items: center;
    /* vertically center contents */
}

.object-info {
    width: 80%;
    height: 35%;
    font-size: 10px;
    font-family: "DM Sans", sans-serif;
    border: 1px solid rgb(255, 255, 255);
    border-radius: 5px;
    background-color: rgb(243, 243, 243);
    padding: 5px;
    text-align: center;
    color: #636262;
    margin-bottom: 5px;
    word-wrap: break-word;
    display: flex;
    text-align: center;
    justify-content: center;
    align-items: center;

}

.description-info {
    width: 80%;
    height: 35%;
    font-size: 10px;
    font-family: "DM Sans", sans-serif;
    border: 1px solid rgb(255, 255, 255);
    border-radius: 5px;
    background-color: rgb(243, 243, 243);
    padding: 5px;
    text-align: center;
    color: #636262;
    margin-bottom: 5px;
    word-wrap: break-word;
}

.generate-method-F {
    // margin-left: -2px;
    background-color: #CDE7F8;
    width: 75px;
    height: 20px;
    border: 0px solid #5B97BD;
    border-radius: 10px;
    display: flex;
    font-size: 10px;
    font-weight: 540;
    padding-left: 27px;
    padding-right: 20px;
    color: #2F75A1;
    position: relative;
    margin-top: 2px;
    margin-right: 10px;
    text-align: center;
    justify-content: center;
    align-items: center;
}

.generate-method-F::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translate(0, -50%);
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background-color: #5B97BD;
    // border: 1.5px solid #5B97BD;
    margin-left: 8px;
}

.generate-method-B {
    // margin-left: -2px;
    background-color: #F5CAC2;
    width: 75px;
    height: 20px;
    border: 0px solid #C84444;
    border-radius: 10px;
    display: flex;
    font-size: 10px;
    font-weight: 540;
    padding-left: 27px;
    padding-right: 20px;
    color: #C84444;
    position: relative;
    margin-top: 2px;
    text-align: center;
    justify-content: center;
    align-items: center;
}

.generate-method-B::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translate(0, -50%);
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background-color: #C84444;
    // border: 1.5px solid #5B97BD;
    margin-left: 8px;
}

.guide-C {
    // margin-left: -2px;
    background-color: #e2e2e2;
    width: 75px;
    height: 20px;
    border: 0px solid #ababab;
    border-radius: 10px;
    display: flex;
    font-size: 10px;
    font-weight: 540;
    padding-left: 27px;
    padding-right: 20px;
    color: #383838;
    position: relative;
    margin-top: 2px;
    text-align: center;
    justify-content: center;
    align-items: center;
}

.guide-C::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translate(0, -50%);
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background-color: #ababab;
    // border: 1.5px solid #5B97BD;
    margin-left: 8px;
}


.gallery-item {
    position: relative;
    width: 22%;
    /* adjust width as needed */
    height: 100%;
    border: 1px solid rgb(216, 216, 216);
    background-color: white;
    border-radius: 7px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 2px 2px 5px rgba(110, 110, 110, 0.3);
    margin-right: -10px;
    /* create 10px space between items */
}

.gallery-item-button {
    position: absolute;
    top: 3px;
    right: 3px;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    border: none;
    background: rgb(229, 229, 229, 0.5);
    outline: none;
    color: #888;
    text-align: center;
    font-size: 5px;
    padding-left: 4px;
}

.gallery-item img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 7px;
}

.gallery-item-button:hover {
    background-color: #cedbe4;
    color: #2c5777;
}

.gallery-item-button:active {
    background-color: #a0c7e4;
    box-shadow: none;
    // color: #2c5777;
}


.gallery::-webkit-scrollbar {
    width: 7px;
    height: 10px;
    background-color: #F5F5F5;
}

.gallery::-webkit-scrollbar-thumb {
    border-radius: 10px;
    background-color: #888;
}

.gallery::-webkit-scrollbar-thumb:hover {
    background-color: #555;
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
</style>
  