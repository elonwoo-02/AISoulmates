<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user.js";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import MarketIcon from "@/components/navbar/icons/MarketIcon.vue";
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
  router.push({ name: "404" });
}

function goCreate() {
  router.push({ name: "create-index" });
}

function goMessages() {
  router.push({ name: "404" });
}

function goMe() {
  if (!user.isLogin()) {
    router.push({ name: "user-account-login-index" });
    return;
  }
  router.push({ name: "user-space-index", params: { user_id: user.id } });
}
</script>

<template>
  <nav
    class="fixed bottom-0 left-0 right-0 z-40 border-t border-black/5 bg-white/90 backdrop-blur"
    style="padding-bottom: env(safe-area-inset-bottom);"
  >
    <div class="mx-auto flex w-full max-w-[1200px] items-center justify-between px-6 py-3">
      <button
        class="flex flex-col items-center gap-1 text-xs font-medium text-[var(--text-tertiary)] transition-colors hover:text-[var(--text-primary)]"
        :class="{ 'text-[var(--accent-red)]': activeName === 'homepage-index' }"
        @click="goHome"
        aria-label="Home"
      >
        <HomepageIcon class="h-6 w-6" />
        Home
      </button>

      <button
        class="flex flex-col items-center gap-1 text-xs font-medium text-[var(--text-tertiary)] transition-colors hover:text-[var(--text-primary)]"
        @click="goMarket"
        aria-label="Market"
      >
        <MarketIcon class="h-6 w-6" />
        Market
      </button>

      <button
        class="relative flex h-14 w-14 -translate-y-4 items-center justify-center rounded-full bg-[var(--accent-red)] text-white shadow-[0_16px_30px_-16px_rgba(255,56,79,0.7)] transition-transform hover:-translate-y-[18px]"
        @click="goCreate"
        aria-label="Create"
      >
        <PlusCircleIcon class="h-7 w-7" />
      </button>

      <button
        class="flex flex-col items-center gap-1 text-xs font-medium text-[var(--text-tertiary)] transition-colors hover:text-[var(--text-primary)]"
        @click="goMessages"
        aria-label="Messages"
      >
        <MessagesIcon class="h-6 w-6" />
        Messages
      </button>

      <button
        class="flex flex-col items-center gap-1 text-xs font-medium text-[var(--text-tertiary)] transition-colors hover:text-[var(--text-primary)]"
        :class="{ 'text-[var(--accent-red)]': activeName === 'user-space-index' }"
        @click="goMe"
        aria-label="Me"
      >
        <UserIcon class="h-6 w-6" />
        Me
      </button>
    </div>
  </nav>
</template>

<style scoped>
</style>
