<script setup>
import {useRoute} from "vue-router";

const route = useRoute() // 取当前url包含的信息
</script>

<template>
个人空间 {{ route.params.user_id }}
</template>

<style scoped>

</style>