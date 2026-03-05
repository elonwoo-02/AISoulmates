<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user.js";
import BottomHomepageIcon from "@/components/navbar/icons/BottomHomepageIcon.vue";
import BottomFriendIcon from "@/components/navbar/icons/BottomFriendIcon.vue";
import MessagesIcon from "@/components/navbar/icons/MessagesIcon.vue";
import UserIcon from "@/components/navbar/icons/UserIcon.vue";
import PlusCircleIcon from "@/components/navbar/icons/PlusCircleIcon.vue";

const route = useRoute();
const router = useRouter();
const user = useUserStore();

const activeName = computed(() => route.name);

function goHome() {
  router.push({ name: "homepage-index" });
}

function goMarket() {
  router.push({ name: "friend-index" });
}

function goCreate() {
  router.push({ name: "create-index" });
}

function goMessages() {
  router.push({ name: "new-index" });
}

function goMe() {
  if (!user.isLogin()) {
    router.push({ name: "user-account-login-index" });
    return;
  }
  if (user.id && user.id !== 0) {
    router.push({ name: "user-space-index", params: { user_id: user.id } });
  }
}
</script>

<template>
  <nav
    class="fixed bottom-0 left-0 right-0 z-40 border-t border-black/5 bg-white/90 backdrop-blur"
    style="padding-bottom: env(safe-area-inset-bottom);"
  >
    <div class="mx-auto flex w-full max-w-300 items-center justify-between px-6 py-1">
      <button
        class="flex flex-col items-center gap-0.5 text-xs font-medium text-[--text-tertiary] transition-colors hover:text-[--text-primary] border-b-2 border-transparent"
        :class="{ 'text-[--accent-red] border-red-500': activeName === 'homepage-index' }"
        @click="goHome"
        aria-label="Home"
      >
        <BottomHomepageIcon class="h-6 w-6" :class="{ 'text-red-500': activeName === 'homepage-index' }" />
      </button>

      <button
        class="flex flex-col items-center gap-0.5 text-xs font-medium text-[--text-tertiary] transition-colors hover:text-[--text-primary] border-b-2 border-transparent"
        :class="{ 'text-[--accent-red] border-red-500': activeName === 'friend-index' }"
        @click="goMarket"
        aria-label="Friends"
      >
        <BottomFriendIcon class="h-6 w-6" :class="{ 'text-red-500': activeName === 'friend-index' }" />
      </button>

      <button
        class="relative flex h-11 w-11 items-center justify-center rounded-full bg-red-500 z-50"
        @click="goCreate"
        aria-label="Create"
      >
        <PlusCircleIcon class="h-7 w-7" />
      </button>

      <button
        class="flex flex-col items-center gap-0.5 text-xs font-medium text-[--text-tertiary] transition-colors hover:text-[--text-primary] border-b-2 border-transparent"
        :class="{ 'text-[--accent-red] border-red-500': activeName === 'new-index' }"
        @click="goMessages"
        aria-label="New"
      >
        <MessagesIcon class="h-6 w-6" :class="{ 'text-red-500': activeName === 'new-index' }" />
      </button>

      <button
        class="flex flex-col items-center gap-0.5 text-xs font-medium text-[--text-tertiary] transition-colors hover:text-[--text-primary] border-b-2 border-transparent"
        :class="{ 'text-[--accent-red] border-red-500': activeName === 'user-space-index' }"
        @click="goMe"
        aria-label="Me"
      >
        <UserIcon class="h-6 w-6" :class="{ 'text-red-500': activeName === 'user-space-index' }" />
      </button>
    </div>
  </nav>
</template>

<style scoped>
</style>
