<script setup>
/**
 * UserEdit.vue
 * ------------
 * 功能：用户资料编辑页面
 * 描述：
 *  - 父组件整合子组件 Photo / Username / Profile
 *  - 用户可编辑头像、用户名、简介
 *  - 点击 Commit 按钮，将修改提交给后端 API
 * 技术点：
 *  - Vue 3 Composition API + <script setup>
 *  - Pinia 状态管理（useUserStore）
 *  - 子组件通过 defineExpose 暴露响应式数据
 *  - 表单验证 + 文件处理（base64 转 File）
 *  - 异步请求提交
 */

import Photo from "@/views/user/profile/compoents/Photo.vue";
import Username from "@/views/user/profile/compoents/Username.vue";
import Profile from "@/views/user/profile/compoents/Profile.vue";

import { useUserStore } from "@/stores/user.js";
import { ref, useTemplateRef } from "vue";
import { base64ToFile } from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";

/* -------------------- 用户状态 -------------------- */
const user = useUserStore() // 获取 Pinia 用户状态

/* -------------------- 子组件引用 -------------------- */
// 子组件均已通过 defineExpose 暴露内部响应式变量
// 通过 useTemplateRef 获取 template 中的 ref 对象
const photoRef = useTemplateRef('photo-ref')       // Photo.vue 的 myPhoto
const profileRef = useTemplateRef('profile-ref')   // Profile.vue 的 myProfile
const usernameRef = useTemplateRef('username-ref') // Username.vue 的 myUsername

/* -------------------- 错误信息 -------------------- */
const errorMessage = ref('')  // 表单验证错误提示

/* -------------------- 提交更新 -------------------- */
async function handleUpdate() {
  // 从子组件获取最新数据
  const photo = photoRef.value.myPhoto
  const username = usernameRef.value.myUsername.trim()
  const profile = profileRef.value.myProfile.trim()

  // 重置错误信息
  errorMessage.value = ''

  // -------------------- 表单验证 --------------------
  if (!photo) {
    errorMessage.value = 'avatar is required'
  } else if (!username) {
    errorMessage.value = 'username is required'
  } else if (!profile) {
    errorMessage.value = 'profile is required'
  } else {
    // -------------------- 构建 FormData --------------------
    const formData = new FormData()
    formData.append('username', username)
    formData.append('profile', profile)

    // 如果头像有变化，将 base64 转 File 再上传
    if (photo !== user.photo) {
      formData.append('photo', base64ToFile(photo, 'photo.png'))
    }

    // -------------------- 发送请求 --------------------
    try {
      const res = await api.post('/api/user/profile/update', formData)
      const data = res.data

      // -------------------- 成功处理 --------------------
      if (data.result === 'success') {
        // 更新全局用户信息
        user.setUserInfo(data)
      } else {
        // 后端返回错误信息
        errorMessage.value = data.result
      }
    } catch (err) {
      // 捕获请求异常（可选打印）
      // console.log(err)
    }
  }
}
</script>

<template>
  <!-- -------------------- 页面容器 -------------------- -->
  <div class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-0">
      <div class="card-body">

        <!-- 页面标题 -->
        <h3 class="text-lg font-bold my-4">Edit Profile</h3>

        <!-- 子组件区域 -->
        <Photo ref="photo-ref" :photo="user.photo"/>
        <Username ref="username-ref" :username="user.username"/>
        <Profile ref="profile-ref" :profile="user.profile"/>

        <!-- 错误提示 -->
        <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>

        <!-- 提交按钮 -->
        <div class="flex justify-center">
          <button @click="handleUpdate" class="btn btn-neutral w-60 mt-2">Commit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 样式由 Tailwind CSS / daisyUI 控制 */
/* card、btn、text-red-500 等类名均为 UI 框架预设 */
</style>