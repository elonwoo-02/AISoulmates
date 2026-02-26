<script setup>
import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import SettingIcon from "@/components/navbar/icons/SettingIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import NewIcon from "@/components/navbar/icons/NewIcon.vue";

import { ref, watch } from 'vue'
import { useUserStore } from "@/stores/user.js";
import UserMenu from "@/components/navbar/UserMenu.vue";
import { useRoute, useRouter } from "vue-router";

const user = useUserStore()
const searchQuery = ref('')
const router = useRouter()
const route = useRoute()

watch(
  () => route.query.q,
  newQ => {
    searchQuery.value = newQ || ''
  },
  { immediate: true }
)

function handleSearch() {
  router.push({ name: 'homepage-index', query: { q: searchQuery.value.trim() } })
}
</script>

<template>
  <div class="drawer lg:drawer-open min-h-screen">
    <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />

    <div class="drawer-content overflow-visible pb-8">
      <nav class="layer-nav sticky top-0 mx-3 mt-3 rounded-2xl bg-[var(--surface)] px-3 py-2 shadow-[var(--shadow)] sm:mx-4 sm:px-4">
        <div class="flex flex-wrap items-center gap-2">
          <label for="my-drawer-4" aria-label="Toggle sidebar" class="inline-flex h-8 w-8 cursor-pointer items-center justify-center text-[var(--muted)] lg:hidden">
            <MenuIcon />
          </label>

          <RouterLink :to="{ name: 'homepage-index' }" class="brand-font text-xl font-semibold tracking-tight text-[var(--text)]">AISoulmates</RouterLink>

          <div class="order-3 w-full sm:order-none sm:ml-4 sm:w-auto sm:flex-1">
            <form @submit.prevent="handleSearch" class="relative max-w-2xl">
              <input
                v-model="searchQuery"
                class="soft-input rounded-full pr-12"
                placeholder="Search companions"
                aria-label="Search companions"
              />
              <button type="submit" aria-label="Submit search" class="absolute right-1.5 top-1.5 flex h-8 w-8 items-center justify-center rounded-full text-[var(--muted)] transition-colors hover:bg-[var(--accent-soft)] hover:text-[var(--accent)]">
                <SearchIcon />
              </button>
            </form>
          </div>

          <div class="ml-auto flex items-center gap-1">
            <RouterLink v-if="user.isLogin()" :to="{ name: 'create-index' }" class="inline-flex h-9 w-9 items-center justify-center text-[var(--muted)] hover:text-[var(--accent)]" aria-label="Create character">
              <CreateIcon />
            </RouterLink>

            <RouterLink v-if="user.isLogin()" :to="{ name: 'new-index' }" class="inline-flex h-9 w-9 items-center justify-center text-[var(--muted)] hover:text-[var(--accent)]" aria-label="Updates">
              <NewIcon />
            </RouterLink>

            <RouterLink
              v-if="user.hasPulledUserInfo && !user.isLogin()"
              :to="{ name: 'user-account-login-index' }"
              class="btn rounded-full bg-[var(--surface-strong)] px-5 text-[var(--text)] hover:bg-[var(--bg-elevated)]"
            >
              Sign in
            </RouterLink>

            <UserMenu v-else-if="user.isLogin()" />
          </div>
        </div>
      </nav>

      <slot></slot>
    </div>

    <div class="drawer-side layer-sidebar isolate overflow-visible">
      <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay layer-overlay !bg-transparent"></label>

      <aside class="mx-3 my-3 flex min-h-[calc(100%-1.5rem)] w-16 flex-col overflow-visible rounded-2xl bg-[var(--surface)] px-2 py-3 shadow-[var(--shadow)] transition-all is-drawer-open:w-56">
        <ul class="menu mt-2 w-full gap-1 p-0 text-[var(--text)]">
          <li>
            <RouterLink :to="{ name: 'homepage-index' }" active-class="active-nav" class="group relative z-[70] layer-popover rounded-xl px-3 py-3 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Home">
              <HomepageIcon />
              <span class="is-drawer-close:hidden ml-2">Home</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{ name: 'friend-index' }" active-class="active-nav" class="group relative z-[70] layer-popover rounded-xl px-3 py-3 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Friends">
              <FriendIcon />
              <span class="is-drawer-close:hidden ml-2">Friends</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{ name: 'create-index' }" active-class="active-nav" class="group relative z-[70] layer-popover rounded-xl px-3 py-3 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Create">
              <CreateIcon />
              <span class="is-drawer-close:hidden ml-2">Create</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{ name: 'setting-index' }" active-class="active-nav" class="group relative z-[70] layer-popover rounded-xl px-3 py-3 is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Settings">
              <SettingIcon />
              <span class="is-drawer-close:hidden ml-2">Settings</span>
            </RouterLink>
          </li>
        </ul>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.active-nav {
  background: var(--accent-soft);
  color: var(--accent);
}

.menu :global(a:hover) {
  background: color-mix(in srgb, var(--surface-strong) 70%, transparent);
}

:deep([class*="tooltip"])::before,
:deep([class*="tooltip"])::after {
  z-index: 70 !important;
}
</style>
