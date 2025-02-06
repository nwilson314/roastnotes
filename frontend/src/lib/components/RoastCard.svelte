<script>
  export let roast;
</script>

<div class="card group animate-warm-fade-in">
  <div class="space-y-3">
    <h3 class="font-garamond text-xl font-semibold text-coffee-deep group-hover:text-coffee-burgundy transition-colors duration-200">
      {roast.title}
    </h3>
    <p class="text-coffee-medium/90 font-inter text-base leading-relaxed">
      {roast.description}
    </p>
    <div class="pt-4 flex justify-between items-center border-t border-coffee-deep/10">
      <div class="flex items-center space-x-2">
        <span class="text-sm text-coffee-light">
          {new Date(roast.date).toLocaleDateString()}
        </span>
      </div>
      <button class="btn btn-secondary text-sm py-1">
        View Details
      </button>
    </div>
  </div>
</div>

<style>
  .card {
    background: #fff;
    border: 1px solid var(--secondary-color);
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.2);
  }
</style>