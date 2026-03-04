<script setup>
import { computed, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import SearchModal from "./SearchModal.vue";

const searchQuery = ref("");
const showSearchModal = ref(false);
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

function openSearchModal() {
  showSearchModal.value = true;
}

function closeSearchModal() {
  showSearchModal.value = false;
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

      <!-- Search Icon -->
      <button @click="openSearchModal" class="absolute right-4 p-1 text-[--text-secondary] hover:text-[--text-primary]">
        <SearchIcon class="w-5 h-5" />
      </button>
    </div>
  </nav>

  <!-- Search Modal -->
  <SearchModal :show="showSearchModal" @close="closeSearchModal" />
</template>

<style scoped>
</style>
