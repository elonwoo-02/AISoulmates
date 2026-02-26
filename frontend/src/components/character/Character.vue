<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user.js'
import UpdateIcon from '@/components/character/icons/UpdateIcon.vue'
import RemoveIcon from '@/components/character/icons/RemoveIcon.vue'
import api from '@/js/http/api.js'

const props = defineProps(['character', 'canEdit'])
const emit = defineEmits(['remove'])
const isHover = ref(false)
const user = useUserStore()

async function handleRemoveCharacter() {
  try {
    const res = await api.post('/api/create/character/remove/', {
      character_id: props.character.id,
    })
    if (res.data.result === 'success') {
      emit('remove', props.character.id)
    }
  } catch {
    // Keep silent to match current behavior.
  }
}
</script>

<template>
  <article
    class="group overflow-hidden rounded-2xl border border-base-300 bg-base-100 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
    @mouseover="isHover = true"
    @mouseleave="isHover = false"
  >
    <div class="relative aspect-video overflow-hidden bg-base-200">
      <img
        :src="character.background_image"
        class="h-full w-full object-cover transition-transform duration-300"
        :class="{ 'scale-105': isHover }"
        alt="character background"
      />
      <div class="absolute inset-0 bg-linear-to-t from-black/50 via-black/10 to-transparent"></div>

      <div
        v-if="canEdit && character.author.user_id === user.id"
        class="absolute right-2 top-2 flex gap-1 opacity-0 transition-opacity group-hover:opacity-100"
      >
        <RouterLink :to="{ name: 'update-character', params: { character_id: character.id } }" class="btn btn-circle btn-ghost btn-xs bg-black/35 text-white hover:bg-black/55">
          <UpdateIcon />
        </RouterLink>
        <button @click="handleRemoveCharacter" class="btn btn-circle btn-ghost btn-xs bg-black/35 text-white hover:bg-black/55">
          <RemoveIcon />
        </button>
      </div>
    </div>

    <div class="flex gap-3 p-3">
      <div class="avatar mt-0.5">
        <div class="h-10 w-10 rounded-full">
          <img :src="character.photo" alt="character avatar" class="object-cover" />
        </div>
      </div>

      <div class="min-w-0 flex-1">
        <h3 class="line-clamp-2 break-all text-sm font-semibold leading-5">{{ character.name }}</h3>
        <p class="line-clamp-2 mt-1 text-xs text-base-content/70">{{ character.profile }}</p>

        <RouterLink
          :to="{ name: 'user-space-index', params: { user_id: character.author.user_id } }"
          class="mt-2 inline-flex max-w-full items-center gap-2 text-xs text-base-content/70 hover:text-base-content"
        >
          <span class="avatar">
            <span class="h-5 w-5 overflow-hidden rounded-full">
              <img :src="character.author.photo" alt="author avatar" class="h-full w-full object-cover" />
            </span>
          </span>
          <span class="truncate">{{ character.author.username }}</span>
        </RouterLink>
      </div>
    </div>
  </article>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
