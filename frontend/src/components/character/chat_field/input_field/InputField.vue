<!--
InputField.vue - 聊天输入组件

功能:
1. 提供文本输入和发送功能
2. 支持语音输入模式切换
3. 处理流式API响应
4. 管理音频播放队列

Props:
- friendId: 必传，当前聊天好友ID

Emits:
- pushBackMessage: 添加新消息到聊天历史
- addToLastMessage: 流式追加内容到最后一条消息
- updateProcessing: 更新处理状态
-->
<script setup>
import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {onUnmounted, ref, useTemplateRef} from "vue";
import streamApi from "@/js/http/streamApi.js";
import Microphone from "@/components/character/chat_field/input_field/Microphone.vue";

const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage', 'updateProcessing'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')      // 响应式消息文本状态
let processId = 0                 // 用于跟踪当前消息处理的计数器（用于忽略旧响应，打断聊天）
const showMic = ref(false)  // 控制是否显示麦克风输入

// 音频流处理相关变量
let mediaSource = null;        // MediaSource对象，用于处理音频流
let sourceBuffer = null;       // SourceBuffer对象，用于存储音频数据
let audioPlayer = new Audio(); // 全局播放器实例
let audioQueue = [];           // 待写入 Buffer 的二进制队列
let isUpdating = false;        // Buffer 是否正在写入（防止并发写入）

/**
 * 初始化音频流播放器
 * 1. 重置播放器和队列状态
 * 2. 创建MediaSource对象并设置给audioPlayer
 * 3. 监听sourceopen事件来创建SourceBuffer
 * 4. 开始播放（需要用户交互后才能实际播放）
 */
const initAudioStream = () => {
    // 重置音频播放器状态
    audioPlayer.pause();
    // 清空音频数据队列
    audioQueue = [];
    // 重置更新状态标志
    isUpdating = false;

    // 创建新的MediaSource对象用于处理音频流
    mediaSource = new MediaSource();
    // 创建对象URL并赋值给音频播放器
    audioPlayer.src = URL.createObjectURL(mediaSource);

    // 监听MediaSource的sourceopen事件
    mediaSource.addEventListener('sourceopen', () => {
        try {
            // 创建音频类型的SourceBuffer
            sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
            // 监听SourceBuffer的updateend事件
            sourceBuffer.addEventListener('updateend', () => {
                // 更新状态标志
                isUpdating = false;
                // 处理队列中的下一个音频块
                processQueue();
            });
        } catch (e) {
            console.error("MSE AddSourceBuffer Error:", e);
        }
    });

    // 尝试播放音频（需要用户交互后才能实际播放）
    audioPlayer.play().catch(e => console.error("等待用户交互以播放音频"));
};

/**
 * 处理音频队列
 * 1. 检查是否可以处理队列（当前没有写入操作且队列不为空）
 * 2. 从队列中取出第一个音频块
 * 3. 将音频块追加到SourceBuffer中
 * 4. 处理错误情况
 */
const processQueue = () => {
    // 检查是否可以处理队列：当前没有写入操作、队列不为空、SourceBuffer可用且未在更新
    if (isUpdating || audioQueue.length === 0 || !sourceBuffer || sourceBuffer.updating) {
        return;
    }

    isUpdating = true;  // 标记为正在写入
    const chunk = audioQueue.shift();  // 从队列头部取出音频块
    
    try {
        // 将音频数据追加到SourceBuffer
        sourceBuffer.appendBuffer(chunk);
    } catch (e) {
        console.error("SourceBuffer Append Error:", e);
        isUpdating = false;  // 出错时重置状态
    }
};

/**
 * 停止音频播放并清理资源
 * 1. 暂停音频播放器
 * 2. 清空音频队列
 * 3. 关闭MediaSource
 * 4. 释放对象URL
 */
const stopAudio = () => {
    // 停止音频播放
    audioPlayer.pause();
    // 清空音频队列
    audioQueue = [];
    // 重置更新状态
    isUpdating = false;

    // 清理MediaSource资源
    if (mediaSource) {
        if (mediaSource.readyState === 'open') {
            try {
                // 标记流结束
                mediaSource.endOfStream();
            } catch (e) {
            }
        }
        mediaSource = null;
    }

    // 清理音频播放器资源
    if (audioPlayer.src) {
        // 释放对象URL
        URL.revokeObjectURL(audioPlayer.src);
        audioPlayer.src = '';
    }
};

/**
 * 处理音频数据块
 * @param {string} base64Data - Base64编码的音频数据
 * 1. 解码Base64数据
 * 2. 将数据转换为Uint8Array
 * 3. 将音频块添加到队列
 * 4. 触发队列处理
 */
const handleAudioChunk = (base64Data) => {
    try {
        // 解码Base64音频数据
        const binaryString = atob(base64Data);
        const len = binaryString.length;
        // 创建Uint8Array缓冲区存储原始音频数据
        const bytes = new Uint8Array(len);
        
        // 将Base64字符串转换为字节数组
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        // 将音频数据加入播放队列
        audioQueue.push(bytes);
        // 触发队列处理
        processQueue();
    } catch (e) {
        console.error("Base64 Decode Error:", e);
    }
};


/**
 * 组件卸载时的清理操作
 */
onUnmounted(() => {
    // 1. 暂停音频播放器
    audioPlayer.pause();
    // 2. 清空音频播放器的src属性，释放资源
    audioPlayer.src = '';
});


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

  initAudioStream()

  const curId = ++ processId  // 更新处理ID
  message.value = ''  // 清空输入框

  // 向父组件发送用户消息和AI空消息
  emit('pushBackMessage', {role: 'user', content: content, id: crypto.randomUUID()})
  emit('pushBackMessage', {role: 'ai', content: '', id: crypto.randomUUID()})

  try {
    emit('updateProcessing', true) // 开始处理时更新状态
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
        if (data.audio) {
          handleAudioChunk(data.audio)
        }

      },
      onerror(err) {
        console.error(err)
      },
    })
    emit('updateProcessing', false) // 处理完成时更新状态
  } catch (err) {
    emit('updateProcessing', false) // 出错时也更新状态
    console.error(err)
  }
}

/**
 * 关闭麦克风输入模式
 */
function close() {
  ++ processId
  showMic.value = false
  stopAudio()
}

/**
 * 打断当前语音播放
 * 1. 更新处理ID（忽略后续响应）
 * 2. 停止音频播放
 */
function handleStop() {
  // 更新处理ID以忽略后续响应
  ++ processId
  // 停止当前音频播放
  stopAudio()
}

// 暴露方法给父组件
defineExpose({
  focus,
  close,
})
</script>

<template>
  <!-- 
    主表单：文本输入模式 
    - 当showMic为false时显示文本输入表单
    - 提交时调用handleSend方法
    - 包含文本输入框、发送按钮和语音输入切换按钮
  -->
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
  
  <!-- 
    语音输入模式组件
    - 当showMic为true时显示
    - 事件处理:
      * @close: 关闭语音输入模式
      * @send: 发送语音消息
      * @stop: 打断当前语音播放
  -->
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