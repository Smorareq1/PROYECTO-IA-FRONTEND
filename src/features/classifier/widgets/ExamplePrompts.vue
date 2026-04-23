<script setup lang="ts">
import type { Category } from '@/core/config/constants'
import { CATEGORY_LABELS } from '@/core/config/constants'

const emit = defineEmits<{ select: [text: string] }>()

const examples: Record<string, string> = {
  ACCOUNT:      'I need to change my account password and username, how can I do that?',
  CANCEL:       'I want to terminate my contract and stop all billing immediately.',
  CONTACT:      'How can I reach your customer support team? I need to speak with someone.',
  DELIVERY:     'My package was supposed to arrive yesterday but it still hasn\'t been delivered.',
  FEEDBACK:     'I want to leave positive feedback about my experience with your team.',
  INVOICE:      'I need a copy of my invoice from last month for my expense report.',
  ORDER:        'Where is my order? I placed it last week and have no updates yet.',
  PAYMENT:      'My payment method was declined, how can I fix this?',
  REFUND:       'I returned the product two weeks ago but still haven\'t received my refund.',
  SHIPPING:     'Can you tell me the shipping cost and estimated delivery time for my area?',
  SUBSCRIPTION: 'I want to upgrade my subscription from the basic plan to the premium plan.',
}
</script>

<template>
  <div class="examples">
    <div class="examples__chips">
      <button
        v-for="(text, cat) in examples"
        :key="cat"
        class="examples__chip"
        :class="`examples__chip--${cat}`"
        @click="emit('select', text)"
        :title="text"
      >
        <span class="examples__chip-dot"></span>
        <span class="examples__chip-label">{{ CATEGORY_LABELS[cat as Category] }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.examples__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.examples__chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 32px;
  padding: 0 14px;
  border-radius: var(--ds-radius-sm);
  font-size: var(--ds-text-xs);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  background: var(--ds-surface);
  color: var(--ds-text-primary);
  border: 1px solid var(--ds-border);
  cursor: pointer;
  transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

:global(.dark .examples__chip) {
  background: #18181B;
  border-color: #27272A;
}

.examples__chip-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.examples__chip-label { letter-spacing: 0.01em; }

.examples__chip--ACCOUNT      .examples__chip-dot { background: var(--ds-cat-account); }
.examples__chip--CANCEL        .examples__chip-dot { background: var(--ds-cat-cancel); }
.examples__chip--CONTACT       .examples__chip-dot { background: var(--ds-cat-contact); }
.examples__chip--DELIVERY      .examples__chip-dot { background: var(--ds-cat-delivery); }
.examples__chip--FEEDBACK      .examples__chip-dot { background: var(--ds-cat-feedback); }
.examples__chip--INVOICE       .examples__chip-dot { background: var(--ds-cat-invoice); }
.examples__chip--ORDER         .examples__chip-dot { background: var(--ds-cat-order); }
.examples__chip--PAYMENT       .examples__chip-dot { background: var(--ds-cat-payment); }
.examples__chip--REFUND        .examples__chip-dot { background: var(--ds-cat-refund); }
.examples__chip--SHIPPING      .examples__chip-dot { background: var(--ds-cat-shipping); }
.examples__chip--SUBSCRIPTION  .examples__chip-dot { background: var(--ds-cat-subscription); }

.examples__chip--ACCOUNT:hover      { border-color: var(--ds-cat-account);      box-shadow: 0 2px 0 var(--ds-cat-account);      transform: translateY(-1px); }
.examples__chip--CANCEL:hover       { border-color: var(--ds-cat-cancel);       box-shadow: 0 2px 0 var(--ds-cat-cancel);       transform: translateY(-1px); }
.examples__chip--CONTACT:hover      { border-color: var(--ds-cat-contact);      box-shadow: 0 2px 0 var(--ds-cat-contact);      transform: translateY(-1px); }
.examples__chip--DELIVERY:hover     { border-color: var(--ds-cat-delivery);     box-shadow: 0 2px 0 var(--ds-cat-delivery);     transform: translateY(-1px); }
.examples__chip--FEEDBACK:hover     { border-color: var(--ds-cat-feedback);     box-shadow: 0 2px 0 var(--ds-cat-feedback);     transform: translateY(-1px); }
.examples__chip--INVOICE:hover      { border-color: var(--ds-cat-invoice);      box-shadow: 0 2px 0 var(--ds-cat-invoice);      transform: translateY(-1px); }
.examples__chip--ORDER:hover        { border-color: var(--ds-cat-order);        box-shadow: 0 2px 0 var(--ds-cat-order);        transform: translateY(-1px); }
.examples__chip--PAYMENT:hover      { border-color: var(--ds-cat-payment);      box-shadow: 0 2px 0 var(--ds-cat-payment);      transform: translateY(-1px); }
.examples__chip--REFUND:hover       { border-color: var(--ds-cat-refund);       box-shadow: 0 2px 0 var(--ds-cat-refund);       transform: translateY(-1px); }
.examples__chip--SHIPPING:hover     { border-color: var(--ds-cat-shipping);     box-shadow: 0 2px 0 var(--ds-cat-shipping);     transform: translateY(-1px); }
.examples__chip--SUBSCRIPTION:hover { border-color: var(--ds-cat-subscription); box-shadow: 0 2px 0 var(--ds-cat-subscription); transform: translateY(-1px); }

.examples__chip:active { transform: translateY(0); box-shadow: none; }
</style>
