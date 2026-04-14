<script setup lang="ts">
import { ref } from 'vue'
import { Zap, X } from 'lucide-vue-next'

const props = defineProps<{ isLoading: boolean }>()
const emit = defineEmits<{ classify: [text: string] }>()

const text = defineModel<string>({ default: '' })

function submit() {
  if (text.value.trim()) emit('classify', text.value.trim())
}

function clear() {
  text.value = ''
}
</script>

<template>
  <div class="classify-box">
    <div class="classify-box__input-wrap">
      <textarea
        v-model="text"
        class="classify-box__textarea"
        placeholder="Escribe o pega el texto del ticket aquí…"
        rows="6"
        @keydown.ctrl.enter="submit"
        @keydown.meta.enter="submit"
      />
      <button v-if="text" class="classify-box__clear" @click="clear" title="Limpiar">
        <X :size="15" />
      </button>
    </div>
    <div class="classify-box__footer">
      <span class="classify-box__hint">Ctrl+Enter para clasificar</span>
      <span class="classify-box__count">{{ text.length }} caracteres</span>
      <button
        class="classify-box__btn"
        :disabled="!text.trim() || isLoading"
        @click="submit"
      >
        <svg v-if="isLoading" class="classify-box__spin" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M21 12a9 9 0 1 1-6.219-8.56" />
        </svg>
        <Zap v-else :size="15" />
        {{ isLoading ? 'Clasificando…' : 'Clasificar' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.classify-box {
  background: var(--ds-surface);
  border: 1px solid var(--ds-border);
  border-radius: var(--ds-radius-lg);
  overflow: hidden;
}

:global(.dark .classify-box) { background: #18181B; border-color: #27272A; }

.classify-box__input-wrap { position: relative; }

.classify-box__textarea {
  width: 100%;
  padding: 20px;
  border: none;
  background: transparent;
  color: var(--ds-text-primary);
  font-size: var(--ds-text-base);
  font-family: var(--ds-font-sans);
  line-height: 1.7;
  resize: none;
  outline: none;
}

.classify-box__textarea::placeholder { color: var(--ds-text-muted); }

.classify-box__clear {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: var(--ds-neutral-100);
  color: var(--ds-text-muted);
  border-radius: var(--ds-radius-sm);
  cursor: pointer;
  transition: all 0.15s;
}

.classify-box__clear:hover { background: var(--ds-neutral-200); color: var(--ds-text-primary); }

.classify-box__footer {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-top: 1px solid var(--ds-border);
  background: var(--ds-neutral-50);
}

:global(.dark .classify-box__footer) { background: #09090B; border-top-color: #27272A; }

.classify-box__hint, .classify-box__count {
  font-size: var(--ds-text-xs);
  color: var(--ds-text-muted);
}

.classify-box__count { margin-left: auto; }

.classify-box__btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 34px;
  padding: 0 16px;
  background: var(--ds-primary-500);
  color: #fff;
  border: none;
  border-radius: var(--ds-radius-md);
  font-size: var(--ds-text-sm);
  font-weight: 600;
  font-family: var(--ds-font-sans);
  cursor: pointer;
  transition: background 0.2s;
}

.classify-box__btn:hover:not(:disabled) { background: var(--ds-primary-700); }
.classify-box__btn:disabled { opacity: 0.6; cursor: not-allowed; }

.classify-box__spin { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
