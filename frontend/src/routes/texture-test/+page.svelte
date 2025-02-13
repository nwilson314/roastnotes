<script>
  // Texture comparison page
</script>

<div class="min-h-screen">
  <!-- Current Noise Texture -->
  <div class="h-[33vh] bg-coffee-cream bg-texture p-8">
    <div class="bg-white/80 backdrop-blur-sm p-4 rounded-lg inline-block">
      <h2 class="text-xl font-garamond text-coffee-deep mb-2">1. Current Noise Texture</h2>
      <p class="text-coffee-medium">Subtle noise pattern using SVG feTurbulence</p>
    </div>
  </div>

  <!-- Coffee Dots Pattern -->
  <div class="h-[33vh] bg-coffee-cream coffee-dots p-8">
    <div class="bg-white/80 backdrop-blur-sm p-4 rounded-lg inline-block">
      <h2 class="text-xl font-garamond text-coffee-deep mb-2">2. Coffee Dots Pattern</h2>
      <p class="text-coffee-medium">Organic dot pattern in coffee colors</p>
    </div>
  </div>

  <!-- New Italian Paper Texture -->
  <div class="h-[33vh] bg-coffee-cream italian-paper p-8">
    <div class="bg-white/80 backdrop-blur-sm p-4 rounded-lg inline-block">
      <h2 class="text-xl font-garamond text-coffee-deep mb-2">3. Italian Paper Texture</h2>
      <p class="text-coffee-medium">Handmade paper texture with subtle grain</p>
    </div>
  </div>
</div>

<style>
  .coffee-dots {
    background-color: #f8f4e9;
    background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23786c3b' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
  }

  .italian-paper {
    background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='paper'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.4' numOctaves='3' seed='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' values='0.3 0 0 0 0 0 0.3 0 0 0 0 0 0.3 0 0 0 0 0 0.15 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23paper)'/%3E%3C/svg%3E");
    background-size: 200px 200px;
  }
</style>
