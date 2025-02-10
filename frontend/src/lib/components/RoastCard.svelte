<script>
  export let roast = {
    title: '',
    description: '',
    date: new Date(),
    overall_score: 0,
    roast_type: '',
    origin: '',
    brew_methods: [],
    tasting_notes: []
  };
</script>

<div class="bg-white rounded-xl border border-coffee-light/20 shadow-warm overflow-hidden">
  <div class="p-6 bg-coffee-paper/30">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-coffee-deep/10 flex items-center justify-center">
          <span class="font-garamond text-coffee-deep text-lg">
            {roast.title.substring(0, 2)}
          </span>
        </div>
        <div class="text-left">
          <h3 class="font-garamond text-xl text-coffee-deep">{roast.title}</h3>
          <p class="text-sm text-coffee-medium">{roast.roast_type} • {roast.origin}</p>
        </div>
      </div>
      <div class="text-right">
        <span class="text-2xl font-garamond text-coffee-gold">{roast.overall_score}</span>
        <span class="text-sm text-coffee-medium">/100</span>
      </div>
    </div>
    
    <!-- Brew Methods -->
    {#if roast.brew_methods?.length > 0}
      <div class="grid grid-cols-3 gap-4 mt-6">
        {#each roast.brew_methods as method}
          <div class="p-3 rounded-lg bg-white/50 border border-coffee-light/10 
                     hover:shadow-warm transition-all duration-300">
            <h4 class="font-garamond text-lg text-coffee-deep mb-1">{method.name}</h4>
            <div class="flex items-center justify-center space-x-1">
              <span class="text-xl font-garamond text-coffee-gold">{method.score}</span>
              <span class="text-sm text-coffee-medium">/100</span>
            </div>
          </div>
        {/each}
      </div>
    {/if}

    <!-- Tasting Notes -->
    {#if roast.tasting_notes?.length > 0}
      <div class="mt-6 flex flex-wrap gap-2">
        {#each roast.tasting_notes as note}
          <span class="px-3 py-1 rounded-full text-sm bg-coffee-cream/50 
                     text-coffee-deep border border-coffee-gold/20">
            {note}
          </span>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .bg-coffee-paper {
    background-color: #F5F5DC;
  }
  .bg-coffee-cream {
    background-color: #FFF599;
  }
  .text-coffee-deep {
    color: #786C3B;
  }
  .text-coffee-medium {
    color: #964B00;
  }
  .text-coffee-gold {
    color: #FFD700;
  }
  .border-coffee-light {
    border-color: #F5F5DC;
  }
  .border-coffee-gold {
    border-color: #FFD700;
  }
  .shadow-warm {
    box-shadow: 0 4px 8px rgba(255, 215, 0, 0.2);
  }
</style>