<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();
</script>

<template>
  <div class="relative flex flex-col items-center justify-center h-screen text-center px-4">
    <h1 class="absolute bottom-0 text-9xl md:text-[12rem] font-black text-gray-50 select-none pointer-events-none z-0">
      404
    </h1>
    <div class="relative z-10">
      <h1 class="text-xl md:text-2xl font-semibold mt-6">This page has not been generated</h1>
      <p class="mt-2 text-base text-gray-400 font-mono">{{ route.path }}</p>
      <p class="mt-4 text-lg md:text-xl text-gray-500">Tell me more about this page, so I can generate it</p>
    </div>
  </div>
</template>
