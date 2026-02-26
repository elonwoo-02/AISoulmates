<script setup>
defineProps(['userProfile'])
</script>

<template>
  <section class="w-full">
    <div class="glass-panel overflow-hidden">
      <div class="h-28 bg-linear-to-r from-[var(--surface-strong)] to-[var(--bg-elevated)] md:h-32"></div>

      <div class="-mt-10 flex flex-col gap-4 px-4 pb-5 md:flex-row md:items-end md:gap-5 md:px-6">
        <template v-if="userProfile">
          <div class="avatar">
            <div class="h-20 w-20 rounded-full bg-[var(--surface)] p-0.5 shadow-sm md:h-24 md:w-24">
              <img :src="userProfile.photo" alt="user avatar" class="object-cover" />
            </div>
          </div>

          <div class="min-w-0 flex-1">
            <h1 class="line-clamp-1 break-all text-2xl font-bold tracking-tight text-[var(--text)] md:text-3xl">{{ userProfile.username }}</h1>
            <p class="mt-1 text-sm text-[var(--muted)]">@{{ userProfile.user_id }}</p>
            <p class="line-clamp-3 mt-3 break-all text-sm text-[var(--muted)] md:max-w-3xl">{{ userProfile.profile }}</p>
          </div>
        </template>

        <template v-else>
          <div class="h-24 w-24 animate-pulse rounded-full bg-[var(--bg-elevated)] md:h-28 md:w-28"></div>
          <div class="flex-1 space-y-3">
            <div class="h-7 w-52 animate-pulse rounded-md bg-[var(--bg-elevated)]"></div>
            <div class="h-4 w-32 animate-pulse rounded-md bg-[var(--bg-elevated)]"></div>
            <div class="h-4 w-80 animate-pulse rounded-md bg-[var(--bg-elevated)]"></div>
          </div>
        </template>
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
