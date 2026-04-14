<template>
  <div class="page-decor" aria-hidden="true">
    <div class="page-decor__dots"></div>
    <div class="page-decor__shape page-decor__shape--circle"></div>
    <div class="page-decor__shape page-decor__shape--circle-sm"></div>
    <div class="page-decor__shape page-decor__shape--square"></div>
    <div class="page-decor__shape page-decor__shape--square-sm"></div>
    <div class="page-decor__shape page-decor__shape--block"></div>
    <div class="page-decor__shape page-decor__shape--block-outline"></div>
    <div class="page-decor__shape page-decor__shape--triangle"></div>
    <div class="page-decor__shape page-decor__shape--line"></div>
    <div class="page-decor__shape page-decor__shape--line-v"></div>
    <div class="page-decor__shape page-decor__shape--plus"></div>
  </div>
</template>

<style scoped>
.page-decor {
  position: fixed;
  inset: 56px 0 0 0; /* below topbar */
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

/* Dotted pattern — subtle base */
.page-decor__dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(var(--ds-neutral-200) 1px, transparent 1px);
  background-size: 32px 32px;
  opacity: 0.35;
}

:global(.dark .page-decor__dots) {
  background-image: radial-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  opacity: 0.5;
}

.page-decor__shape { position: absolute; }

/* Outlined circle — bottom-right, cropped */
.page-decor__shape--circle {
  width: 460px;
  height: 460px;
  border: 1.5px solid var(--ds-primary-500);
  border-radius: 50%;
  right: -180px;
  bottom: -200px;
  opacity: 0.14;
}

:global(.dark .page-decor__shape--circle) { opacity: 0.22; }

/* Smaller outlined circle — top-left */
.page-decor__shape--circle-sm {
  width: 140px;
  height: 140px;
  border: 1.5px solid var(--ds-neutral-300);
  border-radius: 50%;
  top: -50px;
  left: 12%;
  opacity: 0.3;
}

:global(.dark .page-decor__shape--circle-sm) {
  border-color: var(--ds-neutral-200);
  opacity: 0.22;
}

/* Outlined square, rotated — top-right */
.page-decor__shape--square {
  width: 190px;
  height: 190px;
  border: 1.5px solid var(--ds-neutral-300);
  top: 40px;
  right: 6%;
  transform: rotate(12deg);
  opacity: 0.4;
}

:global(.dark .page-decor__shape--square) {
  border-color: var(--ds-neutral-200);
  opacity: 0.3;
}

/* Small rotated square — mid area */
.page-decor__shape--square-sm {
  width: 72px;
  height: 72px;
  border: 1.5px solid var(--ds-neutral-300);
  bottom: 22%;
  right: 42%;
  transform: rotate(-14deg);
  opacity: 0.35;
}

:global(.dark .page-decor__shape--square-sm) {
  border-color: var(--ds-neutral-200);
  opacity: 0.25;
}

/* Solid block — far left edge */
.page-decor__shape--block {
  width: 52px;
  height: 52px;
  background: var(--ds-primary-500);
  top: 25%;
  left: -26px;
  opacity: 0.75;
}

/* Outlined block — bottom-left */
.page-decor__shape--block-outline {
  width: 44px;
  height: 44px;
  border: 1.5px solid var(--ds-primary-500);
  bottom: 14%;
  left: 8%;
  opacity: 0.35;
  transform: rotate(-8deg);
}

/* Outlined triangle — mid-left, low opacity */
.page-decor__shape--triangle {
  width: 0;
  height: 0;
  border-left: 42px solid transparent;
  border-right: 42px solid transparent;
  border-bottom: 68px solid var(--ds-primary-500);
  top: 62%;
  left: 34%;
  opacity: 0.1;
  transform: rotate(18deg);
}

:global(.dark .page-decor__shape--triangle) { opacity: 0.18; }

/* Hard horizontal rule — mid-right */
.page-decor__shape--line {
  width: 108px;
  height: 3px;
  background: var(--ds-text-primary);
  top: 46%;
  right: 18%;
  opacity: 0.5;
}

/* Vertical rule — right side */
.page-decor__shape--line-v {
  width: 3px;
  height: 82px;
  background: var(--ds-primary-500);
  top: 14%;
  right: 3%;
  opacity: 0.55;
}

/* Plus mark — top-center */
.page-decor__shape--plus {
  width: 26px;
  height: 26px;
  top: 10%;
  left: 48%;
  opacity: 0.4;
}

.page-decor__shape--plus::before,
.page-decor__shape--plus::after {
  content: '';
  position: absolute;
  background: var(--ds-text-primary);
}

.page-decor__shape--plus::before {
  top: 50%; left: 0; right: 0;
  height: 2px;
  transform: translateY(-50%);
}

.page-decor__shape--plus::after {
  left: 50%; top: 0; bottom: 0;
  width: 2px;
  transform: translateX(-50%);
}

@media (max-width: 768px) {
  /* Hide decorative noise on small screens for clarity */
  .page-decor__shape--square,
  .page-decor__shape--square-sm,
  .page-decor__shape--triangle,
  .page-decor__shape--line,
  .page-decor__shape--plus {
    display: none;
  }
}
</style>
