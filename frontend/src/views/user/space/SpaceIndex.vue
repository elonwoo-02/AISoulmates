<script setup>
import { ref, onMounted, useTemplateRef, nextTick, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/js/http/api.js'
import UserInfoField from '@/views/user/space/components/UserInfoField.vue'
import Character from '@/components/character/Character.vue'

const userProfile = ref(null)
const characters = ref([])
const loading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()
const error = ref(null)

function checkSentinelVisible() {
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore() {
  if (loading.value || !hasCharacters.value) return
  loading.value = true

  let newCharacters = []
  try {
    const res = await api.get('/api/create/character/get_list/', {
      params: {
        items_count: characters.value.length,
        user_id: route.params.user_id,
      },
    })
    const data = res.data
    if (data.result === 'success') {
      userProfile.value = data.user_profile
      newCharacters = data.characters
    }
  } catch {
    error.value = 'Failed to load more characters'
  } finally {
    loading.value = false
    if (newCharacters.length === 0) {
      hasCharacters.value = false
    } else {
      characters.value.push(...newCharacters)
      await nextTick()

      if (checkSentinelVisible()) {
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async () => {
  await loadMore()

  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadMore()
        }
      })
    },
    { root: null, rootMargin: '2px', threshold: 0 },
  )
  observer.observe(sentinelRef.value)
})

function removeCharacter(characterId) {
  characters.value = characters.value.filter(c => c.id !== characterId)
}

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <main class="page-shell pb-12">
    <UserInfoField :userProfile="userProfile" />

    <section class="mt-7">
      <div class="mb-4 flex items-end justify-between">
        <div>
          <h2 class="brand-font text-2xl tracking-tight">Characters</h2>
          <p class="mt-1 text-sm text-[var(--muted)]">{{ characters.length }} loaded</p>
        </div>
      </div>

      <div class="card-grid">
        <Character
          v-for="character in characters"
          :key="character.id"
          :character="character"
          :canEdit="true"
          @remove="removeCharacter"
        />
      </div>
    </section>

    <div ref="sentinel-ref" class="mt-8 hidden h-2 text-base-100"></div>

    <div v-if="loading" class="mt-4 flex justify-center text-[var(--muted)]">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else-if="error" class="alert alert-error mt-4">
      <span>{{ error }}</span>
    </div>
  </main>
</template>

<style scoped>
</style>
