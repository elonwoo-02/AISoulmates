<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/js/http/api.js'

const router = useRouter()
const characters = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await api.get('/api/create/character/list/')
    const data = res.data
    if (data.result === 'success') {
      characters.value = data.characters
    } else {
      error.value = data.result
    }
  } catch {
    error.value = 'Failed to load characters'
  } finally {
    loading.value = false
  }
})

function goToUpdate(characterId) {
  router.push({
    name: 'update-character',
    params: { character_id: characterId },
  })
}

function goToCreate() {
  router.push({
    name: 'create-index',
  })
}
</script>

<template>
  <div class="mx-auto w-full max-w-7xl px-4 py-6 md:px-6 lg:px-8">
    <header class="mb-6 flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Channel characters</h1>
        <p class="mt-1 text-sm text-base-content/70">Manage your published characters</p>
      </div>
      <button @click="goToCreate" class="btn btn-neutral rounded-full">Create character</button>
    </header>

    <div v-if="loading" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else-if="error" class="alert alert-error">
      <span>{{ error }}</span>
    </div>

    <div v-else-if="characters.length === 0" class="rounded-2xl border border-dashed border-base-300 bg-base-100 p-10 text-center">
      <p class="text-base-content/70">You have not created any characters yet.</p>
      <button @click="goToCreate" class="btn btn-primary mt-4 rounded-full">Create your first character</button>
    </div>

    <div v-else class="space-y-3">
      <article
        v-for="character in characters"
        :key="character.id"
        class="group cursor-pointer rounded-2xl border border-base-300 bg-base-100 p-3 shadow-sm transition-all hover:shadow-md"
        @click="goToUpdate(character.id)"
      >
        <div class="flex items-center gap-4">
          <div class="avatar">
            <div class="h-16 w-16 rounded-xl">
              <img :src="character.photo" :alt="character.name" class="object-cover" />
            </div>
          </div>

          <div class="min-w-0 flex-1">
            <h2 class="truncate text-base font-semibold">{{ character.name }}</h2>
            <p class="line-clamp-2 mt-1 text-sm text-base-content/70">{{ character.profile }}</p>
            <p class="mt-1 text-xs text-base-content/60">
              Updated {{ new Date(character.update_time).toLocaleDateString() }}
            </p>
          </div>

          <button class="btn btn-ghost btn-sm rounded-full">Edit</button>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>