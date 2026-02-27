<script setup>
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user.js";
import TopNavBar from "@/components/navbar/TopNavBar.vue";
import BottomTabBar from "@/components/navbar/BottomTabBar.vue";
import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import SettingIcon from "@/components/navbar/icons/SettingIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import CompactIcon from "@/components/navbar/icons/CompactIcon.vue";
import NewIcon from "@/components/navbar/icons/NewIcon.vue";
import UserMenu from "@/components/navbar/UserMenu.vue";

const route = useRoute();
const router = useRouter();
const user = useUserStore();
const searchQuery = ref("");

const showBottomBar = computed(() => {
  const enabledRoutes = new Set([
    "homepage-index",
    "friend-index",
    "new-index",
    "create-index",
    "user-space-index",
  ]);
  return enabledRoutes.has(route.name);
});

const showTopBarOnMobile = computed(() => {
  return route.name === "homepage-index" || route.name === "friend-index";
});

watch(
  () => route.query.q,
  (newQ) => {
    searchQuery.value = newQ || "";
  },
  { immediate: true }
);

function handleSearch() {
  router.push({ name: "homepage-index", query: { q: searchQuery.value.trim() } });
}

</script>

<template>
  <div class="min-h-screen bg-[--app-bg] text-[--text-primary]">
    <!-- Mobile / small screens -->
    <div class="md:hidden">
      <TopNavBar v-if="showTopBarOnMobile"/>
      <main class="mx-auto w-full max-w-300 pb-[calc(96px+env(safe-area-inset-bottom))]">
        <slot></slot>
      </main>
      <BottomTabBar v-if="showBottomBar" />
    </div>

    <!-- Desktop (legacy drawer kept and used) -->
    <div class="hidden md:block">
      <div class="drawer lg:drawer-open">
        <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />

        <div class="drawer-content">
          <nav class="z-70 navbar w-full bg-base-100 shadow-sm">
            <div class="navbar-start">
              <div class="dropdown dropdown-hover">
                <div tabindex="0" role="button" class="px-0 font-bold text-xl">AISoulmates</div>
                <ul tabindex="-1" class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 shadow-sm">
                  <li><a>Item 1</a></li>
                  <li><a>Item 2</a></li>
                </ul>
              </div>
            </div>

            <div class="navbar-center flex justify-center w-full max-w-150">
              <form @submit.prevent="handleSearch" class="join w-4/5 flex justify-center">
                <input v-model="searchQuery" class="input join-item rounded-l-full w-4/5" placeholder="Search" />
                <button class="btn join-item rounded-r-full">
                  <SearchIcon />
                </button>
              </form>
            </div>

            <div class="navbar-end">
              <RouterLink v-if="user.isLogin()" :to="{ name: 'create-index' }" class="btn btn-ghost text-lg hover-3d py-1">
                <CreateIcon />
              </RouterLink>

              <RouterLink v-if="user.isLogin()" :to="{ name: 'new-index' }" class="btn btn-ghost text-lg hover-3d py-1">
                <NewIcon />
              </RouterLink>

              <RouterLink
                v-if="user.hasPulledUserInfo && !user.isLogin()"
                :to="{ name: 'user-account-login-index' }"
                active-class="btn-active"
                class="btn btn-ghost text-lg"
              >
                Sign in
              </RouterLink>

              <UserMenu v-else-if="user.isLogin()" />
            </div>
          </nav>
          <slot></slot>
        </div>

        <div class="drawer-side is-drawer-close:overflow-visible">
          <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>

          <div class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-16 is-drawer-open:w-54">
            <ul class="menu w-full grow">
              <li>
                <label for="my-drawer-4" aria-label="open sidebar" class="flex group">
                  <CompactIcon class="is-drawer-close:ml-0 is-drawer-close:group-hover:hidden" />
                  <MenuIcon class="is-drawer-open:ml-auto is-drawer-close:hidden group-hover:inline-block" />
                </label>
              </li>

              <li class="is-drawer-close:hidden"></li>
              <li>
                <RouterLink
                  :to="{ name: 'homepage-index' }"
                  active-class="menu-focus"
                  class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3"
                  data-tip="Homepage"
                >
                  <homepage-icon />
                  <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Home</span>
                </RouterLink>
              </li>

              <li>
                <RouterLink
                  :to="{ name: 'friend-index' }"
                  active-class="menu-focus"
                  class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3"
                  data-tip="Friend"
                >
                  <friend-icon />
                  <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Friends</span>
                </RouterLink>
              </li>

              <li>
                <RouterLink
                  :to="{ name: 'create-index' }"
                  active-class="menu-focus"
                  class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3"
                  data-tip="Create"
                >
                  <create-icon />
                  <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Create</span>
                </RouterLink>
              </li>

              <li>
                <RouterLink
                  :to="{ name: 'setting-index' }"
                  active-class="menu-focus"
                  class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3"
                  data-tip="Settings"
                >
                  <setting-icon />
                  <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Settings</span>
                </RouterLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
