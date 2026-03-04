/*
 * 功能：在每个请求头里自动添加`access token`。
 * 然后拦截请求结果，如果返回结果是身份认证失败（401），
 * 则说明`access_token`过期了，那么调用api刷新token`，
 * 如果刷新成功，则重新发送原请求。
*/

import { fetchEventSource } from '@microsoft/fetch-event-source';
import { useUserStore } from "@/stores/user.js";
import api from "./api.js";

const BASE_URL = 'http://127.0.0.1:8000'

/**
 * 通用的流式请求工具
 * @param {string} url 请求地址
 * @param {object} options 配置项 (method, body, onmessage, onerror等)
 */
export default async function streamApi(url, options = {}) {
    const userStore = useUserStore();

    const startFetch = async () => {
        return await fetchEventSource(BASE_URL + url, {
            method: options.method || 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userStore.accessToken}`,
                ...options.headers,
            },
            body: JSON.stringify(options.body || {}),

            openWhenHidden: true,  // 允许后台运行，防止浏览器因隐藏页面而强制关闭它
            async onopen(response) {
                // 1. 处理 401 Token 过期
                if (response.status === 401) {
                    try {
                        // 触发 api.js 中的 Axios 拦截器进行静默刷新
                        await api.post('/api/user/account/refresh_token/', {});
                        // 抛出特定错误触发下面的 onerror 重试逻辑
                        throw new Error("TOKEN_REFRESHED");
                    } catch (err) {
                        // 如果刷新失败（refresh_token也过期），直接报错由上层处理
                        throw err;
                    }
                }

                if (!response.ok || !response.headers.get('content-type')?.includes('text/event-stream')) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.detail || `请求失败: ${response.status}`);
                }
            },

            onmessage(msg) {
                if (msg.data === '[DONE]') {
                    if (options.onmessage) options.onmessage('', true);
                    return
                }
                try {
                    const json = JSON.parse(msg.data);
                    if (options.onmessage) options.onmessage(json, false);
                } catch (e) {
                    console.error("流解析失败:", e);
                }
            },

            onerror(err) {
                // 2. 捕获重试信号并递归
                if (err.message === "TOKEN_REFRESHED") {
                    return startFetch();
                }

                // 其他错误则按用户定义的 onerror 处理
                if (options.onerror) {
                    options.onerror(err);
                }
                throw err; // 停止自动重试
            },

            onclose: options.onclose,
        });
    };

    return await startFetch();
}