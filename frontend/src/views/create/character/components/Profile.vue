<script setup>
import {ref, watch} from "vue";

const props = defineProps(['profile'])

const myProfile = ref(props.profile)

watch(() => props.profile, newVal => {
  myProfile.value = newVal
})

defineExpose({
  myProfile
})
</script>

<template>
  <fieldset class="space-y-1">
    <label for="profile" class="text-sm font-medium text-base-content/80">Profile</label>
    <textarea
      id="profile"
      v-model="myProfile"
      rows="6"
      class="textarea w-full rounded-xl border-base-300 bg-base-100"
      placeholder="Describe personality, tone, and background..."
    ></textarea>
  </fieldset>
</template>

<style scoped>
</style>
