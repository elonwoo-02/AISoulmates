<script setup>
import { ref, watch } from 'vue'

const props = defineProps(['username'])
const myUsername = ref(props.username)

watch(
  () => props.username,
  newVal => {
    myUsername.value = newVal
  },
)

defineExpose({
  myUsername,
})
</script>

<template>
  <fieldset class="space-y-1">
    <label for="username" class="text-sm font-medium text-base-content/80">Username</label>
    <input
      id="username"
      v-model="myUsername"
      type="text"
      class="input w-full rounded-xl border-base-300 bg-base-100"
      placeholder="Enter your channel name"
    />
  </fieldset>
</template>

<style scoped>
</style>