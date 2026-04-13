import { ref, computed } from 'vue'
import { useDark, useToggle } from '@vueuse/core'

/**
 * Theme composable for light/dark mode
 * Uses system preference as default, stores preference in localStorage
 */
export function useTheme() {
  const isDark = useDark({
    selector: 'html',
    attribute: 'class',
    valueDark: 'dark',
    valueLight: '',
    storageKey: 'ticket-ai-theme',
  })

  const toggleDark = useToggle(isDark)

  const themeLabel = computed(() => isDark.value ? 'Oscuro' : 'Claro')
  const themeIcon = computed(() => isDark.value ? 'sun' : 'moon')

  return {
    isDark,
    toggleDark,
    themeLabel,
    themeIcon,
  }
}
