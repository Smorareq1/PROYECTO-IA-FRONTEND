import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Prediction } from '../models/prediction'

export interface PlaygroundEntry {
  text: string
  prediction: Prediction
  timestamp: string
}

export const usePlaygroundStore = defineStore('playground', () => {
  const history = ref<PlaygroundEntry[]>([])

  function addEntry(text: string, prediction: Prediction) {
    history.value.unshift({ text, prediction, timestamp: new Date().toISOString() })
    if (history.value.length > 20) history.value = history.value.slice(0, 20)
  }

  function clearHistory() {
    history.value = []
  }

  return { history, addEntry, clearHistory }
}, { persist: true })
