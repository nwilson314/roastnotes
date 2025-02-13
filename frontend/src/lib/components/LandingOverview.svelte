<script lang="ts">
  import RoastCard from './RoastCard.svelte';
  import { RoastLevel } from '$lib/types';
  import type { Roast } from '$lib/types';

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
  const sampleRoast: Roast = {
    id: 0,
    user_id: 0,
    roaster_id: 1,
    name: "Ethiopian Yirgacheffe",
    origin: "Ethiopia",
    single_origin: true,
    roast_level: RoastLevel.light,
    created_at: new Date().toISOString(),
    bean_details: {
      id: 0,
      roast_id: 0,
      species: "Arabica",
      cultivar: "Heirloom",
      processing_method: "Washed",
      altitude: 1900,
      extra: {
        region: "Yirgacheffe"
      }
    },
    cached_rating_stats: {
      avg_rating: 4.8,
      total_ratings: 42,
      brew_methods: {
        'V60': {
          count: 18,
          avg_rating: 4.9
        },
        'Chemex': {
          count: 12,
          avg_rating: 4.7
        },
        'AeroPress': {
          count: 8,
          avg_rating: 4.8
        }
      }
    }
  };
</script>

<section class="relative py-8 overflow-hidden">
  <div class="absolute inset-0 bg-coffee-paper bg-opacity-50"></div>
  
  <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-12">
      <!-- Preview Section -->
      <div class="mb-12">
        <h1 class="text-4xl font-garamond font-medium text-coffee-deep mb-4">
          Share Your Coffee Journey
        </h1>
        <p class="text-lg text-coffee-medium mb-8">
          Join our community of coffee enthusiasts and share your roasting experiences
        </p>
        <div class="flex gap-4 justify-center mb-16">
          <a 
            href="/roasts" 
            class="px-6 py-3 rounded-lg bg-coffee-medium text-coffee-cream 
                   hover:bg-coffee-deep transition-colors duration-200
                   border border-coffee-gold/20"
          >
            View Roasts
          </a>
          <a 
            href="/register" 
            class="px-6 py-3 rounded-lg bg-coffee-cream text-coffee-medium
                   hover:bg-coffee-light hover:text-coffee-deep transition-colors duration-200
                   border border-coffee-light"
          >
            Join Now
          </a>
        </div>
        <p class="max-w-2xl mx-auto text-coffee-medium mb-6 text-lg">
          Rate your roasts, share brewing methods, and discover new flavors.
          Here's how your roast will look:
        </p>
        
        <div class="max-w-2xl mx-auto">
          <RoastCard roast={sampleRoast} />
        </div>
      </div>
      
      <!-- Feature Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
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
