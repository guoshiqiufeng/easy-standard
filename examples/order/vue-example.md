# Vue 3 订单列表示例

对应规则：VUE-003～VUE-006、VUE-009、API-004、API-005。

以下为 JavaScript 单文件组件片段。`useOrdersApi` 是项目提供的请求适配接口，不是指定依赖；它的 `list({ page, pageSize, signal })` 返回解包后的 `data`，失败抛出含 `code、message、traceId` 的安全错误。它负责认证、超时、HTTP 与业务码校验，不自动重试写操作。

```vue
<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue';
import { useOrdersApi } from './orders-api';

const ordersApi = useOrdersApi();
const orders = ref([]);
const loading = ref(false);
const errorMessage = ref('');
const traceId = ref('');
let controller;
let generation = 0;

async function loadOrders() {
  const currentGeneration = ++generation;
  controller?.abort();
  controller = new AbortController();
  loading.value = true;
  errorMessage.value = '';
  traceId.value = '';
  try {
    const data = await ordersApi.list({
      page: 1,
      pageSize: 20,
      signal: controller.signal,
    });
    if (currentGeneration === generation) {
      orders.value = data.items;
    }
  } catch (error) {
    if (currentGeneration !== generation || error.name === 'AbortError') {
      return;
    }
    errorMessage.value = error.message || '订单加载失败，请重试';
    traceId.value = error.traceId || '';
  } finally {
    if (currentGeneration === generation) {
      loading.value = false;
    }
  }
}

onMounted(loadOrders);
onBeforeUnmount(() => {
  generation += 1;
  controller?.abort();
});
</script>

<template>
  <section aria-labelledby="orders-heading" :aria-busy="loading">
    <h1 id="orders-heading">我的订单</h1>
    <button type="button" :disabled="loading" @click="loadOrders">刷新</button>
    <p v-if="loading" role="status">正在加载订单…</p>
    <div v-else-if="errorMessage" role="alert">
      <p>{{ errorMessage }}</p>
      <p v-if="traceId">问题编号：{{ traceId }}</p>
      <button type="button" @click="loadOrders">重试</button>
    </div>
    <p v-else-if="orders.length === 0">暂无订单</p>
    <ul v-else>
      <li v-for="order in orders" :key="order.id">
        {{ order.id }}：{{ order.totalAmount }} {{ order.currency }}
      </li>
    </ul>
  </section>
</template>
```

本片段仅演示第一页查询、加载、空状态、错误和竞态。完整页面须增加分页控件、详情导航和产品样式。不能将 ID 或金额传入 `Number` 后再展示；金额计算由服务端决定。错误适配层只提供可展示信息，不直接展示原始代理 HTML 或堆栈。

创建表单需要单独覆盖：`quantity` 输入转换为受限整数，`productId` 始终为字符串；一次创建意图生成一次幂等键，超时后保留原键和原载荷，不能在每次重试时生成新键。收到确定成功后才允许新意图；已确定无副作用的校验失败可修正输入并创建新意图。键过期或提交结果未知时引导查询订单，避免盲目重建。

待执行验证：乱序请求只显示最后一次结果；卸载后不更新状态；错误与空页可区分；大 ID 完整显示；键盘可操作；同一创建重试不重复；未登录与无权限由统一适配正确处理。
