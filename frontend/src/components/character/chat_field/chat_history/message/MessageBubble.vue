<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user.js'


const props = defineProps(['message', 'character'])

const user = useUserStore()

const isSelf = computed(() => props.message.role === 'user')

const avatarUrl = computed(() => {
  return isSelf.value ? user.photo : props.character.photo
})

const senderName = computed(() => {
  return isSelf.value ? user.username : props.character.name
})

const formattedTime = computed(() => {
  if (!props.message.time) return ''
  const date = new Date(props.message.time)
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  const messageDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
  
  const timeStr = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  
  // Calculate days difference
  const daysDiff = Math.floor((today - messageDate) / (1000 * 60 * 60 * 24))
  
  if (daysDiff === 0) {
    // Today - just show time
    return timeStr
  } else if (daysDiff === 1) {
    // Yesterday
    return `昨天 ${timeStr}`
  } else if (daysDiff < 7) {
    // This week - show day name
    const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    return `${dayNames[date.getDay()]} ${timeStr}`
  } else {
    // Older - show full date
    return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }) + ' ' + timeStr
  }
})

const statusText = computed(() => {
  if (isSelf.value) {
    switch (props.message.status) {
      case 'sending': return '发送中...'
      case 'sent': return '已发送'
      case 'failed': return '发送失败'
      default: return ''
    }
  }
  return ''
})
</script>

<template>
  <div v-if="message.content" class="flex mb-0" :class="isSelf ? 'flex-row-reverse' : 'flex-row'">
    <!-- Avatar -->
    <div class="shrink-0 mx-1" style="margin-top: 1.5rem;">
      <div class="w-8 h-8 rounded-full overflow-hidden">
        <img :src="avatarUrl" alt="" class="w-full h-full object-cover" />
      </div>
    </div>

    <!-- Message Container (Name + Bubble + Status) -->
    <div class="flex flex-col max-w-[70%]" :class="isSelf ? 'items-end' : 'items-start'">
      <!-- Name above bubble -->
      <span class="text-xs text-gray-400 mb-1 mx-1">{{ senderName }}</span>

      <!-- Bubble -->
      <div
        class="px-3 py-2 rounded-2xl wrap-break-word text-sm"
        :class="isSelf
          ? 'bg-green-500 text-white'
          : 'bg-gray-200 text-gray-800'"
      >
        {{ message.content }}
      </div>

      <!-- Status below bubble -->
      <div class="flex items-center gap-2 mt-1 mx-1 text-xs text-gray-400" :class="isSelf ? 'flex-row-reverse' : 'flex-row'">
        <span v-if="formattedTime">{{ formattedTime }}</span>
        <span v-if="statusText" :class="{ 'text-red-400': message.status === 'failed' }">
          {{ statusText }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
