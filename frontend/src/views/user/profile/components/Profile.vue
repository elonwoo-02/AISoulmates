<script setup>
import { ref, watch } from 'vue'

const props = defineProps(['profile'])
const myProfile = ref(props.profile)

watch(
  () => props.profile,
  newVal => {
    myProfile.value = newVal
  },
)

defineExpose({
  myProfile,
})
</script>

<template>
  <fieldset class="space-y-1">
    <label class="text-sm font-medium text-base-content/80">Profile</label>
    <textarea
      v-model="myProfile"
      rows="6"
      class="textarea w-full rounded-xl border-base-300 bg-base-100"
      placeholder="Tell people about your characters"
    ></textarea>
  </fieldset>
</template>

<style scoped>
</style>