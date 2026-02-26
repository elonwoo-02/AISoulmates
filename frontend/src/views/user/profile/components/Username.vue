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
  <fieldset class="space-y-2">
    <label for="username" class="text-sm font-semibold text-[var(--text)]">Username</label>
    <input
      id="username"
      v-model="myUsername"
      type="text"
      class="w-full rounded-xl bg-[var(--surface)] px-3 py-2.5 text-[var(--text)] placeholder:text-[var(--muted)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
      placeholder="Enter your channel name"
    />
  </fieldset>
</template>

<style scoped>
</style>


