<script>
  import RoastCard from './RoastCard.svelte';

  // Feature highlights for the landing page
  const features = [
    {
      title: "Share Your Roasts",
      description: "Document your coffee journey with rich bean details and brewing notes"
    },
    {
      title: "Rate Your Brews",
      description: "Score each method - from V60 to Moka pot - capturing the perfect cup"
    },
    {
      title: "Join the Table",
      description: "Connect with fellow coffee lovers in a warm, inviting space"
    }
  ];

  // Sample roast for preview
  const sampleRoast = {
    title: "Ethiopian Yirgacheffe",
    roast_type: "Light Roast",
    origin: "Single Origin",
    overall_score: 94,
    brew_methods: [
      { name: 'V60', score: 92 },
      { name: 'Aeropress', score: 88 },
      { name: 'Moka Pot', score: 90 }
    ],
    tasting_notes: ['Floral', 'Citrus', 'Honey', 'Jasmine']
  };
</script>

<section class="relative py-16 overflow-hidden">
  <div class="absolute inset-0 bg-coffee-paper bg-opacity-50"></div>
  
  <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-16">
      <!-- Preview Section -->
      <div class="mb-16">
        <h2 class="font-garamond text-3xl text-coffee-deep mb-6">
          Share Your Coffee Journey
        </h2>
        <p class="max-w-2xl mx-auto text-coffee-medium mb-8 text-lg">
          Rate your roasts, share brewing methods, and discover new flavors.
          Here's how your roast will look:
        </p>
        
        <div class="max-w-2xl mx-auto">
          <RoastCard roast={sampleRoast} />
        </div>
      </div>
      
      <!-- Feature Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
        {#each features as feature}
          <div class="p-6 bg-white/80 rounded-xl shadow-warm
                      border border-coffee-light/10
                      transition-all duration-300 ease-out 
                      hover:shadow-warm-lg hover:scale-101">
            <h3 class="font-garamond text-2xl text-coffee-deep mb-4">
              {feature.title}
            </h3>
            <p class="text-coffee-medium">
              {feature.description}
            </p>
          </div>
        {/each}
      </div>
    </div>
  </div>
  
  <!-- Decorative elements -->
  <div class="absolute top-1/2 left-0 w-96 h-96 -translate-y-1/2 -translate-x-1/2 
              bg-coffee-gold/5 rounded-full blur-3xl"></div>
  <div class="absolute top-1/2 right-0 w-96 h-96 -translate-y-1/2 translate-x-1/2 
              bg-coffee-burgundy/5 rounded-full blur-3xl"></div>
  
  <!-- Subtle grain texture overlay -->
  <div class="absolute inset-0 bg-texture opacity-20 pointer-events-none"></div>
</section>

<style>
  /* Add any additional custom styles here if needed */
</style>
