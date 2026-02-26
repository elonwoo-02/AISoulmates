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
  <fieldset class="space-y-2">
    <label class="text-sm font-semibold text-[var(--text)]">Profile</label>
    <textarea
      v-model="myProfile"
      rows="6"
      class="w-full resize-none rounded-xl bg-[var(--surface)] px-3 py-2.5 text-[var(--text)] placeholder:text-[var(--muted)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
      placeholder="Tell people about your characters"
    ></textarea>
  </fieldset>
</template>

<style scoped>
</style>


