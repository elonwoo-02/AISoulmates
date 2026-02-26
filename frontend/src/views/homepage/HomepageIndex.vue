<script setup>
import Character from "@/components/character/Character.vue";
import UserInfoField from "@/views/user/space/components/UserInfoField.vue";
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch} from "vue";
import api from "@/js/http/api.js";
import {useRoute} from "vue-router";

const characters = ref([])
const loading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const error = ref(null)
const userProfile = ref(null)
const route = useRoute()

function checkSentinelVisible() {  // 判断哨兵是否能被看到
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
    } else {
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
onMounted( async () => {
  await loadMore()

  observer = new IntersectionObserver(
      entries => {
          entries.forEach(
              entry => {
                if (entry.isIntersecting) {
                  loadMore()
                }
              })
        },
      {root: null, rootMargin: '2px', threshold: 0}
  )
  observer.observe(sentinelRef.value)
})

function reset() {
  characters.value = []
  loading.value = false
  hasCharacters.value = true
  loadMore()
}

watch(() => route.query.q, newQ => {
  reset()
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>

  <div class="flex flex-col items-center mb-12 ">
    <UserInfoField :userProfile="userProfile"/>
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
      <Character
        v-for="character in characters"
        :key="character.id"
        :character="character"
        :canEdit="false"
      />
    </div>
    <!-- Sentinel element for infinite scrolling -->
    <div ref="sentinel-ref" class="h-2 mt-8 hidden text-base-100"></div>
    <div v-if="loading" class="text-gray-500 mt-4 flex justify-center">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
    <div v-else-if="error" class="alert alert-error">
      <span>{{ error }}</span>
    </div>

  </div>
</template>

<style scoped>

</style>