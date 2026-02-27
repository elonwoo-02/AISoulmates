<script setup>
import { ref, onMounted, nextTick, useTemplateRef, watch } from 'vue'

const props = defineProps(['userProfile'])
const emit = defineEmits(['editProfile'])

const backgroundRef = useTemplateRef('background-ref')
const profileHeight = ref('16rem') // 增加默认高度到 16rem

function calculateBackgroundHeight() {
  nextTick(() => {
    if (backgroundRef.value && props.userProfile?.profile) {
      const profileElement = backgroundRef.value.querySelector('[data-profile-text]')
      if (profileElement) {
        const profileTextHeight = profileElement.scrollHeight
        const baseHeight = 256 // 增加基础高度到 16rem (256px)
        const additionalHeight = Math.max(0, profileTextHeight - 20) // 减少扣除的间距，让更多空间给内容
        const totalHeight = baseHeight + additionalHeight
        
        // 转换为 rem (假设 1rem = 16px)
        const heightInRem = totalHeight / 16
        profileHeight.value = `${heightInRem}rem`
      }
    } else if (!props.userProfile?.profile) {
      // 如果没有简介，使用默认高度
      profileHeight.value = '16rem' // 默认高度增加到 16rem
    }
  })
}

function editProfile() {
  emit('editProfile')
}

watch(() => props.userProfile?.profile, () => {
  calculateBackgroundHeight()
})

onMounted(() => {
  calculateBackgroundHeight()
})
</script>

<template>
  <section class="w-full">
    <div class="relative overflow-hidden">
      <!-- Background image with gradient overlay -->
      <div ref="background-ref" class="relative transition-all duration-300" :style="`height: ${profileHeight}; ${props.userProfile && props.userProfile.background_image ? `background-image: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.6)), url(${props.userProfile.background_image}); background-size: cover; background-position: center;` : 'background: linear-gradient(135deg, rgb(239 68 68 / 0.9), rgb(251 146 60 / 0.8), rgb(252 211 77 / 0.8));'}`">
        <!-- Edit button in top-right corner -->
        <div class="absolute top-4 right-4 z-10">
          <button @click="editProfile" class="btn btn-ghost btn-sm rounded-full bg-white/10 backdrop-blur-sm text-white border-white/20 hover:bg-white/20">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </button>
        </div>
        <!-- User info overlay on background -->
        <div class="absolute inset-0 flex flex-col justify-end p-6 md:p-8">
          <template v-if="userProfile">
            <div class="relative">
              <!-- User info row -->
              <div class="flex items-start gap-4 md:gap-6">
                <!-- Avatar -->
                <div class="avatar">
                  <div class="h-12 w-12 rounded-lg ring-4 ring-base-100/90 md:h-16 md:w-16">
                    <img :src="userProfile.photo" alt="user avatar" class="object-cover" />
                  </div>
                </div>

                <div class="min-w-0 flex-1 text-white pr-20">
                  <h1 class="line-clamp-1 break-all text-lg font-bold tracking-tight md:text-4xl drop-shadow-lg">{{ userProfile.username }}</h1>
                  <p class="mt-1 text-xs text-white/90 drop-shadow">@{{ userProfile.user_id }}</p>
                </div>
              </div>
              
              <!-- Profile text with button -->
              <div class="relative mt-2">
                <p v-if="userProfile.profile" data-profile-text class="pr-20 text-sm text-white/80 drop-shadow">{{ userProfile.profile }}</p>
                
                <!-- Action buttons positioned absolutely -->
                <div class="absolute bottom-0 right-0 flex gap-2">
                  <button class="btn btn-xs rounded-full bg-white/20 backdrop-blur-sm text-white border-white/30 hover:bg-white/30 md:btn-sm">Subscribed</button>
                </div>
              </div>
            </div>
          </template>

          <!-- Loading state -->
          <template v-else>
            <div class="flex items-end gap-4 md:gap-6">
              <div class="h-12 w-12 animate-pulse rounded-lg bg-white/20 md:h-16 md:w-16"></div>
              <div class="flex-1 space-y-3">
                <div class="h-7 w-52 animate-pulse rounded-md bg-white/20"></div>
                <div class="h-4 w-32 animate-pulse rounded-md bg-white/20"></div>
                <div class="h-4 w-80 animate-pulse rounded-md bg-white/20"></div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>

</style>
