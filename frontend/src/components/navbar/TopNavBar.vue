<script setup>
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user.js";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import NewIcon from "@/components/navbar/icons/NewIcon.vue";
import UserMenu from "@/components/navbar/UserMenu.vue";

const user = useUserStore();
const searchQuery = ref("");
const router = useRouter();
const route = useRoute();

watch(
  () => route.query.q,
  (newQ) => {
    searchQuery.value = newQ || "";
  },
  { immediate: true }
);

const activeTab = computed(() => (route.name === "friend-index" ? "friend" : "explore"));

function handleSearch() {
  router.push({ name: "homepage-index", query: { q: searchQuery.value.trim() } });
}
</script>

<template>
  <nav class="sticky top-0 z-30 border-b border-black/5 bg-white/80 backdrop-blur">
    <div class="mx-auto flex w-full max-w-[1200px] items-center gap-4 px-4 py-3 sm:px-6 lg:px-8">
      <div class="flex items-center gap-5">
        <RouterLink
          :to="{ name: 'friend-index' }"
          class="relative text-[15px] font-semibold tracking-tight text-[var(--text-secondary)] transition-colors hover:text-[var(--text-primary)]"
          :class="{ 'text-[var(--accent-red)]': activeTab === 'friend' }"
        >
          Friend
          <span
            v-if="activeTab === 'friend'"
            class="absolute -bottom-2 left-0 h-[2px] w-full rounded-full bg-[var(--accent-red)]"
          ></span>
        </RouterLink>
        <RouterLink
          :to="{ name: 'homepage-index' }"
          class="relative text-[15px] font-semibold tracking-tight text-[var(--text-secondary)] transition-colors hover:text-[var(--text-primary)]"
          :class="{ 'text-[var(--accent-red)]': activeTab === 'explore' }"
        >
          Explore
          <span
            v-if="activeTab === 'explore'"
            class="absolute -bottom-2 left-0 h-[2px] w-full rounded-full bg-[var(--accent-red)]"
          ></span>
        </RouterLink>
      </div>

      <form @submit.prevent="handleSearch" class="ml-2 flex flex-1 items-center">
        <label class="flex w-full items-center gap-2 rounded-full bg-[var(--surface-muted)] px-4 py-2 text-sm text-[var(--text-secondary)]">
          <SearchIcon class="h-4 w-4 text-[var(--text-tertiary)]" />
          <input
            v-model="searchQuery"
            class="w-full bg-transparent text-[15px] text-[var(--text-primary)] placeholder:text-[var(--text-tertiary)] focus:outline-none"
            placeholder="Search"
            aria-label="Search"
          />
        </label>
      </form>

      <div class="ml-auto flex items-center gap-2">
        <RouterLink
          v-if="user.isLogin()"
          :to="{ name: 'create-index' }"
          class="btn btn-ghost text-lg hover-3d py-1"
          aria-label="Create"
        >
          <CreateIcon />
        </RouterLink>

        <RouterLink
          v-if="user.isLogin()"
          :to="{ name: 'new-index' }"
          class="btn btn-ghost text-lg hover-3d py-1"
          aria-label="New"
        >
          <NewIcon />
        </RouterLink>

        <RouterLink
          v-if="user.hasPulledUserInfo && !user.isLogin()"
          :to="{ name: 'user-account-login-index' }"
          active-class="btn-active"
          class="btn btn-ghost text-sm font-semibold"
        >
          Sign in
        </RouterLink>

        <UserMenu v-else-if="user.isLogin()" />
      </div>
    </div>
  </nav>
</template>

<style scoped>
</style>
