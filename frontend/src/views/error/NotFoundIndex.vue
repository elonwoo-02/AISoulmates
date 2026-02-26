<script setup>
</script>

<template>
  <main class="page-shell flex min-h-[78vh] items-center justify-center pb-12">
    <section class="glass-panel w-full max-w-2xl p-8 text-center md:p-12">
      <p class="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">Not Found</p>
      <h1 class="brand-font mt-3 text-6xl md:text-7xl">404</h1>
      <p class="mt-4 text-[var(--muted)]">The page you requested cannot be found.</p>
      <RouterLink :to="{ name: 'homepage-index' }" class="btn mt-6 rounded-full bg-[var(--accent)] px-8 text-white hover:opacity-90">Back to Home</RouterLink>
    </section>
  </main>
</template>

<style scoped>
</style>
