<script setup lang="ts">
import { useId } from 'vue'

interface Props {
  variant?: 'default' | 'light'
  showText?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'default',
  showText: true,
})

const uid = useId()
const brainGradId = `techBrainGrad-${uid}`
const faceGradId  = `aiFaceGrad-${uid}`
</script>

<template>
  <router-link to="/" class="app-logo" :class="[`app-logo--${variant}`]">
    <div class="app-logo__icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%" aria-hidden="true">
        <defs>
          <linearGradient :id="brainGradId" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FF6B00" />
            <stop offset="100%" stop-color="#FACC15" />
          </linearGradient>
          <linearGradient :id="faceGradId" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#00C6FF" />
            <stop offset="100%" stop-color="#0072FF" />
          </linearGradient>
        </defs>

        <path
          d="M 50 10 L 70 15 L 88 35 L 90 55 L 78 78 L 60 88 L 50 84 L 40 88 L 22 78 L 10 55 L 12 35 L 30 15 Z"
          fill="none" :stroke="`url(#${brainGradId})`" stroke-width="4" stroke-linejoin="round"
        />

        <path d="M 50 10 V 25 M 50 84 V 70" fill="none" :stroke="`url(#${brainGradId})`" stroke-width="4" stroke-linecap="round" />

        <path d="M 30 15 L 40 25 V 35 M 70 15 L 60 25 V 35" fill="none" :stroke="`url(#${brainGradId})`" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" />
        <path d="M 12 35 L 25 40 M 88 35 L 75 40" fill="none" :stroke="`url(#${brainGradId})`" stroke-width="3" stroke-linecap="round" />
        <path d="M 22 78 L 30 68 M 78 78 L 70 68" fill="none" :stroke="`url(#${brainGradId})`" stroke-width="3" stroke-linecap="round" />

        <rect x="30" y="42" width="8" height="8" rx="1.5" :fill="`url(#${faceGradId})`" />
        <rect x="62" y="42" width="8" height="8" rx="1.5" :fill="`url(#${faceGradId})`" />

        <path d="M 24 46 L 30 46 M 34 36 L 34 42 M 76 46 L 70 46 M 66 36 L 66 42" fill="none" :stroke="`url(#${faceGradId})`" stroke-width="2" stroke-linecap="round" />

        <circle cx="50" cy="46" r="1.5" fill="#CBD5E1" />
        <path d="M 38 46 L 48 46 M 52 46 L 62 46" fill="none" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="2 2" />

        <path d="M 32 62 Q 50 78 68 58" fill="none" :stroke="`url(#${faceGradId})`" stroke-width="4.5" stroke-linecap="round" />
        <path d="M 60 56 L 68 58 L 66 66" fill="none" :stroke="`url(#${faceGradId})`" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </div>
    <div v-if="showText" class="app-logo__text">
      <span class="app-logo__name">TicketAI</span>
      <span class="app-logo__tagline">Mesa de Ayuda</span>
    </div>
  </router-link>
</template>

<style scoped>
.app-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
  transition: opacity 0.2s ease;
}

.app-logo:hover {
  opacity: 0.85;
}

.app-logo__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.app-logo__icon svg {
  display: block;
}

.app-logo__text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.app-logo__name {
  font-size: var(--ds-text-lg);
  font-weight: 700;
  letter-spacing: -0.025em;
  color: var(--ds-text-primary);
}

.app-logo__tagline {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
  font-weight: 400;
}

/* Light variant (for dark backgrounds) */
.app-logo--light .app-logo__name {
  color: #fff;
}

.app-logo--light .app-logo__tagline {
  color: rgba(255, 255, 255, 0.6);
}
</style>
