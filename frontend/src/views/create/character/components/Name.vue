<script setup>
import { ref, watch } from "vue";

const props = defineProps(['name'])
const myName = ref(props.name)

watch(() => props.name, newVal => {
  myName.value = newVal
})

defineExpose({
  myName
})
</script>

<template>
  <fieldset class="space-y-2">
    <label class="text-sm font-semibold text-[var(--text)]">Name</label>
    <input v-model="myName" type="text" class="w-full rounded-xl bg-[var(--surface)] px-3 py-2.5 text-[var(--text)] placeholder:text-[var(--muted)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]">
  </fieldset>
</template>

<style scoped>
</style>


