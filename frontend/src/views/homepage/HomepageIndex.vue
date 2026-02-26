<script setup>
import Character from "@/components/character/Character.vue";
import { nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch } from "vue";
import api from "@/js/http/api.js";
import { useRoute } from "vue-router";

const characters = ref([])
const loading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const error = ref(null)
const route = useRoute()

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
    const res = await api.get('/api/homepage/index/', {
      params: {
        items_count: characters.value.length,
        search_query: route.query.q || '',
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newCharacters = data.characters
    }
  } catch (err) {
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
    { root: null, rootMargin: '2px', threshold: 0 }
  )
  if (sentinelRef.value) {
    observer.observe(sentinelRef.value)
  }
})

function reset() {
  characters.value = []
  error.value = null
  loading.value = false
  hasCharacters.value = true
  loadMore()
}

watch(() => route.query.q, () => {
  reset()
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <main class="page-shell pb-12">
    <section class="mt-7">
      <div class="card-grid">
        <Character
          v-for="character in characters"
          :key="character.id"
          :character="character"
          :canEdit="false"
        />
      </div>

      <div ref="sentinel-ref" class="h-2 mt-8 invisible"></div>
      <div v-if="loading" class="mt-4 flex justify-center text-[var(--muted)]">
        <span class="loading loading-spinner loading-lg"></span>
      </div>
      <div v-else-if="error" class="alert alert-error mt-4">
        <span>{{ error }}</span>
      </div>
    </section>
  </main>
</template>

<style scoped>
</style>
