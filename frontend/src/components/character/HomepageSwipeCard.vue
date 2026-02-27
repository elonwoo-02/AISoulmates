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
      console.log('Added to friends:', props.character.name);
    }
  } catch (err) {
    console.error('Error adding friend:', err);
  } finally {
    isProcessing.value = false;
  }
}

async function handleDislike() {
  emit('dislike', props.character.id);
  console.log('Disliked character:', props.character.name);
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
  <div class="relative flex items-center justify-center h-screen max-h-[800px] px-4">
    <!-- Like/Dislike indicators -->
    <div 
      v-if="Math.abs(currentX) > 30"
      class="absolute inset-0 flex items-center justify-center pointer-events-none"
      style="z-index: 10;"
    >
      <div 
        v-if="currentX < -30"
        class="bg-green-500 text-white px-8 py-4 rounded-full text-2xl font-bold transform rotate-12 flex items-center gap-2"
      >
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        LIKE
      </div>
      <div 
        v-if="currentX > 30"
        class="bg-red-500 text-white px-8 py-4 rounded-full text-2xl font-bold transform -rotate-12 flex items-center gap-2"
      >
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
        NOPE
      </div>
    </div>

    <!-- Processing overlay -->
    <div 
      v-if="isProcessing"
      class="absolute inset-0 bg-black/50 flex items-center justify-center z-20 rounded-2xl"
    >
      <span class="loading loading-spinner loading-lg text-white"></span>
    </div>

    <!-- Card -->
    <div
      ref="cardRef"
      class="relative w-full max-w-sm cursor-grab active:cursor-grabbing"
      :style="{
        transform: transform,
        opacity: opacity,
        transition: isDragging ? 'none' : 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)'
      }"
      @click="openChat"
    >
      <article class="overflow-hidden rounded-2xl border border-black/5 bg-white shadow-[0_12px_30px_-20px_rgba(15,23,42,0.35)]">
        <div class="relative aspect-[3/5] overflow-hidden bg-[var(--surface-muted)]">
          <img
            :src="character.background_image"
            class="h-full w-full object-cover"
            alt="character background"
            loading="lazy"
            decoding="async"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent"></div>

          <div class="absolute bottom-0 left-0 right-0 p-4 text-white">
            <h3 class="line-clamp-2 text-lg font-semibold leading-5 tracking-tight">{{ character.name }}</h3>
            <p class="line-clamp-3 mt-2 text-sm text-white/90">{{ character.profile }}</p>
          </div>
        </div>

        <div class="flex items-center justify-between px-4 py-3">
          <div class="flex items-center gap-2 text-xs font-medium text-[var(--text-secondary)]">
            <span class="avatar">
              <span class="h-8 w-8 overflow-hidden rounded-full">
                <img :src="character.author.photo" alt="author avatar" class="h-full w-full object-cover" loading="lazy" decoding="async" />
              </span>
            </span>
            <span class="max-w-[120px] truncate">{{ character.author.username }}</span>
          </div>

          <div class="flex items-center gap-1 text-sm font-semibold text-[var(--accent-yellow)]">
            <HeartIcon />
            <span>{{ likeCount }}</span>
          </div>
        </div>
      </article>
    </div>

    <!-- Action buttons -->
    <div class="absolute bottom-8 left-0 right-0 flex justify-center gap-4 px-4">
      <button 
        @click.stop="handleDislike"
        :disabled="isProcessing"
        class="w-14 h-14 bg-white rounded-full shadow-lg flex items-center justify-center text-red-500 hover:scale-110 transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
      
      <button 
        @click.stop="handleLike"
        :disabled="isProcessing"
        class="w-14 h-14 bg-white rounded-full shadow-lg flex items-center justify-center text-green-500 hover:scale-110 transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2,
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  -webkit-line-clamp: 3;
}

/* Prevent text selection during swipe */
.cursor-grab,
.cursor-grabbing {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}
</style>
