<template>
  <section class="texture-card">
    <div class="texture-card__inner">
      <header v-if="$slots.header" class="texture-card__header">
        <slot name="header" />
      </header>
      <div class="texture-card__body">
        <slot />
      </div>
      <footer v-if="$slots.footer" class="texture-card__footer">
        <slot name="footer" />
      </footer>
    </div>
    <span class="texture-card__noise" aria-hidden="true"></span>
    <span class="texture-card__shine" aria-hidden="true"></span>
  </section>
</template>

<style scoped>
.texture-card {
  position: relative;
  isolation: isolate;
  border-radius: 26px;
  padding: 1px;
  background: linear-gradient(145deg, rgba(255, 242, 233, 0.8), rgba(245, 233, 255, 0.6));
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.18);
  overflow: hidden;
}

.texture-card__inner {
  position: relative;
  z-index: 2;
  border-radius: 24px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(250, 247, 244, 0.92));
  padding: 28px 26px 24px;
  backdrop-filter: blur(6px);
}

.texture-card__header {
  margin-bottom: 20px;
}

.texture-card__body {
  display: grid;
  gap: 16px;
}

.texture-card__footer {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px dashed rgba(15, 23, 42, 0.12);
}

.texture-card__noise {
  position: absolute;
  inset: -40%;
  z-index: 1;
  opacity: 0.18;
  background-image:
    radial-gradient(circle, rgba(15, 23, 42, 0.12) 0.6px, transparent 0.6px),
    radial-gradient(circle, rgba(15, 23, 42, 0.08) 0.5px, transparent 0.5px);
  background-size: 28px 28px, 18px 18px;
  mix-blend-mode: multiply;
  pointer-events: none;
}

.texture-card__shine {
  position: absolute;
  inset: -20% 10% auto 10%;
  height: 60%;
  z-index: 0;
  background: radial-gradient(circle at top, rgba(255, 255, 255, 0.7), transparent 60%);
  pointer-events: none;
}

@media (max-width: 640px) {
  .texture-card__inner {
    padding: 22px 20px 20px;
  }
}
</style>
