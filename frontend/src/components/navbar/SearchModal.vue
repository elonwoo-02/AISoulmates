<script setup>
import { ref, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import ArrowLeftIcon from "./icons/ArrowLeftIcon.vue";

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["close"]);

const searchQuery = ref("");
const searchInputRef = ref(null);
const router = useRouter();
const route = useRoute();

watch(
  () => route.query.q,
  (newQ) => {
    searchQuery.value = newQ || "";
  },
  { immediate: true }
);

// 自动聚焦搜索框
watch(
  () => props.show,
  async (newVal) => {
    if (newVal) {
      searchQuery.value = "";
      await nextTick();
      searchInputRef.value?.focus();
    }
  }
);

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: "homepage-index", query: { q: searchQuery.value.trim() } });
    emit("close");
  }
}

function closeModal() {
  emit("close");
}
</script>

<template>
  <dialog :class="{ 'modal modal-open': props.show }" class="modal-bottom">
    <div class="fixed inset-0 bg-white flex flex-col">
      <!-- Search Bar -->
      <div class="flex items-center gap-3 px-4 py-3 border-b border-base-200">
        <button @click="closeModal" class="btn btn-ghost btn-sm p-0">
          <ArrowLeftIcon class="w-5 h-5" />
        </button>

        <form @submit.prevent="handleSearch" class="flex-1 flex items-center gap-2">
          <input
            ref="searchInputRef"
            v-model="searchQuery"
            type="text"
            placeholder="Search characters..."
            class="input input-sm flex-1 rounded-md bg-base-200 focus:outline-none focus:bg-base-100"
          />
          <button type="submit" class="btn btn-sm btn-ghost p-0 text-red-500 font-medium">
            search
          </button>
        </form>
      </div>

      <!-- Search History (placeholder) -->
      <div class="flex-1 overflow-y-auto p-4">
        <div class="text-center text-gray-400 text-sm">
          Enter keyword to search
        </div>
      </div>
    </div>

    <form method="dialog" class="modal-backdrop">
      <button @click="closeModal">close</button>
    </form>
  </dialog>
</template>

<style scoped>
.modal-bottom {
  align-items: flex-end;
}
.modal-bottom[open] {
  display: flex;
}
.modal-bottom .modal-box {
  max-width: 100%;
  width: 100%;
  border-radius: 0;
  margin: 0;
}
</style>
