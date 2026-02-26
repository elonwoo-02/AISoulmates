<script setup>
defineProps(['userProfile'])
</script>

<template>
  <section class="w-full">
    <div class="relative overflow-hidden rounded-3xl border border-base-300/80 bg-base-200/70">
      <div class="h-28 bg-gradient-to-r from-red-500/80 via-orange-400/70 to-amber-300/70 md:h-36"></div>

      <div class="-mt-10 flex flex-col gap-4 px-4 pb-5 md:-mt-12 md:flex-row md:items-end md:gap-6 md:px-6">
        <template v-if="userProfile">
          <div class="avatar">
            <div class="h-24 w-24 rounded-full ring-4 ring-base-100 md:h-28 md:w-28">
              <img :src="userProfile.photo" alt="user avatar" class="object-cover" />
            </div>
          </div>

          <div class="min-w-0 flex-1">
            <h1 class="line-clamp-1 break-all text-2xl font-bold tracking-tight md:text-3xl">{{ userProfile.username }}</h1>
            <p class="mt-1 text-sm text-base-content/70">@{{ userProfile.user_id }}</p>
            <p class="line-clamp-3 mt-3 break-all text-sm text-base-content/80 md:max-w-3xl">{{ userProfile.profile }}</p>
          </div>

          <div class="flex gap-2 md:self-center">
            <button class="btn btn-sm rounded-full">Subscribed</button>
            <button class="btn btn-sm rounded-full btn-ghost">Share</button>
          </div>
        </template>

        <template v-else>
          <div class="h-24 w-24 animate-pulse rounded-full bg-base-300 md:h-28 md:w-28"></div>
          <div class="flex-1 space-y-3">
            <div class="h-7 w-52 animate-pulse rounded-md bg-base-300"></div>
            <div class="h-4 w-32 animate-pulse rounded-md bg-base-300"></div>
            <div class="h-4 w-80 animate-pulse rounded-md bg-base-300"></div>
          </div>
        </template>
      </div>
    </div>

    <div class="mt-4 border-b border-base-300">
      <div class="flex gap-6 px-2 text-sm font-medium text-base-content/70">
        <span class="border-b-2 border-base-content px-1 pb-2 text-base-content">Home</span>
        <span class="px-1 pb-2">Characters</span>
        <span class="px-1 pb-2">About</span>
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