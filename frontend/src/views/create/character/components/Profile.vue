<script setup>
import {ref, watch} from "vue";
import TextureCard from "@/components/ui/TextureCard.vue";

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
  <TextureCard>
    <fieldset class="create-fieldset">
      <label class="create-label">Profile</label>
      <textarea
          v-model="myProfile"
          rows="6"
          class="textarea textarea-bordered w-full create-textarea"
          placeholder="Describe personality, tone, and background..."
      ></textarea>
    </fieldset>
  </TextureCard>
</template>

<style scoped>
.create-fieldset {
  display: grid;
  gap: 8px;
}

.create-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(15, 23, 42, 0.6);
}

.create-textarea {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(15, 23, 42, 0.1);
  min-height: 160px;
}
</style>
