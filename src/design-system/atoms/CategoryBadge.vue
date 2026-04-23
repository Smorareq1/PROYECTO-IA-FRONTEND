<script setup lang="ts">
import { computed } from 'vue'
import type { Category } from '@/core/config/constants'
import { CATEGORY_LABELS } from '@/core/config/constants'

interface Props {
  category: Category
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
})

const label = computed(() => CATEGORY_LABELS[props.category] || props.category)
</script>

<template>
  <span
    class="category-badge"
    :class="[`category-badge--${category}`, `category-badge--${size}`]"
  >
    {{ label }}
  </span>
</template>

<style scoped>
.category-badge {
  display: inline-flex;
  align-items: center;
  font-weight: 600;
  border-radius: var(--ds-radius-sm);
  white-space: nowrap;
  transition: all 0.15s ease;
}

/* Sizes */
.category-badge--sm {
  font-size: 0.6875rem;
  padding: 2px 8px;
  letter-spacing: 0.01em;
}

.category-badge--md {
  font-size: var(--ds-text-xs);
  padding: 4px 10px;
}

.category-badge--lg {
  font-size: var(--ds-text-sm);
  padding: 6px 14px;
}

/* Category colors (11 Bitext dataset categories) */
.category-badge--ACCOUNT      { color: var(--ds-cat-account);      background: var(--ds-cat-account-bg); }
.category-badge--CANCEL        { color: var(--ds-cat-cancel);       background: var(--ds-cat-cancel-bg); }
.category-badge--CONTACT       { color: var(--ds-cat-contact);      background: var(--ds-cat-contact-bg); }
.category-badge--DELIVERY      { color: var(--ds-cat-delivery);     background: var(--ds-cat-delivery-bg); }
.category-badge--FEEDBACK      { color: var(--ds-cat-feedback);     background: var(--ds-cat-feedback-bg); }
.category-badge--INVOICE       { color: var(--ds-cat-invoice);      background: var(--ds-cat-invoice-bg); }
.category-badge--ORDER         { color: var(--ds-cat-order);        background: var(--ds-cat-order-bg); }
.category-badge--PAYMENT       { color: var(--ds-cat-payment);      background: var(--ds-cat-payment-bg); }
.category-badge--REFUND        { color: var(--ds-cat-refund);       background: var(--ds-cat-refund-bg); }
.category-badge--SHIPPING      { color: var(--ds-cat-shipping);     background: var(--ds-cat-shipping-bg); }
.category-badge--SUBSCRIPTION  { color: var(--ds-cat-subscription); background: var(--ds-cat-subscription-bg); }
</style>
