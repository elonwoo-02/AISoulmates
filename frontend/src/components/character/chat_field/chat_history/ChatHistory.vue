<script setup>
import {nextTick, onBeforeUnmount, onMounted, useTemplateRef} from "vue";
import api from "@/js/http/api.js";
import MessageBubble from "@/components/character/chat_field/chat_history/message/MessageBubble.vue";

const props = defineProps(
  ['history', 'friendId', 'character']
)
const emit = defineEmits(['pushBackFrontMessage'])
const scrollRef = useTemplateRef('scroll-ref')
const sentinelRef = useTemplateRef('sentinel-ref')
let loading = false
let hasMessage = true
let lastMessageId = 0

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const sentinelRect = sentinelRef.value.getBoundingClientRect()
  const scrollRect = scrollRef.value.getBoundingClientRect()
  return sentinelRect.top < scrollRect.bottom && sentinelRect.bottom > scrollRect.top
}

async function loadMore() {
  if (loading || !hasMessage) return
  loading = true

  let newMessages = []
  try {
    const res = await api.get('/api/friend/message/get_history/', {
      params: {
        friend_id: props.friendId,
        last_message_id: lastMessageId
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newMessages = data.messages
    }
  } catch (err) {
  } finally {
    loading = false
    if (newMessages.length === 0) {
      hasMessage = false
    } else {
      const oldestMessageId = newMessages[newMessages.length - 1].id
      const oldHeight = scrollRef.value.scrollHeight
      const oldTop = scrollRef.value.scrollTop

      for (const m of newMessages) {  // 后端已按 id 降序返回；配合 unshift 可保持整体时间正序
        const msgTime = m.created_at || new Date().toISOString()
        emit('pushBackFrontMessage', {
          role: 'ai',
          content: m.output,
          id: crypto.randomUUID(),
          time: msgTime,
          status: 'sent',
        })
        emit('pushBackFrontMessage', {
          role: 'user',
          content: m.user_message,
          id: crypto.randomUUID(),
          time: msgTime,
          status: 'sent',
        })
      }
      lastMessageId = oldestMessageId
      await nextTick()

      const newHeight = scrollRef.value.scrollHeight
      scrollRef.value.scrollTop = oldTop + newHeight - oldHeight

      if (checkSentinelVisible()) {
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async () => {
  await nextTick()

  observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      loadMore()
    }
  }, {root: scrollRef.value, rootMargin: '100px', threshold: 0});
  observer.observe(sentinelRef.value)

  await loadMore()
})

onBeforeUnmount(() => {
  observer?.disconnect()
})

async function scrollToBottom() {
  await nextTick()
  scrollRef.value.scrollTop = scrollRef.value.scrollHeight
}

defineExpose({
  scrollToBottom,
})
</script>

<template>
  <div ref="scroll-ref" class="flex-1 overflow-y-scroll no-scrollbar w-full">
    <div ref="sentinel-ref" class="h-2"></div>
    <MessageBubble
        v-for="message in history"
        :key="message.id"
        :message="message"
        :character="character"
    />
  </div>

</template>

<style scoped>
/* 隐藏 Chrome, Safari 和 Opera 的滚动条 */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* 隐藏 IE, Edge 和 Firefox 的滚动条 */
.no-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
</style>



