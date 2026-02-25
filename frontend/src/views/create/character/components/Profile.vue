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
  <fieldset class="fieldset">
    <label for="" class="label text-base">Profile</label>
    <textarea v-model="myProfile" rows="6" class="textare w-108"></textarea>
  </fieldset>
</template>

<style scoped>

</style>