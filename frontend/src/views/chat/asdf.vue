<template>
  <!-- 1. 主容器：占据全屏 -->
  <div class="relative h-screen bg-gray-50 overflow-hidden">

    <!-- 2. 消息展示区：占据全屏，底部留出足够的内边距防止被输入框遮挡 -->
    <main class="h-full overflow-y-auto pt-4 pb-32 px-4 custom-scrollbar" ref="messageContainer">
      <div class="max-w-3xl mx-auto space-y-6"> <!-- 限制内容最大宽度，更像 AI 聊天 -->
        <div v-for="(msg, index) in chatHistory" :key="index"
             :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
          <div :class="['max-w-[90%] p-4 rounded-2xl shadow-sm',
                       msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white text-gray-800 border border-gray-100']">
            <div class="prose prose-sm max-w-none"
                 :class="{'prose-invert text-white': msg.role === 'user'}"
                 v-html="renderMarkdown(msg.content)">
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="flex justify-start">
          <div class="bg-white border border-gray-100 text-gray-400 p-4 rounded-2xl shadow-sm italic">
            AI 正在思考...
          </div>
        </div>
      </div>
    </main>

    <!-- 3. 悬浮输入框：固定在窗口正下方 -->
    <div class="fixed bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-gray-50 via-gray-50/80 to-transparent">
      <div class="max-w-3xl mx-auto relative">
        <div class="relative flex items-center bg-white rounded-2xl shadow-xl border border-gray-200 p-2 focus-within:ring-2 focus-within:ring-blue-500/20 transition-all">
          <textarea v-model="userInput"
                    @keydown.enter.prevent="handleEnter"
                    rows="1"
                    placeholder="给 AI Soulmate 发送消息..."
                    class="flex-1 bg-transparent border-none focus:outline-none px-4 py-2 resize-none max-h-40"
                    :disabled="loading"></textarea>

          <button @click="sendMessage"
                  class="ml-2 bg-blue-600 text-white p-2 rounded-xl hover:bg-blue-700 transition disabled:opacity-30 disabled:grayscale"
                  :disabled="loading || !userInput.trim()">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
            </svg>
          </button>
        </div>
        <p class="text-center text-xs text-gray-400 mt-2">
          AI 可能会产生错误 ，请核查重要信息。
        </p>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, onMounted, nextTick } from 'vue';
import api from '@/js/http/api';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css'; // 引入代码高亮样式

// 处理回车键
const handleEnter = (e) => {
  if (e.shiftKey) {
    // Shift + Enter 换行，不做处理
    return;
  }
  sendMessage();
};


// 初始化 Markdown 解析器
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: function (str, lang ) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value;
      } catch (__) {}
    }
    return ''; // 使用默认转义
  }
});

const userInput = ref('');
const chatHistory = ref([]);
const loading = ref(false);
const messageContainer = ref(null);

const renderMarkdown = (content) => {
  return md.render(content);
};

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
      history: chatHistory.value.slice(0, -1)
    });
    chatHistory.value.push({ role: 'assistant', content: response.data.reply });
  } catch (error) {
    chatHistory.value.push({ role: 'assistant', content: '**错误**：无法连接到 AI 服务。' });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};

onMounted(() => {
  chatHistory.value.push({ role: 'assistant', content: '你好！我是你的 **AI 伴侣**。你可以试着让我写一段代码或列表。' });
});
</script>

<style scoped>

.h-screen {
  height: 100vh;
  height: 100dvh;
}

/* 消息列表最大宽度限制，使其居中 */
.max-w-3xl {
  max-width: 48rem;
}

/* 隐藏滚动条但保留功能（可选） */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}

/* 基础 Markdown 样式微调 */
.prose :deep(p) { margin-bottom: 0.75rem; line-height: 1.6; }
.prose :deep(pre) {
  background-color: #f6f8fa;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
}
.prose :deep(code) {
  font-family: monospace;
  background-color: rgba(0,0,0,0.05);
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
}
.prose :deep(ul) { list-style-type: disc; padding-left: 1.5rem; }
.prose :deep(ol) { list-style-type: decimal; padding-left: 1.5rem; }
</style>
