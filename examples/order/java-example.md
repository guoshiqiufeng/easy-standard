# Java 订单规则示例

对应规则：JAVA-002、JAVA-003、JAVA-008、JAVA-009、API-005、API-006。

下面是可独立阅读的纯计算规则片段；采用常见 Java 语法，不指定框架、构建工具或 JDK 基线。并发、持久化和认证行为由实际应用实现并测试。

```java
package com.example.order.domain;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * 示例 CNY 订单的金额规则，不处理存储或外部调用。
 */
public final class OrderPricing {

    private static final int MIN_QUANTITY = 1;
    private static final int MAX_QUANTITY = 100;
    private static final int AMOUNT_SCALE = 2;

    private OrderPricing() {
    }

    /**
     * 根据服务端报价计算总额。
     *
     * @param unitPrice 服务端取得的非负 CNY 单价，必须能精确表达为两位小数
     * @param quantity 购买数量，范围为 1 至 100
     * @return 两位小数总额
     * @throws IllegalArgumentException 单价或数量不符合规则
     */
    public static BigDecimal calculateTotal(BigDecimal unitPrice, int quantity) {
        if (unitPrice == null || unitPrice.signum() < 0) {
            throw new IllegalArgumentException("Invalid unit price");
        }
        if (quantity < MIN_QUANTITY || quantity > MAX_QUANTITY) {
            throw new IllegalArgumentException("Invalid quantity");
        }
        final BigDecimal normalizedPrice;
        try {
            normalizedPrice = unitPrice.setScale(AMOUNT_SCALE, RoundingMode.UNNECESSARY);
        } catch (ArithmeticException exception) {
            throw new IllegalArgumentException("Unit price exceeds currency precision", exception);
        }
        return normalizedPrice.multiply(BigDecimal.valueOf(quantity));
    }
}
```

示例输入 `new BigDecimal("12.50")` 和 `2`，输出用 `toPlainString()` 序列化为 `"25.00"`。`0`、`101`、负单价或 `12.501` 均拒绝。允许 `12.500`，因为能精确规范化为两位小数；业务实际要求更严格时另行定义。

## 用例边界

1. 接入层解析请求、校验字段和幂等键，从认证上下文取得 ownerId；缺少身份返回 401，无创建权限返回 403。
2. 应用层先查该用户的已完成幂等结果；相同指纹且仍有权限时重放结果，不重复询价；不同指纹返回 409。
3. 新意图通过商品模块公开接口取得有效报价，在数据库事务外完成受限的外部等待；报价失败没有订单副作用。
4. 进入事务，写入唯一幂等记录、保存订单和原响应快照，原子提交。并发唯一约束冲突在回滚后处理；无界重试禁止。
5. 接入层将 ID 和 BigDecimal 转成字符串，加入本次 traceId；创建返回 201 和 `Location`。持久化实体不能直接成为响应模型。

全局异常处理需要按来源区分：客户端数量错误映射 400；服务端报价精度错误代表依赖或内部数据问题，应记录受控日志并返回安全的服务错误，不能把所有 `IllegalArgumentException` 一律当成客户端错误。

## 需要实际项目验证

纯计算单元测试；真实数据库的唯一约束和事务回滚；同键并发与超时后重试；提交结果未知的查询恢复；授权撤销后的重放；响应序列化。只有这些测试通过后，才能声明实际实现符合规则。
