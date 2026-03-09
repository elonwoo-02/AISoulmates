<script setup>

import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {computed, ref, useTemplateRef} from "vue";
import streamApi from "@/js/http/streamApi.js";

const props = defineProps({
  friendId: {
    type: [Number, String],
    required: true,
  },
  variant: {
    type: String,
    default: "modal",
  },
});

const emit = defineEmits(["pushBackMessage", "addToLastMessage", "updateProcessing"]);
const inputRef = useTemplateRef("input-ref");
const message = ref("");
const processing = ref(false);

const isPageVariant = computed(() => props.variant === "page");
const formClass = computed(() =>
  isPageVariant.value
    ? "flex items-center gap-2 w-full px-2 py-1.5"
    : "flex items-center gap-2 h-8 w-full px-2"
);
const inputClass = computed(() =>
  isPageVariant.value
    ? "input h-9 w-full rounded-lg border-0 bg-gray-100 text-base text-gray-800 placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-300"
    : "input h-full w-full rounded-xl bg-black/20 text-base text-white placeholder:text-white/60 focus:outline-none focus:border-none focus:ring-0 focus:bg-black/30"
);
const actionButtonClass = computed(() =>
  isPageVariant.value
    ? "flex h-9 min-w-[60px] items-center justify-center rounded-lg bg-gray-200 text-gray-600 font-medium text-sm transition-colors hover:bg-gray-300"
    : "flex h-8 w-8 items-center justify-center rounded bg-slate-800 text-white transition-colors hover:bg-slate-700"
);
const showMic = computed(() => !isPageVariant.value);

function focus() {
  inputRef.value.focus();
}

async function handleSend() {
  if (processing.value) return;
  processing.value = true;
  emit("updateProcessing", true);

  const content = message.value.trim();
  if (!content) {
    processing.value = false;
    emit("updateProcessing", false);
    return;
  }
  message.value = "";

  const now = new Date().toISOString();
  emit("pushBackMessage", {role: "user", content: content, id: crypto.randomUUID(), time: now, status: "sent" });
  emit("pushBackMessage", {role: "ai", content: "", id: crypto.randomUUID(), time: now, status: "sent" });

  try {
    await streamApi("/api/friend/message/chat/", {
      body: {
        friend_id: props.friendId,
        message: content,
      },
      onmessage(data, isDone) {
        if (isDone) {
          processing.value = false;
          emit("updateProcessing", false);
        } else if (data.content) {
          emit("addToLastMessage", data.content);
        }
      },
      onerror(err) {
        processing.value = false;
        emit("updateProcessing", false);
      }
    });
  } catch (err) {
    processing.value = false;
    emit("updateProcessing", false);
  }
}

defineExpose({
  focus,
});
</script>

<template>
  <form @submit.prevent="handleSend" :class="formClass">
    <div v-if="isPageVariant" class="flex items-center gap-1.5">
      <button
        type="button"
        class="flex h-9 w-9 items-center justify-center rounded-lg bg-transparent text-gray-500 hover:bg-gray-100"
      >
        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
      </button>
    </div>
    <input
        ref="input-ref"
        v-model="message"
        :class="inputClass"
        type="text"
        :placeholder="isPageVariant ? '' : 'type here...'"
    >
    <div class="flex items-center gap-1">
      <div
        v-if="showMic"
        class="flex h-8 w-8 cursor-pointer items-center justify-center rounded bg-slate-800 text-white transition-colors hover:bg-slate-700"
      >
        <MicIcon/>
      </div>
      <div @click="handleSend" :class="actionButtonClass">
        <span v-if="isPageVariant">发送</span>
        <SendIcon v-else/>
      </div>
    </div>
  </form>
</template>

<style scoped>

</style>
