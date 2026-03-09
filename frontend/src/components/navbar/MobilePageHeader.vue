<script setup>
import { useRouter } from "vue-router";
import ArrowLeftIcon from "@/components/navbar/icons/ArrowLeftIcon.vue";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  fallbackRoute: {
    type: [Object, String],
    default: () => ({ name: "homepage-index" }),
  },
});

const router = useRouter();

function handleBack() {
  if (window.history.state?.back) {
    router.back();
    return;
  }

  router.push(props.fallbackRoute);
}
</script>

<template>
  <div class="md:hidden">
    <header class="fixed top-0 left-0 right-0 z-40 border-b border-black/5 bg-white backdrop-blur">
      <div class="mx-auto flex w-full max-w-300 items-center justify-center px-4 py-3 sm:px-6 lg:px-8">
        <button
          type="button"
          class="absolute left-4 flex h-10 w-10 items-center justify-center rounded-full text-[--text-secondary] transition-colors hover:bg-black/5 hover:text-[--text-primary]"
          aria-label="返回上一页"
          @click="handleBack"
        >
          <ArrowLeftIcon class="h-5 w-5" />
        </button>

        <h1 class="max-w-[60vw] truncate text-[15px] font-semibold tracking-tight text-[--text-primary]">
          {{ title }}
        </h1>
      </div>
    </header>

    <div class="h-[61px]"></div>
  </div>
</template>

<style scoped>
</style>
