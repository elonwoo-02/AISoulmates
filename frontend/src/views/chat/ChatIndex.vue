<template>
  <div class="flex flex-col h-screen bg-gray-100">
<!--    &lt;!&ndash; Header &ndash;&gt;-->
<!--    <header class="bg-white shadow-sm p-4">-->
<!--      <h1 class="text-xl font-bold text-center text-blue-600">AI Soulmate 聊天</h1>-->
<!--    </header>-->

    <!-- Chat Messages -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messageContainer">
      <div v-for="(msg, index) in chatHistory" :key="index" 
           :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
        <div :class="['max-w-xs md:max-w-md p-3 rounded-lg shadow', 
                     msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-white text-gray-800']">
          {{ msg.content }}
        </div>
      </div>
      <div v-if="loading" class="flex justify-start">
        <div class="bg-white text-gray-500 p-3 rounded-lg shadow italic">
          AI 正在思考中...
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <footer class="bg-white p-4 border-t">
      <div class="flex space-x-2">
        <input v-model="userInput" @keyup.enter="sendMessage"
               type="text" placeholder="输入你想说的话..." 
               class="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
               :disabled="loading" />
        <button @click="sendMessage" 
                class="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 transition disabled:opacity-50"
                :disabled="loading || !userInput.trim()">
          发送
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import api from '@/js/http/api';

const userInput = ref('');
const chatHistory = ref([]);
const loading = ref(false);
const messageContainer = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
  }
};

const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return;

  const message = userInput.value.trim();
  chatHistory.value.push({ role: 'user', content: message });
  userInput.value = '';
  loading.value = true;
  scrollToBottom();

  try {
    const response = await api.post('/api/chat/', {
      message: message,
      history: chatHistory.value.slice(0, -1) // 发送除当前消息外的历史记录
    });

    chatHistory.value.push({ role: 'assistant', content: response.data.reply });
  } catch (error) {
    console.error('Chat error:', error);
    chatHistory.value.push({ role: 'assistant', content: '抱歉，我现在有点累了，请稍后再试。' });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};

onMounted(() => {
  chatHistory.value.push({ role: 'assistant', content: '你好！我是你的 AI 伴侣，很高兴见到你。' });
});
</script>
