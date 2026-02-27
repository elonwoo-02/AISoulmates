<script setup>
defineProps(['userProfile'])
</script>

<template>
  <section class="w-full">
    <div class="relative bg-white rounded-2xl shadow-sm border border-gray-100">
      <div class="h-32 bg-gradient-to-r from-pink-100 via-red-50 to-orange-100"></div>

      <div class="px-4 pb-4">
        <div class="flex flex-col items-center -mt-12">
        <template v-if="userProfile">
          <div class="avatar">
            <div class="w-24 h-24 rounded-full border-4 border-white shadow-md">
              <img :src="userProfile.photo" alt="user avatar" class="object-cover" />
            </div>
          </div>

          <div class="mt-3 text-center">
            <h1 class="text-xl font-semibold text-gray-900">{{ userProfile.username }}</h1>
            <p class="text-sm text-gray-500 mt-1">@{{ userProfile.user_id }}</p>
            <p class="text-sm text-gray-600 mt-2 max-w-xs line-clamp-2">{{ userProfile.profile }}</p>
          </div>

          <div class="flex gap-3 mt-4">
            <button class="px-6 py-2 bg-red-500 text-white text-sm rounded-full hover:bg-red-600 transition-colors">
              关注
            </button>
            <button class="px-6 py-2 border border-gray-300 text-gray-700 text-sm rounded-full hover:bg-gray-50 transition-colors">
              私信
            </button>
          </div>
        </template>

        <template v-else>
          <div class="w-full h-full bg-gray-200 animate-pulse"></div>
          <div class="mt-3 text-center space-y-2">
            <div class="h-6 w-32 bg-gray-200 animate-pulse rounded mx-auto"></div>
            <div class="h-4 w-24 bg-gray-200 animate-pulse rounded mx-auto"></div>
            <div class="h-4 w-48 bg-gray-200 animate-pulse rounded mx-auto"></div>
          </div>
        </template>
      </div>
    </div>

                                        </div>
    </div>
  </section>
</template>

<style scoped>
.line-clamp-1,
.line-clamp-3 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-1 {
  -webkit-line-clamp: 1;
}

.line-clamp-3 {
  -webkit-line-clamp: 3;
}
</style>