<script setup>
// setup是Vue3的Composition API + 编译期语法糖，无需export default，变量、函数自动暴露给template
/**
 * Photo.vue
 * -----------------
 * 功能：头像上传 + 裁剪组件
 * 描述：
 *  - 父组件传入初始头像（props.photo）
 *  - 用户点击头像上的相机图标选择图片
 *  - 弹出裁剪弹窗（Croppie）
 *  - 裁剪完成后更新头像，并暴露给父组件
 * 技术点：
 *  - Vue 3 Composition API + <script setup>
 *  - 响应式数据管理
 *  - 第三方库 Croppie
 *  - 模态弹窗 dialog
 *  - 隐藏原生文件 input + 自定义触发
 */

import { nextTick, onBeforeMount, ref, useTemplateRef, watch } from "vue";
import CameraIcon from "@/views/user/profile/compoents/icon/CameraIcon.vue";

import Croppie from 'croppie'          // 引入 Croppie 裁剪库
import 'croppie/croppie.css'           // Croppie 样式

/* -------------------- Props & 响应式状态 -------------------- */
const props = defineProps(['photo'])   // 接收父组件传入头像
const myPhoto = ref(props.photo)       // 创建本地可写副本，用于 v-model 和裁剪操作

// 监听父组件更新 avatar 时同步到本地副本
watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})

/* -------------------- 模板引用 -------------------- */
const fileInputRef = useTemplateRef('file-input-ref') // 文件选择 input
const modalRef = useTemplateRef('modal-ref')         // 裁剪弹窗 dialog
const croppieRef = useTemplateRef('croppie-ref')     // Croppie 容器

let croppie = null // Croppie 实例（第三方库实例，不需要响应式）

/* -------------------- 打开裁剪弹窗 -------------------- */
async function openModal(photo) {
  modalRef.value.showModal()   // 打开 dialog
  await nextTick()             // 等 DOM 更新完毕再初始化 Croppie

  // 初始化 Croppie（只初始化一次）
  if (!croppie) {
    croppie = new Croppie(croppieRef.value, {
      viewport: { width: 200, height: 200, type: 'square' }, // 裁剪区域大小
      boundary: { width: 300, height: 300 },                  // 边界容器大小
      enableOrientation: true,    // 支持旋转
      enforceBoundary: true,      // 保证裁剪区域不超出边界
    })
  }

  // 绑定要裁剪的图片
  croppie.bind({
    url: photo,
  })
}

/* -------------------- 执行裁剪操作 -------------------- */
async function crop() {
  if (!croppie) return          // 防御性判断

  // 获取裁剪结果（base64），并更新响应式变量
  myPhoto.value = await croppie.result({
    type: 'base64',
    size: 'viewport',            // 输出与裁剪区域大小一致
  })

  modalRef.value.close()         // 关闭弹窗
}

/* -------------------- 文件选择处理 -------------------- */
function onFileChange(e) {
  const file = e.target.files[0] // 获取用户选择的文件
  e.target.value = ''            // 清空 input，以便可以重复选择同一文件
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    openModal(reader.result)    // 文件读取完成后打开裁剪弹窗
  }
  reader.readAsDataURL(file)    // 转 base64 供 Croppie 使用
}

/* -------------------- 生命周期 -------------------- */
onBeforeMount(() => {
  // 防止组件挂载时遗留 Croppie 实例
  croppie?.destroy()
})

/* -------------------- 暴露给父组件 -------------------- */
defineExpose({
  myPhoto,  // 父组件可直接访问裁剪后的头像
})
</script>

<template>
  <!-- -------------------- 头像显示区 -------------------- -->
  <div class="flex justify-center">
    <div class="avatar relative">
      <!-- 圆形头像 -->
      <div class="w-25 rounded-full">
        <img :src="myPhoto" alt="avatar">
      </div>

      <!-- 点击触发文件选择 -->
      <div @click="fileInputRef.click()"
           class="absolute left-0 top-0 w-25 h-25 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
        <CameraIcon/>
      </div>
    </div>
  </div>

  <!-- -------------------- 隐藏文件 input -------------------- -->
  <input ref="file-input-ref"
         type="file"
         accept="image/*"
         class="hidden"
         @change="onFileChange">

  <!-- -------------------- 裁剪弹窗 -------------------- -->
  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <!-- 关闭按钮 -->
      <button @click="modalRef.close()"
              class="btn btn-circle btn-xs btn-ghost absolute right-2 top-2">✕</button>

      <!-- Croppie 容器 -->
      <div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>

      <!-- 弹窗操作按钮 -->
      <div class="modal-action">
        <div @click="modalRef.close()" class="btn">Cancel</div>
        <div @click="crop" class="btn btn-neutral">Confirm</div>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
/* 样式使用 daisyUI/Tailwind，组件本身无需额外 CSS */
</style>
