<script setup>
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";

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
  <nav class="fixed top-0 left-0 right-0 z-40 border-b border-black/5 bg-white backdrop-blur">
    <div class="mx-auto flex justify-center w-full max-w-300 items-center gap-4 px-4 py-3 sm:px-6 lg:px-8">
      <div class="flex justify-center items-center gap-5">
        <RouterLink
          :to="{ name: 'friend-index' }"
          class="relative text-[15px] font-semibold tracking-tight text-[--text-secondary] transition-colors hover:text-[--text-primary]"
          :class="{ 'text-[--accent-red] border-b-2 border-red-500': activeTab === 'friend' }"
        >
          Friend
        </RouterLink>

        <RouterLink
          :to="{ name: 'homepage-index' }"
          class="relative text-[15px] font-semibold tracking-tight text-[--text-secondary] transition-colors hover:text-[--text-primary]"
          :class="{ 'text-[--accent-red] border-b-2 border-red-500': activeTab === 'explore' }"
        >
          Explore
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<style scoped>
</style>
