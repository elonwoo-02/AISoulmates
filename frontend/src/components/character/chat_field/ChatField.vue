<script setup>
import {computed, nextTick, ref, useTemplateRef} from 'vue'
import InputField from '@/components/character/chat_field/input_field/InputField.vue'
import CharacterPhotoField from '@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue'
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";

// 组件属性定义
const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')
const chatHistoryRef = useTemplateRef('chat-history-ref')
const history = ref([]) // 存储聊天历史记录
const isThinking = ref(false) // 标记AI是否正在思考/回复

/**
 * 显示聊天对话框（供父组件调用）
 * 1. 打开模态框
 * 2. 等待Vue更新DOM后自动聚焦到输入框
 */
async function showModal() {
  modalRef.value.showModal()

  await nextTick()
  inputRef.value.focus()
}

/**
 * 计算模态框的样式
 * 如果有好友信息，则设置背景图为好友角色的背景图片
 * 否则返回空样式对象
 */
const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})

/**
 * 在聊天历史记录末尾添加新消息
 * @param {Object} msg - 要添加的消息对象
 */
function handlePushBackMessage(msg) {
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom() // 添加后自动滚动到底部
}

/**
 * 在最后一条消息上追加内容（用于流式响应）
 * @param {string} delta - 要追加的内容
 */
function handleAddToLastMessage(delta) {
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom() // 更新后自动滚动到底部
}

/**
 * 在聊天历史记录开头添加消息
 * @param {Object} msg - 要添加的消息对象
 */
function handlePushFrontMessage(msg) {
  history.value.unshift(msg)
}

/**
 * 关闭聊天对话框
 * 1. 关闭模态框
 * 2. 关闭输入框
 */
function handleClose() {
  modalRef.value.close()
  inputRef.value.close()
}

/**
 * 更新AI思考状态
 * // todo: 丰富更多思考状态：思考中/思考完成/发送消息/报错；
 * // todo: 生活状态：忙碌/空闲/忙碌中;
 * // todo: 丰富状态样式图标；
 * @param {boolean} value - 是否正在思考
 */
function handleUpdateProcessing(value) {
  isThinking.value = value
}

// 暴露给父组件的方法
defineExpose({
  showModal,
})
</script>

<template>
  <!--todo: 更新对话框的样式，包括头部、消息历史区、输入框 -->
  <!-- 聊天对话框：阻止事件冒泡，确保点击对话框时不会触发父元素的点击监听器 -->
  <dialog ref="modal-ref" class="modal" @click.stop>
    <!-- 对话框内容区域，应用动态背景样式 -->
    <div class="modal-box p-2 max-w-sm aspect-3/5 flex flex-col" :style="modalStyle">
      <!-- 头部区域：角色信息 + 关闭按钮 -->
      <div class="flex justify-between items-start mb-2">
        <CharacterPhotoField v-if="friend" :character="friend.character" :isThinking="isThinking" />
        <button @click.stop="handleClose" class="btn btn-sm btn-circle btn-ghost bg-black/30 text-white hover:bg-black/50">✕</button>
      </div>

      <!-- 消息历史区域 -->
      <ChatHistory
          ref="chat-history-ref"
          v-if="friend"
          :history="history"
          :friendId="friend.id"
          :character="friend.character"
          @pushBackFrontMessage="handlePushFrontMessage"
      />

      <!-- 底部输入区域 -->
      <InputField
          v-if="friend"
          ref="input-ref"
          :friendId="friend.id"
          @pushBackMessage="handlePushBackMessage"
          @addToLastMessage="handleAddToLastMessage"
          @updateProcessing="handleUpdateProcessing"
      />
    </div>
  </dialog>
</template>

<style scoped>
</style>
