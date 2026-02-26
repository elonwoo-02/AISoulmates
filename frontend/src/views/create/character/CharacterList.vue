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
  <main class="page-shell pb-12">
    <section class="glass-panel p-6 md:p-8">
      <header class="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 class="brand-font text-3xl tracking-tight">Channel Characters</h1>
          <p class="mt-1 text-sm text-[var(--muted)]">Manage every character in one clean workspace.</p>
        </div>
        <button @click="goToCreate" class="btn rounded-full  bg-[var(--accent)] text-white">Create character</button>
      </header>

      <div v-if="loading" class="flex justify-center py-12 text-[var(--muted)]">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <div v-else-if="error" class="alert alert-error">
        <span>{{ error }}</span>
      </div>

      <div v-else-if="characters.length === 0" class="rounded-2xl bg-[var(--surface)] p-10 text-center">
        <p class="text-[var(--muted)]">You have not created any characters yet.</p>
        <button @click="goToCreate" class="btn mt-4 rounded-full  bg-[var(--accent)] text-white">Create your first character</button>
      </div>

      <div v-else class="space-y-3">
        <article
          v-for="character in characters"
          :key="character.id"
          class="group cursor-pointer rounded-2xl bg-[var(--surface)] p-3 transition-all hover:translate-x-0.5 "
          @click="goToUpdate(character.id)"
        >
          <div class="flex items-center gap-4">
            <div class="avatar">
              <div class="h-16 w-16 rounded-xl">
                <img :src="character.photo" :alt="character.name" class="object-cover" />
              </div>
            </div>

            <div class="min-w-0 flex-1">
              <h2 class="truncate text-base font-semibold text-[var(--text)]">{{ character.name }}</h2>
              <p class="line-clamp-2 mt-1 text-sm text-[var(--muted)]">{{ character.profile }}</p>
              <p class="mt-1 text-xs text-[var(--muted)]">
                Updated {{ new Date(character.update_time).toLocaleDateString() }}
              </p>
            </div>

            <button class="btn rounded-full bg-[var(--surface-strong)] px-4 text-xs text-[var(--text)]">Edit</button>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>


