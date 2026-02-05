<script setup>
import {ref, watch} from "vue";

const props = defineProps(['username'])
const myUsername = ref(props.username)

watch(() => props.username, newVal => {
  myUsername.value = newVal
})

defineExpose({
  myUsername
})
</script>

<!--
 ProfileIndex username
      ↓
 props.username   （只读）
      ↓
 myUsername (ref) （可编辑）
      ↓
   v-model 输入框
-->

<template>
  <fieldset class="fieldset">
    <label for="username" class="label text-base">Username</label>
    <input id="username" v-model="myUsername" type="text" class="input w-108">
  </fieldset>
</template>

<style scoped>
/* 样式使用 daisyUI/Tailwind，组件本身无需额外 CSS */
</style>