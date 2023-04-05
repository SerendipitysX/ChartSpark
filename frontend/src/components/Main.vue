<!--
 * @Description: 
 * @Author: Qing Shi
 * @Date: 2022-11-20 23:25:35
 * @LastEditTime: 2023-01-27 08:31:53
-->
<template>
    <div style="padding-top: 10vh; font-family: Quicksand;">
        <div class="logo" style="margin-bottom: 16px;">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-brand-docker" width="100"
                height="100" viewBox="0 0 24 24" stroke-width="1" stroke="black" fill="none" stroke-linecap="round"
                stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <path
                    d="M22 12.54c-1.804 -.345 -2.701 -1.08 -3.523 -2.94c-.487 .696 -1.102 1.568 -.92 2.4c.028 .238 -.32 1.002 -.557 1h-14c0 5.208 3.164 7 6.196 7c4.124 .022 7.828 -1.376 9.854 -5c1.146 -.101 2.296 -1.505 2.95 -2.46z" />
                <path d="M5 10h3v3h-3z" />
                <path d="M8 10h3v3h-3z" />
                <path d="M11 10h3v3h-3z" />
                <path d="M8 7h3v3h-3z" />
                <path d="M11 7h3v3h-3z" />
                <path d="M11 4h3v3h-3z" />
                <path d="M4.571 18c1.5 0 2.047 -.074 2.958 -.78" />
                <line x1="10" y1="16" x2="10" y2="16.01" />
            </svg>
            <h1 style="color: black; font-family: Quicksand,system-ui; font-size: 1.875rem; font-weight: 600;">
                NFTSearcher</h1>
            <p style="color: rgba(96, 98, 102); font-family: Quicksand,system-ui; font-size: 1rem;">A search engine for
                NFTs. Choose from
                millions of NFTs that best suit your preferences!</p>
        </div>
        <el-form :model="formData">
            <el-form-item label="">
                <!-- <el-input v-model="form.name" :input-style="{
                    'margin-left': '10px',
                    'margin-right': '10px',
                }"/> -->
                <el-input v-model="formData.name" placeholder="Please input" class="input-with-select">
                    <!-- <template #append>
                        <el-select v-model="select" placeholder="Select" style="width: 115px">
                            <el-option label="Restaurant" value="1" />
                            <el-option label="Order No." value="2" />
                            <el-option label="Tel" value="3" />
                        </el-select>
                    </template> -->
                    <template #append>

                        <div style="width: 50px; margin-top: -10px;">
                            <el-button @click="showMoreSearch()">
                                <el-icon :size="25" style="vertical-align: middle">
                                    <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" data-v-029747aa=""
                                        :transform="translate(0, 0, -90 * moreSearch)">
                                        <path fill="currentColor"
                                            d="M452.864 149.312a29.12 29.12 0 0 1 41.728.064L826.24 489.664a32 32 0 0 1 0 44.672L494.592 874.624a29.12 29.12 0 0 1-41.728 0 30.592 30.592 0 0 1 0-42.752L764.736 512 452.864 192a30.592 30.592 0 0 1 0-42.688zm-256 0a29.12 29.12 0 0 1 41.728.064L570.24 489.664a32 32 0 0 1 0 44.672L238.592 874.624a29.12 29.12 0 0 1-41.728 0 30.592 30.592 0 0 1 0-42.752L508.736 512 196.864 192a30.592 30.592 0 0 1 0-42.688z">
                                        </path>
                                    </svg>
                                </el-icon>
                            </el-button>
                        </div>
                        <div style="width: 50px; margin-top: -10px;">
                            <el-button @click="nftSearch()">
                                <el-icon :size="25" style="vertical-align: middle">
                                    <Search />
                                </el-icon>
                            </el-button>
                        </div>
                        <div style="width: 50px; margin-top: -10px;">
                            <el-button ref="img_button" @click="submitForm($event)">
                                <el-icon :size="25" style="vertical-align: middle">
                                    <Camera />
                                </el-icon>
                            </el-button>

                            <input ref="img_sub" type="file" name="img" id="pic_img" style="display: none;"
                                @change="getFile($event)">
                        </div>
                        <!-- <el-button :icon="Search" />
                        <el-button :icon="Search" /> -->
                    </template>
                </el-input>
            </el-form-item>
            <div v-show="moreSearch == -1 ? 0 : 1"
                style="border: 1px solid rgb(220, 223, 230); padding: 20px; border-radius: 15px; width: calc(100% - 195px); font-weight: bold; margin-bottom: 30px; float: left;">
                <div style="float: left; font-family: Quicksand;">Market Features</div>
                <br>
                <br>
                <el-form-item label="Price">
                    <el-input v-model="formData.price" placeholder="the highest price, continuous rise" :input-style="{
                        'float': 'right'
                    }" />
                </el-form-item>
                <el-form-item label="Rarity">
                    <el-input v-model="formData.rarity" placeholder="rarest" />
                </el-form-item>
                <el-form-item label="Collection">
                    <el-input v-model="formData.collection" placeholder="Doodles" />
                </el-form-item>
                <div style="float: left; font-family: Quicksand;">NFT Features</div>
                <br>
                <br>
                <el-form-item label="Background Color">
                    <el-input v-model="formData.backgroundColor" placeholder="red, blue, green" :input-style="{
                        'float': 'right'
                    }" />
                </el-form-item>
                <el-form-item label="Style">
                    <el-input v-model="formData.style" placeholder="sketch, comic" />
                </el-form-item>
                <div style="float: left; font-family: Quicksand;">Personal Features
                    <el-button :style="{ 'border-radius': '30px', 'padding': '8px' }" @click="open()">
                        <el-icon>
                            <Plus />
                        </el-icon>
                    </el-button>
                </div>
                <br>
                <br>
                <el-form-item v-for="(item, i) in addFeature" :key="'F' + i" :label="item">
                    <el-input v-model="formData[item]" :input-style="{
                        'float': 'right'
                    }" />
                </el-form-item>
            </div>
            <div v-if="imgURL != ''"
                style="border: 1px solid rgb(220, 223, 230); padding: 20px; border-radius: 15px; width: calc(190px); font-weight: bold; margin-bottom: 30px; float: right;">
                <div style="float: left; font-family: Quicksand;">Selected Image</div>
                <br>
                <br>
                <img :src="imgURL" alt="selected image" style="border: 1px solid rgb(220, 223, 230)" width="150">
            </div>
        </el-form>
    </div>
</template>
<script>
import { Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router';
import { dataService } from '@/service';
import { useDataStore } from "../stores/counter";
import { postImg, postText } from '../service/module/dataService'
export default {
    name: 'APP',
    props: ["msgH"],
    data() {
        return {
            msg1: "Hello, main!",
            moreSearch: -1,
            formData: {
                name: '',
                region: '',
                price: '',
                rarity: '',
                collection: '',
                backgroundColor: '',
                style: '',
                type: '',
            },
            imgData: {
                accept: "image/png, image/jpeg, image/jpg"
            },
            addFeature: [],
            file: '',
            imgURL: ''
        }
    },
    methods: {
        translate(x, y, r) {
            return `translate(${x}, ${y}) rotate(${r})`;
        },
        jump() {
            // const router = useRouter();
            this.$router.push({ path: 'result' });
        },
        nftSearch() {
            const dataStore = useDataStore();
            // Image
            if (this.file != '' && this.formData.name == '') {
                let formData = new FormData();
                formData.append('image', this.file);
                // console.log(this.file, formData);
                postImg(formData, res => {
                    console.log(res);
                    this.jump();
                });
            }
            // Text
            else if (this.file == '' && this.formData.name != '') {
                let formData = new FormData();
                let inputText=this.formData.name
                for (let key in this.formData){
                    if (this.formData[key]!='' && key!='name')
                    {
                        inputText=inputText+"/"+key+": "+this.formData[key]
                    }
                }
                console.log(inputText)
                formData.append('text', inputText);
                // console.log(this.file, formData);
                postText(formData, res => {
                    console.log(res);
                    this.jump();
                });
            }
        },
        getFile(event) {
            // console.log(event.target.files);
            this.file = event.target.files[0];
            // console.log(this.file);
            event.preventDefault();
            let type = this.file.type;
            let size = this.file.size;
            // if (this.imgData.accept.indexOf(type) == -1) {
            //     ElMessage({
            //         type: 'error',
            //         message: 'Invalid Image Format',
            //     })
            // }
            let URL = window.URL || window.webkitURL;
            let imgURL = URL.createObjectURL(this.file);
            this.imgURL = imgURL;
            const dataStore = useDataStore();
            dataStore.imgFile = this.file;
        },
        submitForm(event) {
            this.$refs.img_sub.dispatchEvent(new MouseEvent('click'))

        },
        open() {
            const vm = this;
            ElMessageBox.prompt('Please add a feature', 'Feature Adding', {
                confirmButtonText: 'Add',
                cancelButtonText: 'Cancel',
                inputPattern: ''
            })
                .then(({ value }) => {
                    vm.addNFTFeature(value);
                    vm.formData[value] = null;
                    ElMessage({
                        type: 'success',
                        message: `Successfully added feature: ${value}`,
                    })
                })
        },
        showMoreSearch() {
            this.moreSearch = -this.moreSearch;
            // console.log(this.moreSearch)
        },
        addNFTFeature(featureName) {
            this.addFeature.push(featureName);
        }
    },
    created() {
    },
    mounted() {
        // this.$refs.img_button.click(() => {
        //     this.$refs.img_sub.change();
        // })
    },
    watch: {
        formData() {
            console.log(this.formData);
        }
    }
}
</script>
<style scoped>
.el-input {
    --el-input-border-radius: 25px;
    height: 35px;
    font-size: 15px;
    font-family: Quicksand, system-ui;
    color: black
        /* padding-right: 15%; */
}

.el-form-item__content {
    background-color: #0000;
}
</style>
