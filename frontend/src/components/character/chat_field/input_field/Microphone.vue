<script setup>
import KeyboardIcon from "@/components/character/icons/KeyboardIcon.vue";
import {onBeforeUnmount, onMounted, ref} from "vue";
import {MicVAD} from "@ricky0123/vad-web";
import api from "@/js/http/api.js";

// 定义组件事件：关闭语音输入、发送消息、停止语音输入
const emit = defineEmits(['close', 'send', 'stop'])
// 标识当前是否正在说话
const isSpeaking = ref(false)

// VAD实例变量，用于控制语音活动检测
let vadInstance = null;

/**
 * 开始语音录制
 * 初始化语音活动检测(VAD)实例并开始监听麦克风输入
 * 当检测到语音时触发onSpeechStart回调
 * 当语音结束时触发onSpeechEnd回调并发送音频数据
 */
const startRecording = async () => {
  const baseUrl = "http://localhost:5173/vad/";
  try {
    vadInstance = await MicVAD.new({
      // VAD基础资源路径
      baseAssetPath: baseUrl,
      // 语音开始回调 - 设置说话状态并停止其他输入
      onSpeechStart: () => {
        isSpeaking.value = true;
        emit('stop')
      },
      // 语音结束回调 - 重置状态并发送音频数据
      onSpeechEnd: (audio) => {
        isSpeaking.value = false;
        const pcm16 = float32ToInt16(audio);
        sendToBackend(pcm16);
      },
      // ONNX运行时配置
      ortConfig: (ort) => {
        ort.env.wasm.wasmPaths = baseUrl; // 设置WASM路径
        ort.env.logLevel = "error";      // 只记录错误日志
      },
      positiveSpeechThreshold: 0.8,   // 语音检测阳性阈值
      negativeSpeechThreshold: 0.65,  // 语音检测阴性阈值
      minSpeechFrames: 5,             // 最小语音帧数
      redemptionFrames: 5,            // 补偿帧数
    });

    await vadInstance.start();
  } catch (e) {
    console.error("VAD 初始化失败:", e);
  }
};
// 将 Float32 转 PCM 16-bit
const float32ToInt16 = (float32Array) => {
  // 创建16位整型缓冲区
  const buffer = new Int16Array(float32Array.length);
  
  // 遍历每个采样点进行转换
  for (let i = 0; i < float32Array.length; i++) {
    // 将采样值限制在[-1, 1]范围内
    let s = Math.max(-1, Math.min(1, float32Array[i]));
    
    // 将浮点值转换为16位整型
    buffer[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
  }
  
  // 返回ArrayBuffer格式的数据
  return buffer.buffer;
};

/**
 * 将音频数据发送到后端处理
 * @param {ArrayBuffer} arrayBuffer - PCM 16-bit格式的音频数据
 */
const sendToBackend = async (arrayBuffer) => {
  // 将音频数据包装为Blob对象
  const blob = new Blob([arrayBuffer], { type: "audio/pcm" })
  
  // 创建表单数据用于上传
  const formData = new FormData()
  formData.append("audio", blob, 'voice.pcm')  // 添加音频文件

  try {
    // 发送POST请求到后端API
    const res = await api.post('/api/friend/message/stt/stt/', formData)
    const data = res.data
    console.log(data)
    // 处理成功响应
    if (data.result === 'success') {
      emit('send', null, data.text)  // 发送识别结果
    }
  } catch (err) {
    console.error(err)
  }
};

// 组件挂载时自动开始录音
onMounted(() => {
  startRecording()  // 调用录音开始方法
})

// 组件卸载前清理资源
onBeforeUnmount(() => {
  if (vadInstance) {
    vadInstance.destroy()  // 销毁VAD实例
    vadInstance = null    // 释放引用
  }
})
</script>

<template>
  <!-- 语音输入容器 -->
  <div class="w-full h-12 flex items-center bg-black/30 backdrop-blur-sm rounded-2xl">
    <!-- 语音活动可视化 - 当用户说话时显示波形动画 -->
    <div v-if="isSpeaking" class="flex items-center justify-center gap-1 h-6 flex-1">
      <div
        v-for="i in 32" :key="i"
        class="w-0.5 bg-blue-400 rounded-full animate-wave"
        :style="{ animationDelay: `${i * 0.1}s` }"
      ></div>
    </div>
    <!-- 语音输入提示 - 当用户没有说话时显示 -->
    <div v-else class="text-white/50 text-base w-full text-center">
      按住说话...
    </div>
    <!-- 键盘图标按钮 - 点击关闭语音输入模式 -->
    <div @click="emit('close')" class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
      <KeyboardIcon />
    </div>
  </div>
</template>

<style scoped>
/* 语音波形动画样式 - 控制波形条的基本高度和动画属性 */
.animate-wave {
  height: 4px;
  animation: wave-animation 0.6s ease-in-out infinite alternate;
}

/* 波形动画关键帧 - 定义从4px到20px的高度变化和透明度变化 */
@keyframes wave-animation {
  0% { height: 4px; opacity: 0.3; }
  100% { height: 20px; opacity: 1; }
}
</style>