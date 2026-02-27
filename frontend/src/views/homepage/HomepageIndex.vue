<script setup>
import Character from "@/components/character/Character.vue";
import HomepageSwipeCard from "@/components/character/HomepageSwipeCard.vue";
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch, computed} from "vue";
import api from "@/js/http/api.js";
import {useRoute} from "vue-router";
import { useUserStore } from "@/stores/user.js";

const characters = ref([])
const loading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const error = ref(null)
const route = useRoute()
const user = useUserStore()
const currentCardIndex = ref(0)

// Responsive design - use swipe cards on mobile when logged in, masonry otherwise
const shouldUseSwipeCards = computed(() => {
  if (typeof window === 'undefined') return false;
  return window.innerWidth < 768 && user.isLogin(); // md breakpoint + logged in
})

// Get current card for swipe mode
const currentCard = computed(() => {
  return characters.value[currentCardIndex.value];
})

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
  if (sentinelRef.value) {
    observer.observe(sentinelRef.value)
  }
})

function reset() {
  characters.value = []
  error.value = null
  loading.value = false
  hasCharacters.value = true
  currentCardIndex.value = 0
  loadMore()
}

function handleLike(characterId) {
  console.log('Added to friends:', characterId)
  nextCard()
}

function handleDislike(characterId) {
  console.log('Disliked character:', characterId)
  nextCard()
}

function nextCard() {
  if (currentCardIndex.value < characters.value.length - 1) {
    currentCardIndex.value++
  } else {
    // Load more cards if we're at the end
    loadMore()
  }
}

// Handle window resize
let resizeListener = null;
onMounted(() => {
  // Add resize listener to update shouldUseSwipeCards computed
  resizeListener = () => {
    // Force reactivity update
    const dummy = shouldUseSwipeCards.value;
  };
  window.addEventListener('resize', resizeListener);
})

watch(() => route.query.q, newQ => {
  reset()
})

onBeforeUnmount(() => {
  observer?.disconnect()
  if (resizeListener) {
    window.removeEventListener('resize', resizeListener);
  }
})
</script>

<template>
  <div class="flex flex-col items-center">
    <!-- Mobile Swipe Card View (only when logged in) -->
    <div v-if="shouldUseSwipeCards && currentCard" class="fixed inset-0 w-full h-full pt-0 z-30">
      <HomepageSwipeCard
        :character="currentCard"
        @like="handleLike"
        @dislike="handleDislike"
        @next="nextCard"
      />
      
      <!-- Card counter -->
      <div class="absolute top-4 left-0 right-0 text-center z-40">
        <span class="bg-black/50 text-white px-3 py-1 rounded-full text-sm">
          {{ currentCardIndex + 1 }} / {{ characters.length }}
        </span>
      </div>
    </div>

    <!-- Desktop Masonry View or logged out view -->
    <div v-else class="w-full gap-2">
      <div class="grid grid-cols-2 gap-1 mx-1 my-1 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-5">
      <Character
        v-for="character in characters"
        :key="character.id"
        :character="character"
        :canEdit="false"
      />
      </div>
    </div>

    <!-- Sentinel for infinite scrolling (desktop and logged out only) -->
    <div v-if="!shouldUseSwipeCards" ref="sentinel-ref" class="h-2 mt-8 invisible"></div>

    <!-- Loading state -->
    <div v-if="loading" class="text-gray-500 mt-4 flex justify-center">
      <span class="loading loading-spinner loading-lg"></span>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="alert alert-error">
      <span>{{ error }}</span>
    </div>

    <!-- No more cards (mobile swipe mode) -->
    <div v-if="shouldUseSwipeCards && characters.length > 0 && currentCardIndex >= characters.length && !loading" class="flex flex-col items-center justify-center h-64">
      <p class="text-gray-500 text-lg mb-4">No more cards!</p>
      <button @click="loadMore" class="btn btn-primary">
        Load More
      </button>
    </div>

    <!-- Empty state -->
    <div v-if="characters.length === 0 && !loading" class="flex flex-col items-center justify-center h-64">
      <p class="text-gray-500 text-lg">
        {{ user.isLogin() ? 'No characters found' : 'Please login to swipe cards' }}
      </p>
      <div v-if="!user.isLogin()" class="mt-4">
        <router-link :to="{ name: 'user-account-login-index' }" class="btn btn-primary">
          Login
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
