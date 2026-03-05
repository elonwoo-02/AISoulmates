<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useUserStore } from "@/stores/user.js";
import HeartIcon from "@/components/character/icons/HeartIcon.vue";
import api from "@/js/http/api.js";
import { useRouter } from "vue-router";

const props = defineProps(['character']);
const emit = defineEmits(['like', 'dislike', 'next']);

const user = useUserStore();
const router = useRouter();
const cardRef = ref(null);
const isDragging = ref(false);
const startX = ref(0);
const currentX = ref(0);
const rotation = ref(0);
const opacity = ref(1);
const isAnimating = ref(false);
const isProcessing = ref(false);

const likeCount = computed(() => props.character?.like_count ?? props.character?.likes ?? 0);

const transform = computed(() => {
  return `translateX(${currentX.value}px) rotate(${rotation.value}deg)`;
});

const swipeThreshold = 100; // pixels
const rotationMultiplier = 0.1;

function handleTouchStart(e) {
  if (isAnimating.value || isProcessing.value) return;
  
  isDragging.value = true;
  startX.value = e.touches[0].clientX - currentX.value;
  opacity.value = 1;
}

function handleTouchMove(e) {
  if (!isDragging.value || isAnimating.value || isProcessing.value) return;
  
  e.preventDefault();
  const clientX = e.touches[0].clientX;
  currentX.value = clientX - startX.value;
  rotation.value = currentX.value * rotationMultiplier;
  
  // Fade out based on distance
  const fadeThreshold = swipeThreshold * 2;
  if (Math.abs(currentX.value) > fadeThreshold) {
    opacity.value = Math.max(0, 1 - (Math.abs(currentX.value) - fadeThreshold) / fadeThreshold);
  }
}

function handleTouchEnd() {
  if (!isDragging.value || isAnimating.value || isProcessing.value) return;
  
  isDragging.value = false;
  
  if (Math.abs(currentX.value) > swipeThreshold) {
    // Swipe detected
    performSwipe();
  } else {
    // Snap back to center
    resetCard();
  }
}

function handleMouseDown(e) {
  if (isAnimating.value || isProcessing.value) return;
  
  isDragging.value = true;
  startX.value = e.clientX - currentX.value;
  opacity.value = 1;
  
  // Add mouse move and up listeners
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
}

function handleMouseMove(e) {
  if (!isDragging.value || isAnimating.value || isProcessing.value) return;
  
  const clientX = e.clientX;
  currentX.value = clientX - startX.value;
  rotation.value = currentX.value * rotationMultiplier;
  
  // Fade out based on distance
  const fadeThreshold = swipeThreshold * 2;
  if (Math.abs(currentX.value) > fadeThreshold) {
    opacity.value = Math.max(0, 1 - (Math.abs(currentX.value) - fadeThreshold) / fadeThreshold);
  }
}

function handleMouseUp() {
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
  
  if (!isDragging.value || isAnimating.value || isProcessing.value) return;
  
  isDragging.value = false;
  
  if (Math.abs(currentX.value) > swipeThreshold) {
    // Swipe detected
    performSwipe();
  } else {
    // Snap back to center
    resetCard();
  }
}

async function performSwipe() {
  isAnimating.value = true;
  const direction = currentX.value > 0 ? 'right' : 'left';
  
  // Animate card off screen
  currentX.value = direction === 'right' ? window.innerWidth : -window.innerWidth;
  rotation.value = direction === 'right' ? 30 : -30;
  opacity.value = 0;
  
  setTimeout(async () => {
    if (direction === 'right') {
      // Right swipe = dislike
      await handleDislike();
    } else {
      // Left swipe = like - add to friends
      await handleLike();
    }
    resetCard();
    emit('next');
  }, 300);
}

function resetCard() {
  currentX.value = 0;
  rotation.value = 0;
  opacity.value = 1;
  isAnimating.value = false;
  isDragging.value = false;
}

async function handleLike() {
  if (!user.isLogin()) {
    // Redirect to login if not logged in
    await router.push({
      name: 'user-account-login-index'
    });
    return;
  }

  isProcessing.value = true;
  
  try {
    // Add to friends list
    const res = await api.post('/api/friend/get_or_create/', {
      character_id: props.character.id
    });
    
    if (res.data.result === 'success') {
      emit('like', props.character.id);
    }
  } catch (err) {
    console.error('Error adding friend:', err);
  } finally {
    isProcessing.value = false;
  }
}

async function handleDislike() {
  emit('dislike', props.character.id);
}

async function openChat() {
  if (!user.isLogin()) {
    await router.push({
      name: 'user-account-login-index'
    });
    return;
  }
  
  try {
    const res = await api.post('/api/friend/get_or_create/', {
      character_id: props.character.id
    });
    const data = res.data;
    if (data.result === 'success') {
      // Navigate to chat
      router.push({ name: 'chat-index', params: { friend_id: data.friend.id } });
    }
  } catch (err) {
    console.error("Error opening chat:", err);
  }
}

onMounted(() => {
  const card = cardRef.value;
  if (card) {
    card.addEventListener('touchstart', handleTouchStart, { passive: false });
    card.addEventListener('touchmove', handleTouchMove, { passive: false });
    card.addEventListener('touchend', handleTouchEnd);
    card.addEventListener('mousedown', handleMouseDown);
  }
});

onBeforeUnmount(() => {
  const card = cardRef.value;
  if (card) {
    card.removeEventListener('touchstart', handleTouchStart);
    card.removeEventListener('touchmove', handleTouchMove);
    card.removeEventListener('touchend', handleTouchEnd);
    card.removeEventListener('mousedown', handleMouseDown);
  }
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
});
</script>

<template>
  <!-- Full Screen Container -->
  <div class="fixed inset-0 z-50 bg-black">
    <!-- Card - Full Screen -->
    <div
      ref="cardRef"
      class="w-full h-full cursor-grab active:cursor-grabbing"
      :style="{
        transform: transform,
        opacity: opacity,
        transition: isDragging ? 'none' : 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)'
      }"
      @click="openChat"
    >
      <article class="relative w-full h-full">
        <!-- Background Image - Full Screen -->
        <img
          :src="character.background_image"
          class="w-full h-full object-cover"
          alt="character background"
          loading="lazy"
          decoding="async"
        />

        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>

        <!-- LIKE/NOPE Indicators -->
        <div v-if="Math.abs(currentX) > 30" class="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div v-if="currentX < -30" class="bg-green-500 text-white px-8 py-4 rounded-full text-2xl font-bold transform rotate-12 flex items-center gap-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            LIKE
          </div>
          <div v-if="currentX > 30" class="bg-red-500 text-white px-8 py-4 rounded-full text-2xl font-bold transform -rotate-12 flex items-center gap-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
            NOPE
          </div>
        </div>

        <!-- Character Info - Bottom -->
        <div class="absolute bottom-0 left-0 right-0 p-5 pb-24">
          <!-- Avatar + Name Row -->
          <div class="flex items-center gap-3">
            <!-- Character Avatar -->
            <div class="w-14 h-14 rounded-full overflow-hidden ring-3 ring-white/60 shadow-lg flex-shrink-0">
              <img
                v-if="character.photo"
                :src="character.photo"
                alt="character avatar"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center">
                <span class="text-xl font-bold text-white">{{ character.name?.charAt(0) }}</span>
              </div>
            </div>

            <!-- Name -->
            <h3 class="text-3xl font-bold text-white leading-tight">{{ character.name }}</h3>
          </div>

          <!-- Profile -->
          <p class="text-white/80 text-base mt-2 line-clamp-2">bio: {{ character.profile }}</p>

          <!-- Bottom Row: Author -->
          <div class="flex items-center justify-between mt-4">
            <!-- Author Info -->
            <div class="flex items-center gap-2">
              <div class="w-6 h-6 rounded-full overflow-hidden">
                <img :src="character.author.photo" alt="author" class="w-full h-full object-cover" />
              </div>
              <span class="text-white/60 text-sm">{{ character.author.username }}</span>
            </div>

            <!-- Like Count -->
            <div class="flex items-center gap-1 text-sm font-semibold text-white/80">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-pink-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
              </svg>
              <span>{{ likeCount }}</span>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- Processing Overlay -->
    <div v-if="isProcessing" class="absolute inset-0 bg-black/50 flex items-center justify-center z-20">
      <span class="loading loading-spinner loading-lg text-white"></span>
    </div>
  </div>
</template>

<style scoped>

</style>
