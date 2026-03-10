<script setup>
import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {ref, useTemplateRef} from "vue";
import streamApi from "@/js/http/streamApi.js";
import Microphone from "@/components/character/chat_field/input_field/Microphone.vue";

// 定义组件接受的props - friendId是必传参数
const props = defineProps(['friendId'])
// 定义组件可以触发的事件，来自父组件
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])
// 输入框的模板引用
const inputRef = useTemplateRef('input-ref')
// 响应式消息文本状态
const message = ref('')
// 用于跟踪当前消息处理的计数器（用于忽略旧响应，打断聊天）
let processId = 0
// 控制是否显示麦克风输入
const showMic = ref(false)

/**
 * 聚焦输入框
 */
function focus() {
  inputRef.value.focus()
}

/**
 * 处理发送消息（文本或音频）
 * @param {Event} event - 提交事件（可选）
 * @param {string} audio_msg - 音频消息内容（可选）
 */
async function handleSend(event, audio_msg) {
  let content
  if (audio_msg) {
    content = audio_msg.trim()  // 如果是音频消息，使用音频内容
  } else {
    content = message.value.trim()  // 否则使用输入框的文本内容
  }
  if (!content) return  // 内容为空则不处理

  const curId = ++ processId  // 更新处理ID
  message.value = ''  // 清空输入框

  // 向父组件发送用户消息和AI空消息
  emit('pushBackMessage', {role: 'user', content: content, id: crypto.randomUUID()})
  emit('pushBackMessage', {role: 'ai', content: '', id: crypto.randomUUID()})

  try {
    // 调用流式API发送消息
    await streamApi('/api/friend/message/chat/', {
      body: {
        friend_id: props.friendId,
        message: content,
      },
      onmessage(data) {                  // onmessage回调：处理流式API返回的消息
        if (curId !== processId) return  // 如果不是当前处理的消息则忽略

        if (data.content) {
          emit('addToLastMessage', data.content)  // 将AI回复内容流式添加到消息列表
        }
      },
      onerror(err) {
        console.error(err)
      },
    })
  } catch (err) {
    console.error(err)
  }
}

/**
 * 关闭麦克风输入模式
 */
function close() {
  ++ processId
  showMic.value = false
}

/**
 * 打断角色说话
 */
function handleStop() {
  ++ processId
}

// 暴露方法给父组件
defineExpose({
  focus,
  close,
})
</script>

<template>
  <!-- 主表单：文本输入模式 -->
  <form 
    v-if="!showMic" 
    @submit.prevent="handleSend" 
    class="w-full h-12 flex items-center"
  >
    <!-- 文本输入框：打开自动聚焦，松开enter键触发handleSend函数 -->
    <input
        ref="input-ref"
        v-model="message"
        class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl pr-20"
        type="text"
        placeholder="输入消息..."
        @keyup.enter="handleSend"
    >
    
    <!-- 发送按钮：点击触发handleSend函数 -->
    <div 
      @click="handleSend" 
      class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer"
      title="发送消息"
    >
      <SendIcon />
    </div>
    
    <!-- 麦克风切换按钮：点击切换语音输入模式 -->
    <div 
      @click="showMic = true" 
      class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer"
      title="语音输入"
    >
      <MicIcon />
    </div>
  </form>
  
  <!-- 语音输入模式：语音输入完成后发送，打断对方说话 -->
  <Microphone
      v-else
      @close="showMic = false"
      @send="(audioMsg) => handleSend(null, audioMsg)"
      @stop="handleStop"
  />
</template>

<style scoped>
.input:focus {
  outline: none;
}
</style>