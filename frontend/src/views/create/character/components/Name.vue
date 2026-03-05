<script setup>
import {ref, watch} from "vue";
import TextureCard from "@/components/ui/TextureCard.vue";

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
  <TextureCard>
    <fieldset class="create-fieldset">
      <label class="create-label">Name</label>
      <input
          v-model="myName"
          type="text"
          class="input input-bordered w-full create-input"
          placeholder="Character name"
      >
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

.create-input {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(15, 23, 42, 0.1);
}
</style>
