<script setup>
import {ref, onMounted, useTemplateRef, nextTick, onBeforeUnmount} from 'vue'
import {useRoute} from 'vue-router'
import api from '@/js/http/api.js'
import UserInfoField from "@/views/user/space/components/UserInfoField.vue";

const userProfile = ref(null)
const characters = ref([])
const loading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()
const error = ref(null)

console.log('Route params:', route.params)
console.log('User ID from route:', route.params.user_id)


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
    const res = await api.get('/api/create/character/get_list/', {
      params: {
        items_count: characters.value.length,
        user_id: route.params.user_id
      }
    })
    const data = res.data
    console.log('API Response:', data)
    if (data.result === 'success') {
      userProfile.value = data.user_profile
      console.log('User profile set:', userProfile.value)
      newCharacters = data.characters
    } else {
      console.log('API returned non-success result:', data.result)
    }
  } catch (err) {
    error.value = 'Failed to load more characters'
  } finally {
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

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <div class="flex flex-col mb-12">
    <UserInfoField :userProfile="userProfile"/>
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">

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
