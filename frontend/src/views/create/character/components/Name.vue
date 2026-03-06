<script setup>
import {ref, watch} from "vue";

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
  <fieldset class="space-y-1">
    <label for="name" class="text-sm font-medium text-base-content/80">Name</label>
    <input
      id="name"
      v-model="myName"
      type="text"
      class="input w-full rounded-xl border-base-300 bg-base-100"
      placeholder="Character name"
    />
  </fieldset>
</template>

<style scoped>
</style>
