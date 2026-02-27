<script setup>
import { ref, onMounted, useTemplateRef, nextTick, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/js/http/api.js'
import UserInfoField from '@/views/user/space/components/UserInfoField.vue'
import Character from '@/components/character/Character.vue'

const userProfile = ref(null)
const characters = ref([])
const loading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()
const router = useRouter()
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

function handleEditProfile() {
  router.push({ name: 'user-profile-index' })
}

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <div class="mx-auto w-full max-w-screen-2xl">
    <UserInfoField :userProfile="userProfile" @editProfile="handleEditProfile" />

    <section class="bg-white rounded-t-2xl -mt-3 shadow-lg relative z-10 pb-[calc(96px+env(safe-area-inset-bottom))]">
      <!-- Navigation tabs -->
      <!-- todo: -->
      <div class="mb-0 border-b border-gray-200 gap-5">
        <nav class="mx-4 py-2 flex items-center space-x-8">
          <button class="border-b-2 border-red-500 font-medium hover:text-red-500">
            Characters
          </button>
          <button class="border-b-2 border-transparent font-medium text-gray-500 hover:text-red-500">
            Likes
          </button>
        </nav>
      </div>
      <div class="grid grid-cols-2 gap-1 mx-1 my-1 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-5">
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

    <div v-if="loading" class="mt-4 flex justify-center text-gray-500">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else-if="error" class="alert alert-error mt-4">
      <span>{{ error }}</span>
    </div>
  </div>
</template>

<style scoped>
</style>